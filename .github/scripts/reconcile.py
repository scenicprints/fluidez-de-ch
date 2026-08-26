# -*- coding: utf-8 -*-
"""Rewrites every warm-up to the words its story actually teaches.

    python .github/scripts/reconcile.py --root .

A warm-up is a CLAIM: these are the words this lesson is going to hammer.
Written by hand the claim drifts - 46% of the warm-up words in the course es-ni
replaced never appeared in the lesson they warmed up for. So it is not written
by hand. This derives it from the text, and the text is the only thing that can
be wrong.

A word is warmed up when all of this is true:

  * the story uses it at least DENSITY_MIN times, so there is context to work
    it out from;
  * it is a content word, not a preposition or an article;
  * it is a dictionary lemma, or nothing can be shown on the card;
  * it is not in BORING - sein, haben, auch, dann - which every story is full
    of and which nobody needs a card for;
  * it comes back later per schedule.py's RETURN rule, or it is a one-scene
    word that this story is most of;
  * and no story in the last GAP stories has already warmed it up.

That last rule was es-ni's hardest-won line. It used to be "no story has EVER
warmed it up", and first-come-first-served meant the early stories claimed
every common word and everything after them starved: 95 of 185 stories ended
with NO warm-up at all. Letting a word be warmed up again twenty-five stories
later is not a duplicate claim - the later story really does hammer it, and
re-teaching a word a month later is spacing, which is the whole point.

---------------------------------------------------------------------------
WHAT GERMAN CHANGES

Counting goes through schedule.story_words, so it inherits both German fixes:
lookups try the exact spelling before the lower-cased one (or no noun is ever
found), and a separable verb counts as one word across its two halves (or
ankommen scores zero in the story that is full of it and could never be warmed
up).

BORING is deliberately SHORTER than es-ni's. Theirs is calibrated against a
finished 185-story course where a card for "hacer" in story 140 teaches
nobody; phase 0 is where gehen, kommen and sagen are genuinely being taught for
the first time, so only the truly structural words are listed. The ordering
below does the rest of the work: a word is ranked by how much of it belongs to
THIS story, so a ubiquitous verb sinks on its own without being banned.
---------------------------------------------------------------------------
"""
import argparse, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import forms as M          # noqa: E402
import schedule as SCH     # noqa: E402

NEWLINE = chr(10)
GAP = 25     # how many stories must pass before a word may be warmed up again
CAP = 12     # the most a single warm-up may show; stage.py enforces the same

# Words every story is full of. Structural rather than teachable: a card for
# "auch" is a card nobody reads, and it pushes out the word the story is about.
# is_content() already drops prepositions, articles, conjunctions,
# contractions, pronouns and numbers, so what is left here is the adverbs and
# the three or four verbs that are in literally every story.
#
# MATCHED ON EXACT SPELLING, not lower-cased. German has pairs where the
# capital is the whole difference: `weg` means gone and belongs here, `der Weg`
# is the way and is what "Wo ist die Post?" is about. Lower-casing the test
# killed Weg along with weg, and Morgen along with morgen. Every entry below is
# lower case, and a German noun is not, so a noun can never match one.
BORING = set(u"""
sein haben werden
nicht auch dann noch schon jetzt immer nie oft wieder sehr ganz fast nur mehr
weniger so hier dort da einfach wirklich vielleicht natürlich trotzdem sonst
etwa kaum genug zusammen weg heute morgen später vorher plötzlich endlich
gerade also anders wohin damit darin dazu davon dabei
gut schlecht klein anders viel wenig alle alles nichts etwas
""".split())

# Dictionary entries that are a form of something else that is ALSO an entry,
# so they are tappable but do not belong on a vocabulary card. German's list is
# short because forms.py resolves rather than duplicates - the one case is the
# possessive `sein`, spelled exactly like the verb.
NOT_A_LEMMA = set(u"möchte".split())


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change and write nothing")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    content = os.path.join(root, "content")

    dictionary = {}
    ddir = os.path.join(content, "dictionary")
    for name in sorted(os.listdir(ddir)):
        if name.endswith(".json") and "override" not in name:
            dictionary.update(read(os.path.join(ddir, name)))

    vpath = os.path.join(content, "verbs.json")
    verbs = read(vpath) if os.path.exists(vpath) else {}
    spine = [s["id"] for s in read(os.path.join(content, "plan", "spine.json"))]

    lessons = {}
    ldir = os.path.join(content, "lessons")
    for name in sorted(os.listdir(ldir)):
        if re.match(u"^p[0-7]-\\d\\d\\.json$", name):
            b = read(os.path.join(ldir, name))
            lessons[b["id"]] = b
    if not lessons:
        print("no stories written yet")
        return 0

    corpus = [sn["s"] for b in lessons.values() for sn in b["sn"]]
    ov_path = os.path.join(ddir, "forms-overrides.json")
    overrides = read(ov_path) if os.path.exists(ov_path) else {}
    # forms.build applies the overrides itself, so this map is the same one the
    # pack ships. Counting without them counts a course nobody reads.
    forms, _amb, _seen = M.build(dictionary, corpus, verbs, overrides)

    counts = dict((sid, SCH.story_words(b, dictionary, forms, verbs))
                  for sid, b in lessons.items())
    order = [s for s in spine if s in lessons]

    total_uses = {}
    for c in counts.values():
        for w, n in c.items():
            total_uses[w] = total_uses.get(w, 0) + n

    changed, before_total = [], sum(len(lessons[s].get("wu") or []) for s in order)

    def own(i, w):
        """How much of everything the course says with this word is said here."""
        return counts[order[i]][w] / float(total_uses.get(w, counts[order[i]][w]))

    def returns(i, w):
        # The same rule schedule.py enforces, both exemptions included.
        later = order[i + 1:]
        if len(later) < SCH.RETURN_WINDOW:
            return True
        if sum(1 for j in later if counts[j].get(w)) >= SCH.RETURN_MIN:
            return True
        return SCH.one_scene(counts[order[i]].get(w, 0), total_uses.get(w, 0))

    def qualifies(i, w, n):
        return (n >= SCH.DENSITY_MIN
                and SCH.is_content(w, dictionary)
                and w in dictionary
                and w not in BORING
                and w not in NOT_A_LEMMA
                and returns(i, w))

    # THE WORD GOES TO THE STORY THAT OWNS IT, not to the first one that
    # qualifies.
    #
    # es-ni assigns in reading order, and the cost of that is written into its
    # own header: the early stories claim every common word and everything
    # after them starves. Here it showed up as "Der See" being refused `See`
    # because p0-03 mentions a lake through a train window six times on the way
    # past, and as "Wo ist die Post?" losing `Weg`. Ranking every candidate by
    # how much of the word belongs to its story, and handing it out best-first,
    # gives the word to the story that is actually about it. GAP still stops a
    # second claim inside twenty-five stories.
    candidates = []
    for i, sid in enumerate(order):
        for w, n in counts[sid].items():
            if qualifies(i, w, n):
                candidates.append((own(i, w), n, i, w))
    candidates.sort(key=lambda x: (-x[0], -x[1], x[3]))

    claimed = {}                       # story index -> [words]
    claims = {}                        # word -> [story indexes that took it]
    for _o, _n, i, w in candidates:
        near = [j for j in claims.get(w, []) if abs(i - j) < GAP]
        if near:
            continue
        if len(claimed.get(i, [])) >= CAP:
            continue
        claimed.setdefault(i, []).append(w)
        claims.setdefault(w, []).append(i)

    for i, sid in enumerate(order):
        b = lessons[sid]
        mine = claimed.get(i, [])
        if not mine:
            # Nothing left to pre-teach is an honest blank, but a story with no
            # unclaimed word of its own should still lead with what it leans on
            # hardest rather than show nothing.
            mine = [w for w, n in counts[sid].items() if qualifies(i, w, n)]
        fresh = sorted(mine, key=lambda w: (-own(i, w), -counts[sid][w], w))[:CAP]
        was = list(b.get("wu") or [])
        if fresh != was:
            changed.append((sid, was, fresh))
        b["wu"] = fresh

        if not args.dry_run:
            io.open(os.path.join(ldir, sid + ".json"), "w", encoding="utf-8").write(
                json.dumps(b, ensure_ascii=False, indent=1) + NEWLINE)

    sizes = [len(lessons[s]["wu"]) for s in order]
    lines = [
        u"warm-ups   %d stories, %d words, median %d, %d with none"
        % (len(sizes), sum(sizes), sorted(sizes)[len(sizes) // 2],
           sum(1 for x in sizes if x == 0)),
        u"was        %d words" % before_total,
        u"changed    %d stor%s" % (len(changed), u"y" if len(changed) == 1 else u"ies"),
    ]
    for sid, old, new in changed:
        gone = [w for w in old if w not in new]
        added = [w for w in new if w not in old]
        if gone or added:
            lines.append(u"  %s  -%s  +%s"
                         % (sid, u",".join(gone) or u"-", u",".join(added) or u"-"))
        else:
            lines.append(u"  %s  reordered" % sid)
    if args.dry_run:
        lines.append(u"(dry run, nothing written)")

    io.open(os.path.join(content, "plan", "reconcile-report.txt"), "w",
            encoding="utf-8").write(NEWLINE.join(lines) + NEWLINE)
    for l in lines:
        try:
            print(l)
        except UnicodeEncodeError:
            print(l.encode("ascii", "replace").decode("ascii"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
