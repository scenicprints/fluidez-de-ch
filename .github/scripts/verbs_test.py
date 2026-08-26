# -*- coding: utf-8 -*-
"""Proves the verb gate fires on holes and stays quiet on a good entry.

This exists for the same reason dialect_test.py does: that gate was written in
ASCII and rejected the correct spelling of Gruezi, the single most important
word in the course, and nobody would have known until content hit it. A gate
nobody has watched fail has not been tested.

    python .github/scripts/verbs_test.py
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verbs  # noqa: E402

NEWLINE = chr(10)

GOOD = {
    u"en": u"to speak", u"pres3": u"spricht", u"pres2": u"sprichst",
    u"past3": u"sprach", u"pp": u"gesprochen", u"aux": u"hat", u"imp": u"sprich",
}
SEP = {
    u"en": u"to change trains", u"pres3": u"steigt um", u"pres2": u"steigst um",
    u"past3": u"stieg um", u"pp": u"umgestiegen", u"aux": u"ist",
    u"pre": u"um", u"sep": True,
}
INSEP = {
    u"en": u"to hug", u"pres3": u"umarmt", u"pres2": u"umarmst",
    u"past3": u"umarmte", u"pp": u"umarmt", u"aux": u"hat",
    u"pre": u"um", u"sep": False,
}
LEMMAS = set([u"sprechen", u"umsteigen", u"umarmen", u"gehen"])


def doc(table, drill=None):
    d = {u"kind": u"principal-parts", u"verbs": table}
    if drill is not None:
        d[u"drill"] = drill
    return d


def without(entry, field):
    out = dict(entry)
    out.pop(field, None)
    return out


def swap(entry, field, value):
    out = dict(entry)
    out[field] = value
    return out


MUST_FAIL = [
    (u"a missing participle", doc({u"sprechen": without(GOOD, u"pp")})),
    (u"a missing du form", doc({u"sprechen": without(GOOD, u"pres2")})),
    (u"a missing auxiliary", doc({u"sprechen": without(GOOD, u"aux")})),
    (u"an empty form", doc({u"sprechen": swap(GOOD, u"past3", u"")})),
    (u"an auxiliary that is neither", doc({u"sprechen": swap(GOOD, u"aux", u"wird")})),
    (u"a prefix with no answer about it", doc({u"umsteigen": without(SEP, u"sep")})),
    (u"sep with no prefix named", doc({u"sprechen": swap(GOOD, u"sep", True)})),
    (u"a separable verb written joined", doc({u"umsteigen": swap(SEP, u"pres3", u"umsteigt")})),
    (u"an inseparable verb written apart", doc({u"umarmen": swap(INSEP, u"pres3", u"armt um")})),
    (u"a prefix the verb does not start with", doc({u"umsteigen": swap(SEP, u"pre", u"an")})),
    (u"drilling a verb with no entry", doc({u"sprechen": GOOD}, [u"sprechen", u"laufen"])),
    (u"the wrong kind of file", {u"kind": u"conjugation", u"verbs": {u"sprechen": GOOD}}),
    (u"a verb the course does not teach", doc({u"schwaetzen": GOOD})),
]

MUST_PASS = [
    (u"a whole strong verb", doc({u"sprechen": GOOD})),
    (u"a separable verb", doc({u"umsteigen": SEP})),
    (u"an inseparable prefix verb", doc({u"umarmen": INSEP})),
    (u"all three together", doc({u"sprechen": GOOD, u"umsteigen": SEP, u"umarmen": INSEP})),
    (u"an empty file", doc({})),
    (u"a note key, which is not a verb", doc({u"_": [u"a comment"], u"sprechen": GOOD})),
    (u"a held-back verb", doc({u"sprechen": GOOD, u"umsteigen": SEP}, [u"sprechen"])),
]

lines, bad = [], 0

for why, d in MUST_FAIL:
    problems, _w, _n = verbs.check(d, LEMMAS)
    if not problems:
        lines.append(u"MISSED  %s went straight through" % why)
        bad += 1
lines.append(u"must fail  %d cases" % len(MUST_FAIL))

for why, d in MUST_PASS:
    problems, _w, _n = verbs.check(d, LEMMAS)
    if problems:
        lines.append(u"FALSE POSITIVE  %s -> %s" % (why, problems[0]))
        bad += 1
lines.append(u"must pass  %d cases" % len(MUST_PASS))

# The membership rule is the only one that needs content to exist. With no
# dictionary yet it has to warn rather than fail, or a course could never carry
# a verb file before it carried words.
p, w, _n = verbs.check(doc({u"sprechen": GOOD}), set())
if p or not w:
    lines.append(u"MISSED  an empty dictionary should warn, not fail")
    bad += 1
lines.append(u"empty dictionary warns instead of failing")

lines.append(u"verb gate: %s" % (u"all clean" if not bad else u"%d PROBLEM(S)" % bad))
io.open(os.path.join(HERE, "verbs-test-report.txt"), "w",
        encoding="utf-8").write(NEWLINE.join(lines) + NEWLINE)
for l in lines:
    try:
        print(l)
    except UnicodeEncodeError:
        print(l.encode("ascii", "replace").decode("ascii"))
sys.exit(1 if bad else 0)
