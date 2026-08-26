# -*- coding: utf-8 -*-
"""The Swiss gate. Is this actually Swiss Standard German?

Ported in spirit from es-ni's dialect.py, which exists because a tu form here
and a Mexicanism there is invisible in any single lesson and obvious across a
hundred thousand words. The same is true of Fahrrad and Krankenhaus.

Three rules, in order of how absolute they are:

  1. NO ESZETT. Switzerland abolished it; ss always. This is not a preference,
     it is orthography, and it is the one rule with no exceptions at all.
  2. NO GERMANISM where a Helvetism is the Swiss standard. The list lives in
     helvetisms.json WITH SOURCES, because "trust the model" does not survive
     148,000 words. Anything not attested is a warning, never a failure.
  3. ONE SPELLING for every pinned dialect word. No dialect orthography is
     objectively correct, so ours becomes the course's, and Sali appearing
     three ways reads as sloppy rather than authentic.

A story that names the German word IN ORDER TO TEACH THE CONTRAST is exempt by
story id, never by word: p0-06 says "Weggli, not Broetchen" and is right to.
Exempting the word globally would let a real slip through, which is exactly the
lesson es-ni's dialect-allow.json already paid for.

    python .github/scripts/dialect.py content/pack.json
"""
import io, json, os, re, sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LIST = os.path.join(HERE, "helvetisms.json")
NEWLINE = chr(10)
ESZETT = u"ß"

PUNCT = re.compile(u"[.,;:!?\"'()«»“”—–…]")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def fold(s):
    """Umlauts to their two-letter spelling, so a list written in plain ASCII
    matches text written properly. Fahrrad has no umlaut but Moehre does, and
    the list must not depend on which way somebody typed it."""
    s = s.lower()
    for a, b in ((u"ä", u"ae"), (u"ö", u"oe"), (u"ü", u"ue"), (ESZETT, u"ss")):
        s = s.replace(a, b)
    return u"".join(c for c in unicodedata.normalize("NFD", s)
                    if not unicodedata.combining(c))


def words_of(text):
    return [w for w in PUNCT.sub(u" ", text or u"").split() if w]


def collect(pack):
    """Every line of German in the pack, with where it came from.

    Lessons, scenes, momo lines AND the interface. The interface is included
    from the start on purpose: es-ni shipped its labels ungated because
    collect() predated them, and the interface is the text a learner reads
    most - every screen, every day, for months.
    """
    out = []
    # Every line carries its own position, so the allow-list can exempt ONE
    # line rather than a whole story. It used to be "lesson p0-06" for all
    # ninety-odd sentences in p0-06, which meant exempting the one line that
    # teaches Weggli-not-Broetchen also stopped checking the other ninety.
    # An entry with no position still exempts the whole thing, so the coarse
    # form keeps working where it is genuinely wanted.
    for l in pack.get("lessons") or []:
        for i, sn in enumerate(l.get("sn") or l.get("sentences") or [], 1):
            out.append((u"lesson %s #%d" % (l.get("id"), i),
                        sn.get("s") or sn.get("es") or u""))
    for s in pack.get("scenarios") or []:
        for si, st in enumerate(s.get("steps") or [], 1):
            out.append((u"scene %s step %d" % (s.get("id"), si), st.get("es") or u""))
            for oi, o in enumerate(st.get("options") or [], 1):
                out.append((u"scene %s option %d.%d" % (s.get("id"), si, oi),
                            o.get("es") or u""))
    for m in pack.get("momo") or []:
        out.append((u"momo %s" % m.get("id"), m.get("say") or u""))
    # The emergency phrasebook. It was outside the gate at first, which is the
    # worst possible place for a hole: it is the one screen read in a hurry by
    # somebody who cannot yet check the words, and Spital-not-Krankenhaus would
    # have sailed straight through it.
    for i, group in enumerate(pack.get("emergency") or pack.get("emergencyData") or []):
        for ph in group.get("phrases") or []:
            out.append((u"emergency %s" % (group.get("title") or i), ph.get("es") or u""))
    # And every stated verb form. verbs.py checks that they are all written
    # down; this checks that what is written down is Swiss.
    verbs = pack.get("verbs") or {}
    for name, v in sorted((verbs.get("verbs") or {}).items()):
        if name.startswith(u"_") or not isinstance(v, dict):
            continue
        for field in ("pres3", "pres2", "past3", "pp", "imp", "k2"):
            if isinstance(v.get(field), str):
                out.append((u"verb %s" % name, v[field]))
    for key, value in sorted((pack.get("ui") or {}).items()):
        if isinstance(value, str):
            out.append((u"ui %s" % key, value))
    for i, phase in enumerate(pack.get("phases") or []):
        pair = phase if isinstance(phase, list) else [phase.get("name"), phase.get("desc")]
        for part in pair:
            if isinstance(part, str):
                out.append((u"phase %d" % i, part))
    return out


def load_rules(path=None):
    doc = read(path or LIST)
    banned = {}          # folded German word -> (level, the Swiss word, source)
    for row in doc.get("words") or []:
        for bad in row.get("not") or []:
            banned[fold(bad)] = (row.get("level", "fail"), row["say"], row.get("source", "?"))
    # Pinned words are matched on EXACT spelling, lower-cased but with the
    # umlauts intact, because the umlaut IS the difference. Folding these once
    # made the gate reject the correct spelling of Gruezi as a misspelling of
    # itself. Same split es-ni uses for tu forms versus foreign vocabulary.
    pinned_word, pinned_phrase = {}, {}
    for row in doc.get("pinned") or []:
        for v in row.get("variants") or []:
            if v.lower() == row["say"].lower():
                continue
            (pinned_phrase if " " in v else pinned_word)[v.lower()] = row["say"]
    swiss = set(fold(r["say"]) for r in (doc.get("words") or []))
    swiss |= set(fold(r["say"]).split()[0] for r in (doc.get("pinned") or []))
    return banned, pinned_word, pinned_phrase, swiss


def check(pack, allow=None, rules_path=None):
    """Returns (problems, warnings, swiss_count).

    A problem fails the build. A warning is printed and does not.
    """
    allow = allow or {}
    skip_ids = set(allow.get("lines") or [])
    skip_words = set(fold(w) for w in (allow.get("words") or []))
    banned, pinned_word, pinned_phrase, swiss = load_rules(rules_path)

    def exempt(where):
        """An allow entry matches its own line, or every line beneath it.

        "lesson p0-06 #41" exempts one sentence. "lesson p0-06" still exempts
        the whole story, which is what the coarse form is for and what
        dialect_test.py asserts.
        """
        for entry in skip_ids:
            if where == entry or where.startswith(entry + u" "):
                return True
        return False

    problems, warnings, hits = [], [], 0
    for where, text in collect(pack):
        if exempt(where):
            continue

        # 1. The eszett rule, on the raw text, before any folding.
        if ESZETT in (text or u""):
            problems.append((where, ESZETT,
                             u"eszett -- Switzerland does not use it, write ss",
                             text))

        # Multi-word variants have to be looked for in the line: "merci
        # villmal" is never a single token.
        low = (text or u"").lower()
        for bad, good in pinned_phrase.items():
            if bad in low:
                problems.append((where, bad,
                                 u"write it %s -- one spelling per pinned word" % good,
                                 text))

        for w in words_of(text):
            f = fold(w)
            if f in swiss:
                hits += 1
            if f in skip_words:
                continue
            if w.lower() in pinned_word:
                problems.append((where, w,
                                 u"spell it %s -- one spelling per pinned word"
                                 % pinned_word[w.lower()], text))
                continue
            hit = banned.get(f)
            if hit:
                level, say, source = hit
                why = u"German, not Swiss -- use %s (%s)" % (say, source)
                (problems if level == "fail" else warnings).append((where, w, why, text))
    return problems, warnings, hits


def main(pack_path, allow_path=None):
    pack = read(pack_path)
    allow = {}
    if allow_path and os.path.exists(allow_path):
        allow = read(allow_path) or {}
    problems, warnings, hits = check(pack, allow)

    lines = []
    for where, word, why, text in warnings:
        lines.append(u"WARNING: %s says %r - %s: %s" % (where, word, why, text[:70]))
    for where, word, why, text in problems:
        lines.append(u"PROBLEM: %s says %r - %s: %s" % (where, word, why, text[:70]))
    lines.append(u"checked  %d lines of German" % len(collect(pack)))
    lines.append(u"swiss    %d Helvetisms in use" % hits)
    lines.append(u"dialect  %s" % (u"clean -- every line is Swiss"
                                   if not problems else
                                   u"%d PROBLEM(S)" % len(problems)))
    # Console output here is cp1252 and mangles umlauts, which is written down
    # in the handoff. Write the report to a file and print what survives.
    io.open(os.path.join(os.path.dirname(pack_path) or ".", "dialect-report.txt"),
            "w", encoding="utf-8").write(NEWLINE.join(lines) + NEWLINE)
    for l in lines:
        try:
            print(l)
        except UnicodeEncodeError:
            print(l.encode("ascii", "replace").decode("ascii"))
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: dialect.py content/pack.json [content/dialect-allow.json]")
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
