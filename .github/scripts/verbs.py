# -*- coding: utf-8 -*-
"""The verb gate. Is every form stated, and is every verb one the course teaches?

There is no gate on verbs.json in either course today, and that is how es-ni's
Verb Trainer taught "cerro" and "perdo" for years without anybody noticing: the
app's conjugate() silently falls back to the regular table whenever an irregular
is missing a tense, so a hole in the data does not throw, it just teaches the
wrong thing quietly.

German removes that failure mode by construction - the principal-parts drill
never calls conjugate() - but it replaces it with a different one. Every form in
this file is stated by hand, so a field left out is a form nobody wrote, and a
field guessed at is worse than a field missing. "er sprecht" is exactly the
mistake the learner already makes; handing it back as the right answer is the
one outcome worse than having no trainer.

Two rules:

  1. EVERY REQUIRED FIELD IS PRESENT AND STATED. en, pres3, pres2, past3, pp
     and aux, on every verb. aux is hat or ist and nothing else. A prefix comes
     with a sep, and a separable verb writes its pres3 separated.
  2. EVERY DRILLED VERB IS A LEMMA THE COURSE TEACHES. This is the pattern
     trigger lesson: es-ni shipped two patterns and sixteen mascot lines that
     could never fire, because they keyed on words nothing in the course used.
     A drill on a verb no story contains is a flashcard, and flashcards are the
     thing this app exists not to be.

    python .github/scripts/verbs.py content/verbs.json content/dictionary/core.json
"""
import io, json, os, sys

NEWLINE = chr(10)
REQUIRED = ["en", "pres3", "pres2", "past3", "pp", "aux"]
OPTIONAL = ["imp", "pre", "sep", "k2"]
AUX = ("hat", "ist")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def check(doc, known_lemmas=None):
    """Returns (problems, warnings, verb_count).

    known_lemmas is the dictionary. Pass None or an empty set while the course
    has no words yet and the membership rule downgrades to a warning - it is the
    only thing here that depends on content existing, and blocking an empty
    course from having a verb file would just mean nobody writes the file.
    """
    problems, warnings = [], []
    if not isinstance(doc, dict):
        return [u"verbs.json is not an object"], [], 0

    kind = doc.get("kind")
    if kind != "principal-parts":
        problems.append(u"kind is %r, this course is principal-parts" % kind)

    table = doc.get("verbs") or {}
    drill = doc.get("drill") or []
    for name in drill:
        if name not in table:
            problems.append(u"drill lists %s, which has no entry" % name)

    for name in sorted(table.keys()):
        if name.startswith(u"_"):
            continue                      # notes, not verbs
        v = table[name]
        if not isinstance(v, dict):
            problems.append(u"%s is not an object" % name)
            continue

        for field in REQUIRED:
            got = v.get(field)
            if not isinstance(got, str) or not got.strip():
                problems.append(u"%s has no %s -- every form is stated, none is derived"
                                % (name, field))

        if v.get("aux") not in AUX and v.get("aux") is not None:
            problems.append(u"%s says aux %r, it is hat or ist" % (name, v.get("aux")))

        for field in v.keys():
            if field not in REQUIRED and field not in OPTIONAL:
                warnings.append(u"%s carries an unknown field %r" % (name, field))

        # A prefix and whether it comes off travel together: the drill asks the
        # question of BOTH kinds, so knowing one without the other is useless.
        pre, sep = v.get("pre"), v.get("sep")
        if pre and not isinstance(sep, bool):
            problems.append(u"%s has the prefix %r but does not say if it separates" % (name, pre))
        if isinstance(sep, bool) and not pre:
            problems.append(u"%s says sep but names no prefix" % name)
        if pre and not name.startswith(pre):
            problems.append(u"%s does not start with its own prefix %r" % (name, pre))

        pres3 = v.get("pres3") or u""
        if pre and sep is True:
            # umsteigen -> "steigt um". Written joined, the drill cannot build
            # the wrong option and the stranding never shows on the card.
            if not pres3.endswith(u" " + pre):
                problems.append(u"%s separates, so its pres3 is written %r, not %r"
                                % (name, u"<stem> " + pre, pres3))
        if pre and sep is False:
            if not pres3.startswith(pre):
                problems.append(u"%s does not separate, so its pres3 keeps the prefix in front"
                                % name)

        # A form that equals another form of the same verb makes a card with two
        # right answers on it. umarmen genuinely has pp == pres3, so this is a
        # warning rather than a failure.
        forms = [v.get(f) for f in ("pres3", "pres2", "past3", "pp") if v.get(f)]
        if len(set(forms)) != len(forms):
            warnings.append(u"%s has two parts spelled the same" % name)

    names = [n for n in table.keys() if not n.startswith(u"_")]
    if known_lemmas:
        for name in sorted(names):
            if name.lower() not in known_lemmas:
                problems.append(u"%s is drilled but the course teaches no such word" % name)
    elif names:
        warnings.append(u"%d verb(s) unchecked -- the dictionary is still empty" % len(names))

    return problems, warnings, len(names)


def main(verbs_path, dict_path=None):
    doc = read(verbs_path)
    known = set()
    if dict_path and os.path.exists(dict_path):
        known = set(k.lower() for k in read(dict_path).keys())
    problems, warnings, n = check(doc, known)

    lines = []
    for w in warnings:
        lines.append(u"WARNING: %s" % w)
    for p in problems:
        lines.append(u"PROBLEM: %s" % p)
    lines.append(u"verbs    %d stated" % n)
    lines.append(u"verbs    %s" % (u"clean -- every form is written down"
                                   if not problems else u"%d PROBLEM(S)" % len(problems)))
    # Console output here is cp1252 and mangles umlauts. Write the report to a
    # file and print whatever survives.
    io.open(os.path.join(os.path.dirname(verbs_path) or ".", "verbs-report.txt"),
            "w", encoding="utf-8").write(NEWLINE.join(lines) + NEWLINE)
    for l in lines:
        try:
            print(l)
        except UnicodeEncodeError:
            print(l.encode("ascii", "replace").decode("ascii"))
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: verbs.py content/verbs.json [content/dictionary/core.json]")
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
