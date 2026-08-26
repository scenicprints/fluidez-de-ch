# -*- coding: utf-8 -*-
"""Checks the course while it is being written, and says where it stands.

Ported from es-ni's stage.py. It exists for the same reason: 192 stories land
a few at a time across many sessions, and without one command that reports the
truth, the plan and the content drift until nobody knows what is left.

    python .github/scripts/stage.py --root .

It never publishes anything. It rewrites content/plan/PROGRESS.md on every run
so that file cannot go stale, and nobody writes it by hand.

What it checks, deliberately in this order:

  * the SHAPE of every story: it is on the spine, it has a warm-up and
    sentences, every sentence has both halves, ids are not duplicated.
  * the SWISS of every story, by handing the whole thing to dialect.py.
  * the DICTIONARY debt: which words the stories use that nothing defines yet,
    written to plan/needs-entry.txt.

What it deliberately does NOT check yet is the recycling schedule, because
coverage and density count how often a word reappears and that needs forms.py
to know spricht and sprach are the same word. Until then the numbers would be
arithmetic on noise. That is written down in NEXT.md too.
"""
import argparse, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dialect  # noqa: E402
import verbs as verbs_gate  # noqa: E402
import forms as morphology  # noqa: E402
import schedule as sched    # noqa: E402

NEWLINE = chr(10)
WORD = re.compile(u"[^\\W\\d_]+", re.UNICODE)
PHASES = [u"Landing", u"Settling In", u"Making Friends", u"Getting About",
          u"Close to the Heart", u"Hard Things", u"Sounding Swiss", u"Belonging"]


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def words_of(text):
    return [w.lower() for w in WORD.findall(text or u"")]


def check_story(body, spine_ids, problems):
    """A story has to be findable, complete, and shaped like a story."""
    sid = body.get("id") or u"?"
    if sid not in spine_ids:
        problems.append(u"%s is not on the spine" % sid)
    wu = body.get("wu") or body.get("warmup") or []
    sn = body.get("sn") or body.get("sentences") or []
    if not sn:
        problems.append(u"%s has no sentences" % sid)
    if not wu:
        problems.append(u"%s has no warm-up" % sid)
    if len(wu) > 12:
        problems.append(u"%s claims %d warm-up words, the ceiling is 12" % (sid, len(wu)))
    for i, s in enumerate(sn, 1):
        if not (s.get("s") or s.get("es")):
            problems.append(u"%s sentence %d has no German" % (sid, i))
        if not (s.get("e") or s.get("en")):
            problems.append(u"%s sentence %d has no English" % (sid, i))
    if body.get("ph") is None and body.get("phase") is None:
        problems.append(u"%s does not say which phase it is in" % sid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    content = os.path.join(root, "content")

    spine = read(os.path.join(content, "plan", "spine.json"))
    spine_ids = [x["id"] for x in spine]
    by_id = dict((x["id"], x) for x in spine)

    lessons_dir = os.path.join(content, "lessons")
    written, problems = [], []
    if os.path.isdir(lessons_dir):
        for name in sorted(os.listdir(lessons_dir)):
            if not name.endswith(".json"):
                continue
            try:
                body = read(os.path.join(lessons_dir, name))
            except ValueError as e:
                problems.append(u"%s is not valid JSON (%s)" % (name, e))
                continue
            check_story(body, spine_ids, problems)
            written.append(body)

    seen = {}
    for b in written:
        seen.setdefault(b.get("id"), []).append(b)
    for sid, rows in seen.items():
        if len(rows) > 1:
            problems.append(u"%s is written %d times" % (sid, len(rows)))

    # What the stories use that the dictionary does not define yet.
    dict_path = os.path.join(content, "dictionary", "core.json")
    known = set()
    if os.path.exists(dict_path):
        known = set(k.lower() for k in read(dict_path).keys())

    # Every stated verb form, checked for holes and for words the course does
    # not teach. Read before the Swiss gate runs so its forms go through that
    # gate too, in the same pass as the stories.
    verbs_path = os.path.join(content, "verbs.json")
    verbs_doc, verbs_count = None, 0
    if os.path.exists(verbs_path):
        try:
            verbs_doc = read(verbs_path)
        except ValueError as e:
            problems.append(u"verbs.json is not valid JSON (%s)" % e)
        if verbs_doc is not None:
            vp, vw, verbs_count = verbs_gate.check(verbs_doc, known)
            problems.extend(vp)

    # Is it Swiss? The whole thing goes through the same gate the build uses,
    # so nothing can be true here and false at publish time.
    allow_path = os.path.join(content, "dialect-allow.json")
    allow = read(allow_path) if os.path.exists(allow_path) else {}
    dialect_problems, dialect_warnings, swiss_hits = dialect.check(
        {"lessons": written, "verbs": verbs_doc}, allow)
    for where, word, why, text in dialect_problems:
        problems.append(u"%s says %r - %s" % (where, word, why))
    used, needs = set(), {}
    for b in written:
        for s in (b.get("sn") or []):
            for w in words_of(s.get("s") or u""):
                used.add(w)
                if w not in known:
                    needs[w] = needs.get(w, 0) + 1
    plan_dir = os.path.join(content, "plan")
    if not os.path.isdir(plan_dir):
        os.makedirs(plan_dir)
    io.open(os.path.join(plan_dir, "needs-entry.txt"), "w", encoding="utf-8").write(
        NEWLINE.join(u"%-24s %d" % (w, n)
                     for w, n in sorted(needs.items(), key=lambda x: -x[1])) + NEWLINE)

    # PROGRESS.md, rewritten every run so it can never be stale.
    done = set(b.get("id") for b in written)
    lines = [u"# Progress", u"",
             u"Written by `stage.py`. Do not edit by hand.", u"",
             u"**%d of %d stories written.**" % (len(done), len(spine)), u"",
             u"| Phase | | Written | Total |", u"|---|---|---|---|"]
    for p in range(8):
        ids = [x["id"] for x in spine if x["phase"] == p]
        lines.append(u"| %d | %s | %d | %d |"
                     % (p, PHASES[p], len([i for i in ids if i in done]), len(ids)))
    nxt = [i for i in spine_ids if i not in done][:8]
    lines += [u"", u"## Next to write", u""]
    for i in nxt:
        lines.append(u"- `%s` **%s** - %s" % (i, by_id[i]["title"], by_id[i]["desc"]))
    io.open(os.path.join(plan_dir, "PROGRESS.md"), "w", encoding="utf-8").write(
        NEWLINE.join(lines) + NEWLINE)

    # How much of the page a reader can actually tap. This is the number
    # forms.py exists to move, and it belongs in the same report as the rest.
    corpus = [s.get("s") or u"" for b in written for s in (b.get("sn") or [])]
    ov_path = os.path.join(content, "dictionary", "forms-overrides.json")
    overrides = read(ov_path) if os.path.exists(ov_path) else {}
    word_forms, ambiguous, _seen = morphology.build(
        dict((k, v) for k, v in
             (read(dict_path).items() if os.path.exists(dict_path) else [])),
        corpus, verbs_doc or {}, overrides)
    corpus_words = [w for t in corpus for w in morphology.tokens(t)]
    tappable = sum(1 for w in corpus_words
                   if w in word_forms or w.lower() in word_forms
                   or w.lower() in known)

    # The recycling quota, run against a pack assembled in memory from what is
    # written so far - so it says the same thing here as it will at publish.
    sched_problems, sched_stats = sched.check(
        {"dictionary": read(dict_path) if os.path.exists(dict_path) else {},
         "forms": word_forms, "lessons": written, "verbs": verbs_doc or {}},
        spine_ids)
    problems.extend(sched_problems)

    report = [
        u"planned    %d stories across 8 phases" % len(spine),
        u"written    %d" % len(done),
        u"dictionary %d words defined, %d used in stories with no entry"
        % (len(known), len(needs)),
        u"swiss      %d Helvetisms in use, %d warning(s)"
        % (swiss_hits, len(dialect_warnings)),
        u"verbs      %d stated" % verbs_count,
        u"forms      %d mapped, %d ambiguous, %.1f%% of the page tappable"
        % (len(word_forms), len(ambiguous),
           100.0 * tappable / max(1, len(corpus_words))),
        u"schedule   median %d encounters, %d words reach ten"
        % (sched_stats.get("median_encounters", 0), sched_stats.get("reach_ten", 0)),
    ]
    for p in problems[:25]:
        report.append(u"PROBLEM: %s" % p)
    if len(problems) > 25:
        report.append(u"PROBLEM: ... and %d more" % (len(problems) - 25))
    if not problems:
        report.append(u"shape      clean")

    io.open(os.path.join(plan_dir, "stage-report.txt"), "w",
            encoding="utf-8").write(NEWLINE.join(report) + NEWLINE)
    for line in report:
        try:
            print(line)
        except UnicodeEncodeError:
            print(line.encode("ascii", "replace").decode("ascii"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
