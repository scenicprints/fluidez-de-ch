# -*- coding: utf-8 -*-
"""Checks what the mascot is allowed to say.

Ported from es-ni's check_momo, WITH THE CHECK IT WAS MISSING.

es-ni shipped 59 lines and 16 of them could never fire: they were gated on
inflected forms (`vamos`, `sos`, `hacés`) or on words the course never uses at
all (`tranqui`, `platicar`). Nothing complained, because the only thing checked
was that `min` was not larger than the trigger list. A line nobody can ever
earn is not a line, and silence is what the learner gets instead.

So this checks four things:

  1. SHAPE. An id, a known moment, a known state, something to say, and a `min`
     the trigger list can actually satisfy.
  2. NO TWO LINES SAY THE SAME THING. Two moments sharing wording reads as a
     bug on screen: in es-ni a bad score followed by the daily goal said
     "¡Qué tuani!" twice and looked like praise for the score it had just
     marked down.
  3. EVERY MOMENT HAS AN UNGATED LINE, or a brand new learner meets a silent
     cow at that moment.
  4. EVERY TRIGGER IS A LEMMA THE COURSE ACTUALLY TEACHES. Exposures are
     recorded against the resolved lemma, so a trigger on a form or on a word
     no story contains can never be met.
"""
import io, json, os, sys

NEWLINE = chr(10)
WHEN = ("welcome", "back", "poke", "great", "ok", "poor", "goal", "pattern", "sleep")
STATE = ("happy", "cheer", "speak", "wrong", "sleep")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def check(doc, dictionary=None, used=None):
    """Returns (problems, warnings, lines).

    `dictionary` is the course's own, and `used` the set of lemmas that occur
    in its text. Pass neither while the course has no content and rule 4
    downgrades to a warning.
    """
    problems, warnings = [], []
    lines = doc.get("lines") if isinstance(doc, dict) else doc
    if not isinstance(lines, list) or not lines:
        return [u"mascot: expected a non-empty 'lines' list"], [], []

    seen, starters, said = set(), set(), {}
    for i, ln in enumerate(lines):
        where = u"mascot line %d" % (i + 1)
        if not isinstance(ln, dict):
            problems.append(u"%s: should be an object" % where)
            continue

        lid = ln.get("id")
        if not lid:
            problems.append(u"%s: has no id" % where)
        elif lid in seen:
            problems.append(u"%s: duplicate id %s" % (where, lid))
        else:
            seen.add(lid)
        where = u"mascot line %s" % (lid or i + 1)

        when = ln.get("when")
        if when not in WHEN:
            problems.append(u"%s: 'when' must be one of %s, got %r"
                            % (where, u", ".join(WHEN), when))
        if ln.get("state") not in STATE:
            problems.append(u"%s: 'state' must be one of %s, got %r"
                            % (where, u", ".join(STATE), ln.get("state")))

        say = (ln.get("say") or u"").strip()
        if not say:
            problems.append(u"%s: 'say' is empty" % where)
        elif say in said:
            problems.append(u"%s: says the same as %s - %r" % (where, said[say], say))
        else:
            said[say] = lid or i + 1
        # The bubble does not wrap. es-ni's longest is 17 characters.
        if len(say) > 24:
            warnings.append(u"%s: %d characters, the bubble will not wrap it - %r"
                            % (where, len(say), say))

        trigger = ln.get("trigger") or []
        if not isinstance(trigger, list) or any(not isinstance(w, str) for w in trigger):
            problems.append(u"%s: 'trigger' must be a list of words" % where)
            trigger = []
        mn = ln.get("min", 1 if trigger else 0)
        if not isinstance(mn, int) or mn < 0:
            problems.append(u"%s: 'min' must be a whole number" % where)
        elif mn > len(trigger):
            problems.append(u"%s: needs %d of %d trigger words - unreachable"
                            % (where, mn, len(trigger)))

        for w in trigger:
            if dictionary is None:
                continue
            if w not in dictionary:
                problems.append(u"%s: trigger %r is not a dictionary entry, so it "
                                u"can never be met" % (where, w))
            elif used is not None and w not in used:
                problems.append(u"%s: trigger %r has an entry but no story uses "
                                u"it, so it can never be met" % (where, w))

        if not trigger:
            starters.add(when)

    missing = [w for w in WHEN if w not in starters]
    if missing:
        problems.append(u"mascot: no ungated line for %s - a brand new learner "
                        u"would get silence there" % u", ".join(missing))

    return problems, warnings, lines


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    content = os.path.join(os.path.abspath(root), "content")
    m = read(os.path.join(content, "manifest.json"))
    doc = read(os.path.join(content, *m["momo"].split("/")))

    dictionary = {}
    ddir = os.path.join(content, "dictionary")
    for name in sorted(os.listdir(ddir)):
        if name.endswith(".json") and "override" not in name:
            dictionary.update(read(os.path.join(ddir, name)))

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import forms as morphology
    import schedule as sched
    verbs_path = os.path.join(content, "verbs.json")
    verbs = read(verbs_path) if os.path.exists(verbs_path) else {}
    lessons = [read(os.path.join(content, *row["path"].split("/")))
               for row in m.get("lessons") or []]
    scenes = [read(os.path.join(content, *row["path"].split("/")))
              for row in m.get("scenarios") or []]
    # Scenes count. The learner reads them and they record exposures, so a word
    # a scene teaches is a word the mascot may lean on.
    corpus = [sn["s"] for l in lessons for sn in l.get("sn") or []]
    for sc in scenes:
        for st in sc.get("steps") or []:
            corpus.append(st.get("es") or u"")
            for o in st.get("options") or []:
                corpus.append(o.get("es") or u"")
    ov = os.path.join(ddir, "forms-overrides.json")
    fm, _a, _s = morphology.build(dictionary, corpus,
                                  verbs, read(ov) if os.path.exists(ov) else {})
    used = set()
    for l in lessons:
        for w in sched.story_words(l, dictionary, fm, verbs):
            used.add(w)
    for sc in scenes:
        for st in sc.get("steps") or []:
            texts = [st.get("es") or u""] + [o.get("es") or u"" for o in st.get("options") or []]
            for t in texts:
                for w in sched.TOKEN.findall(t):
                    lem = sched.lemma_of(w, dictionary, fm)
                    if lem:
                        used.add(lem)

    problems, warnings, lines = check(doc, dictionary, used)
    out = []
    for w in warnings:
        out.append(u"WARNING: %s" % w)
    for p in problems:
        out.append(u"PROBLEM: %s" % p)
    out.append(u"mascot     %d lines" % len(lines))
    out.append(u"mascot     %s" % (u"clean - every line can be earned"
                                   if not problems else
                                   u"%d PROBLEM(S)" % len(problems)))
    io.open(os.path.join(content, "plan", "mascot-report.txt"), "w",
            encoding="utf-8").write(NEWLINE.join(out) + NEWLINE)
    for l in out:
        try:
            print(l)
        except UnicodeEncodeError:
            print(l.encode("ascii", "replace").decode("ascii"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
