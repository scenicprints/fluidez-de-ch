# -*- coding: utf-8 -*-
"""Checks that the course actually recycles its vocabulary.

Ported from es-ni's, whose numbers were calibrated against a real 185-story
course. The disease it was built for: that course's predecessor taught 769
words and let 42% of them appear in exactly one lesson, ever, median two
encounters. You cannot learn a word from two encounters, so the decay model
correctly forgot almost all of them and 81 lessons left the reader with 187
words.

The fix is not in the app, it is in the writing, and **writing recycles by
accident unless something checks.** So this is a build gate: a story that fails
its quota does not ship.

Three rules, all measured at the LEMMA so that Zug, Züge and dem Zug are one
word:

  COVERAGE   at least 88% of the dictionary words in a story must already have
             been introduced by an earlier story, ramping up from 60% because
             story four cannot have 88% known - there are three stories of
             German in existence at that point.

  DENSITY    every word a story DECLARES it teaches - its warm-up - must appear
             at least 5 times in that story. One occurrence is a sighting, not
             context. This also kills the old bug by construction: in the
             course es-ni replaced, 46% of warm-up words never appeared in the
             lesson that warmed them up.

  RETURN     every declared word must come back in at least 6 LATER stories.
             Incidental vocabulary is exempt - you arrive at a Flughafen once.
             A word is judged only once RETURN_WINDOW stories exist after it,
             so a half-written course never false-alarms.

---------------------------------------------------------------------------
WHAT GERMAN CHANGES, AND IT IS ONE THING THAT MATTERS

es-ni lower-cases every token before looking it up, which is right for Spanish
and would be catastrophic here: German capitalises every noun, so `.lower()`
would find none of them and the gate would silently measure the function words
only. Every lookup goes through `lemma_of`, which tries the exact spelling
first and the lower-cased one second - the same rule the app's own dictKey()
uses, so the gate counts exactly the words the reader can tap.
---------------------------------------------------------------------------
"""
import argparse, collections, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import forms as morphology  # noqa: E402

TOKEN = re.compile(u"[^\\W\\d_]+", re.UNICODE)
SPINE_ID = re.compile(u"^p[0-7]-\\d\\d$")
NEWLINE = chr(10)

COVERAGE_MIN = 0.88
COVERAGE_START = 0.60    # what story four is held to
RAMP = 50
#   50, not 25: phases 0 and 1 are where the base vocabulary is built, and in
#   German they are 38 stories between them. Demanding 88% known while the
#   course is still assembling its first thousand words just blocks the words
#   from arriving.
DENSITY_MIN = 5
RETURN_MIN = 6
RETURN_WINDOW = 25
ONE_SCENE = 0.60
#   A word can be exempt from RETURN by being a ONE-SCENE word: this much of
#   everything the course ever says with it is said in the story that teaches
#   it. Fasnacht is like that, and so is Gipfeli. Demanding a festival noun
#   turn up in six of the following stories does not teach it, it only stops
#   the lesson being allowed to warm it up, which teaches it less.

# Structural rather than vocabulary. They are in every story whether anybody
# planned it or not, so holding them to a recycling quota measures nothing and
# buries the words that matter. `contr` is German's own addition: am, im, zum.
FUNCTION_POS = (u"prep", u"art", u"conj", u"contr", u"pron", u"num")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def lemma_of(word, dictionary, forms):
    """Which dictionary entry this written word is, or None.

    Exact spelling first, lower-cased second. See the header: lower-casing
    first loses every German noun.
    """
    for k in (word, word.lower()):
        if k in dictionary:
            return k
        if k in forms and forms[k] in dictionary:
            return forms[k]
    return None


def is_content(word, dictionary):
    pos = (dictionary.get(word, {}).get("pos") or u"").split(u"/")[0]
    return pos not in FUNCTION_POS


def one_scene(here, everywhere):
    return everywhere > 0 and here / float(everywhere) >= ONE_SCENE


SPLIT = re.compile(r"([^\W\d_]+|[^\w\s]|\s+)", re.UNICODE)


def story_words(lesson, dictionary, forms, verbs=None):
    """Every dictionary word in the story, counted at the lemma.

    Separable verbs are counted as ONE word across their two halves, exactly
    as the reader resolves them. Counting token by token scored ankommen at
    zero in the story that is full of "Der Zug kommt in Luzern an" - the gate
    was measuring a reading nobody gets, and would have had the story rewritten
    to fix a fault in the gate.
    """
    counts = collections.Counter()
    for sn in lesson.get("sn") or lesson.get("sentences") or []:
        text = sn.get("s") or sn.get("es") or u""
        words = []
        for piece in SPLIT.findall(text):
            if TOKEN.match(piece):
                words.append((piece, False))
            elif piece.strip() and re.match(u"[,;:.!?]", piece):
                words.append((piece, True))
        bound = morphology.separable_bindings(
            words, lambda w: lemma_of(w, dictionary, forms), verbs or {})
        counted = set()
        for i, (w, is_end) in enumerate(words):
            if is_end:
                continue
            if i in bound:
                # Both halves are the same word, so it counts once per clause.
                key = (bound[i], min(k for k in bound if bound[k] == bound[i]))
                if key in counted:
                    continue
                counted.add(key)
                counts[bound[i]] += 1
                continue
            lem = lemma_of(w, dictionary, forms)
            if lem:
                counts[lem] += 1
    return counts


def check(pack, spine_order=None):
    """Returns (problems, stats). A problem is a hard build failure."""
    dictionary = pack.get("dictionary") or {}
    forms = pack.get("forms") or {}
    lessons = [l for l in (pack.get("lessons") or [])
               if SPINE_ID.match(str(l.get("id") or u""))]
    if not lessons:
        return [], {"stories": 0}

    # Reading order is the spine's, not whatever the manifest happens to list:
    # "already introduced" only means anything in the order somebody reads.
    if spine_order:
        rank = dict((sid, i) for i, sid in enumerate(spine_order))
        lessons.sort(key=lambda l: rank.get(l.get("id"), 10 ** 6))
    else:
        lessons.sort(key=lambda l: str(l.get("id")))

    verbs = pack.get("verbs") or {}
    counts = [story_words(l, dictionary, forms, verbs) for l in lessons]

    problems = []
    introduced, known = {}, set()
    thin, weak = [], []
    local = 0

    for i, (lesson, c) in enumerate(zip(lessons, counts)):
        sid = lesson.get("id")
        if not c:
            problems.append(u"%s has no dictionary words in it at all" % sid)
            continue

        fresh = [w for w in c if w not in known]
        coverage = (len(c) - len(fresh)) / float(len(c))

        need = COVERAGE_MIN
        if i < RAMP:
            need = COVERAGE_START + (COVERAGE_MIN - COVERAGE_START) * (i / float(RAMP))
        if i >= 3 and coverage < need:
            problems.append(
                u"%s: only %.0f%% of its words were introduced earlier (need %.0f%%). "
                u"%d new words in one story is too many to infer."
                % (sid, 100 * coverage, 100 * need, len(fresh)))

        for w in fresh:
            introduced[w] = i
        known.update(fresh)

        for raw in lesson.get("wu") or lesson.get("warmup") or []:
            if u" " in raw:
                # "merci vielmal" and "Grüezi mitenand" are one entry and two
                # tokens, so a word counter can never see them. Count the
                # phrase in the raw text instead.
                low = raw.lower()
                hits = sum((sn.get("s") or sn.get("es") or u"").lower().count(low)
                           for sn in lesson.get("sn") or lesson.get("sentences") or [])
                if hits < DENSITY_MIN:
                    thin.append((sid, raw, hits))
                continue
            w = lemma_of(raw, dictionary, forms) or raw
            if c.get(w, 0) < DENSITY_MIN:
                thin.append((sid, raw, c.get(w, 0)))

    # Reported per story, so a story with eight thin words is one readable
    # failure rather than eight.
    by_story = collections.defaultdict(list)
    for sid, w, n in thin:
        by_story[sid].append(u"%s(%dx)" % (w, n))
    for sid in sorted(by_story):
        ws = by_story[sid]
        problems.append(
            u"%s introduces %d word(s) it barely uses: %s. A new word needs %d "
            u"uses in the story that teaches it, or there is no context to work "
            u"it out from." % (sid, len(ws), u", ".join(sorted(ws)[:10]), DENSITY_MIN))

    # RETURN. The window runs from the story that CLAIMS the word, not from
    # wherever it first happened to appear.
    last = len(lessons) - 1
    targets = {}
    for i, lesson in enumerate(lessons):
        for raw in lesson.get("wu") or lesson.get("warmup") or []:
            w = lemma_of(raw, dictionary, forms)
            if w and w in introduced:
                targets[w] = i

    judged = 0
    for w, at in sorted(targets.items()):
        if not is_content(w, dictionary):
            continue
        window = list(range(at + 1, last + 1))
        # Judged only once there is enough course after it to judge with.
        # Scaling the requirement down for a short tail ends up demanding that
        # EVERY remaining story contain EVERY word, which flagged 109 words in
        # story one when six stories existed.
        if len(window) < RETURN_WINDOW:
            continue
        judged += 1
        came_back = sum(1 for j in window if counts[j].get(w))
        if came_back < RETURN_MIN:
            everywhere = sum(c.get(w, 0) for c in counts)
            if one_scene(counts[at].get(w, 0), everywhere):
                local += 1
                continue
            weak.append((lessons[at].get("id"), w))

    per_story = collections.defaultdict(list)
    for sid, w in weak:
        per_story[sid].append(w)
    for sid in sorted(per_story):
        ws = per_story[sid]
        problems.append(
            u"%s introduces %d word(s) that never come back: %s. Every new word "
            u"has to reappear in at least %d later stories or it is taught once "
            u"and forgotten." % (sid, len(ws), u", ".join(sorted(ws)[:10]), RETURN_MIN))

    encounters = collections.Counter()
    for c in counts:
        for w, n in c.items():
            encounters[w] += n
    vals = sorted(encounters.values())
    stats = {
        "stories": len(lessons),
        "running_words": sum(sum(c.values()) for c in counts),
        "vocabulary": len(encounters),
        "median_encounters": vals[len(vals) // 2] if vals else 0,
        "reach_ten": sum(1 for v in encounters.values() if v >= 10),
        "one_scene": local,
        "return_judged": judged,
        "return_total": sum(1 for w in targets if is_content(w, dictionary)),
    }
    return problems, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    content = os.path.join(os.path.abspath(args.root), "content")

    pack = read(os.path.join(content, "pack.json"))
    order = None
    spine = os.path.join(content, "plan", "spine.json")
    if os.path.exists(spine):
        try:
            order = [s["id"] for s in read(spine)]
        except (IOError, ValueError, KeyError):
            order = None

    problems, stats = check(pack, order)
    lines = [
        u"stories    %d" % stats.get("stories", 0),
        u"running    %s words" % format(stats.get("running_words", 0), ","),
        u"taught     %d words, median %d encounters, %d reach ten"
        % (stats.get("vocabulary", 0), stats.get("median_encounters", 0),
           stats.get("reach_ten", 0)),
    ]
    judged, total = stats.get("return_judged", 0), stats.get("return_total", 0)
    if judged < total:
        lines.append(
            u"return     %d of %d declared words judged - the rest need %d stories "
            u"after them and the course is not that long yet"
            % (judged, total, RETURN_WINDOW))
    if stats.get("one_scene"):
        lines.append(u"one-scene  %d word(s) exempt from return" % stats["one_scene"])
    for p in problems:
        lines.append(u"PROBLEM: %s" % p)
    lines.append(u"schedule   %s" % (u"clean" if not problems
                                     else u"%d PROBLEM(S)" % len(problems)))

    io.open(os.path.join(content, "plan", "schedule-report.txt"), "w",
            encoding="utf-8").write(NEWLINE.join(lines) + NEWLINE)
    for l in lines:
        try:
            print(l)
        except UnicodeEncodeError:
            print(l.encode("ascii", "replace").decode("ascii"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
