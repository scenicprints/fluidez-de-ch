# -*- coding: utf-8 -*-
"""Bundles content/pack.json from the manifest, and runs every gate first.

    python .github/scripts/build-pack.py --root . --language de-ch --version 20260825-1900+phase0

Two rules, both inherited from es-ni:

  * NOTHING REACHES THE PACK UNLESS THE MANIFEST NAMES IT. A file sitting on
    disk that nobody lists does not exist. That is what makes publishing an
    edit to one list rather than a hunt.
  * NOTHING REACHES THE PACK AT ALL IF A GATE FIRES. The Swiss gate over every
    line, the verb gate over every stated form, and a check that every pattern
    trigger is a lemma the course can teach — es-ni shipped two patterns that
    could never unlock because nothing checked that last one.

Two things this does that es-ni's does not, both because German needed them:
it carries `verbs` and `emergency` through, and it ships **no `ui` block**.
The German course's interface is English, so `t()` falls back to the app's own
EN table and there is nothing here to keep in step with it.
"""
import argparse, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dialect          # noqa: E402
import verbs as vgate   # noqa: E402
import forms as morphology  # noqa: E402
import schedule as sched    # noqa: E402

NEWLINE = chr(10)


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--version", default=None)
    # CI derives the code from the repo name, so a new course needs no edit here.
    ap.add_argument("--language", default=None, help="course code, e.g. de-ch")
    args = ap.parse_args()
    content = os.path.join(os.path.abspath(args.root), "content")

    def rd(rel):
        return read(os.path.join(content, *rel.split("/")))

    m = rd("manifest.json")

    dictionary = {}
    for path in m.get("dictionary") or []:
        dictionary.update(rd(path))

    patterns = []
    for path in m.get("patterns") or []:
        patterns.extend(rd(path))

    lessons = [rd(row["path"]) for row in m.get("lessons") or []]
    scenarios = [rd(row["path"]) for row in m.get("scenarios") or []]
    verbs_doc = rd(m["verbs"]) if m.get("verbs") else None
    if verbs_doc:
        verbs_doc.pop("_", None)          # the schema notes stay in the repo
    emergency = rd(m["emergency"]) if m.get("emergency") else None

    # Every inflected form that ACTUALLY OCCURS, mapped back to its entry.
    # Without this the reader is at 53% of the words on the page tappable and
    # the memory of every verb is split across its own principal parts.
    corpus = []
    for l in lessons:
        for sn in l.get("sn") or []:
            corpus.append(sn.get("s") or u"")
    for sc in scenarios:
        for st in sc.get("steps") or []:
            corpus.append(st.get("es") or u"")
            for o in st.get("options") or []:
                corpus.append(o.get("es") or u"")
    for g in emergency or []:
        for ph in g.get("phrases") or []:
            corpus.append(ph.get("es") or u"")

    dead = []
    ov_path = os.path.join(content, "dictionary", "forms-overrides.json")
    overrides = read(ov_path) if os.path.exists(ov_path) else {}
    for f, lemma in overrides.items():
        if not f.startswith("_") and lemma is not None and lemma not in dictionary:
            dead.append(u"forms-overrides: %r points at %r, which is not an entry"
                        % (f, lemma))

    word_forms, ambiguous, seen_words = morphology.build(
        dictionary, corpus, verbs_doc or {}, overrides)

    # Counted the way the app resolves a word: exact spelling first, then
    # lower-cased. Counting only the exact hit understates it by nineteen
    # points, because every sentence-initial capital looks like a miss.
    def resolves(w):
        return (w in dictionary or w in word_forms
                or w.lower() in dictionary or w.lower() in word_forms)
    corpus_words = [w for t in corpus for w in morphology.tokens(t)]
    tappable_pct = 100.0 * sum(1 for w in corpus_words if resolves(w)) / max(1, len(corpus_words))

    pack = {
        "version": None,
        "language": args.language or "de-ch",
        "features": m.get("features"),
        "speech": m.get("speech"),
        "mascot": m.get("mascot"),
        "icons": m.get("icons"),
        "phases": m.get("phases"),
        "dictionary": dictionary,
        "forms": word_forms,
        "patterns": patterns,
        "lessons": lessons,
        "scenarios": scenarios,
        "verbs": verbs_doc,
        "emergency": emergency,
        "momo": [],
    }

    allow_path = os.path.join(content, "dialect-allow.json")
    allow = read(allow_path) if os.path.exists(allow_path) else {}
    problems, warnings, hits = dialect.check(pack, allow)
    vp, vw, vcount = vgate.check(verbs_doc or {},
                                 set(k.lower() for k in dictionary))

    for p in patterns:
        for t in p.get("trigger") or []:
            if t not in dictionary:
                dead.append(u"pattern %s: trigger %r has no entry, so it can "
                            u"never unlock" % (p.get("id"), t))

    # The recycling quota, over the pack as it now stands. Coverage and density
    # are judged from the first story; return abstains until a word has
    # RETURN_WINDOW stories after it, so a half-written course never false-alarms.
    spine_path = os.path.join(content, "plan", "spine.json")
    order = None
    if os.path.exists(spine_path):
        try:
            order = [x["id"] for x in read(spine_path)]
        except (IOError, ValueError, KeyError):
            order = None
    sched_problems, sched_stats = sched.check(pack, order)

    lines = []
    for w in warnings:
        lines.append(u"WARNING: %s says %r - %s" % (w[0], w[1], w[2]))
    for w in vw:
        lines.append(u"WARNING: %s" % w)
    for p in problems:
        lines.append(u"PROBLEM: %s says %r - %s" % (p[0], p[1], p[2]))
    for p in vp + dead + sched_problems:
        lines.append(u"PROBLEM: %s" % p)

    fatal = len(problems) + len(vp) + len(dead) + len(sched_problems)
    lines += [
        u"lessons    %d" % len(lessons),
        u"scenes     %d" % len(scenarios),
        u"patterns   %d" % len(patterns),
        u"dictionary %d" % len(dictionary),
        u"verbs      %d" % vcount,
        u"emergency  %d groups, %d phrases"
        % (len(emergency or []),
           sum(len(g.get("phrases") or []) for g in (emergency or []))),
        u"forms      %d inflections mapped, %d dropped as ambiguous"
        % (len(word_forms), len(ambiguous)),
        u"tappable   %.1f%% of the words on the page" % tappable_pct,
        u"swiss      %d Helvetisms in use" % hits,
        u"schedule   median %d encounters, %d words reach ten"
        % (sched_stats.get("median_encounters", 0), sched_stats.get("reach_ten", 0)),
        u"build      %s" % (u"clean" if not fatal
                            else u"%d PROBLEM(S), nothing written" % fatal),
    ]
    io.open(os.path.join(content, "build-report.txt"), "w",
            encoding="utf-8").write(NEWLINE.join(lines) + NEWLINE)
    for l in lines:
        try:
            print(l)
        except UnicodeEncodeError:
            print(l.encode("ascii", "replace").decode("ascii"))

    if fatal:
        return 1

    stamp = args.version or read(os.path.join(content, "version.json")).get("version")
    pack["version"] = stamp
    io.open(os.path.join(content, "pack.json"), "w", encoding="utf-8").write(
        json.dumps(pack, ensure_ascii=False, indent=1) + NEWLINE)
    io.open(os.path.join(content, "version.json"), "w", encoding="utf-8").write(
        json.dumps({"version": stamp, "lessons": len(lessons),
                    "scenarios": len(scenarios), "words": len(dictionary)},
                   ensure_ascii=False) + NEWLINE)
    print("pack written, version %s" % stamp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
