# -*- coding: utf-8 -*-
"""Proves the Swiss gate fires, and proves it does not fire on correct German.

A gate nobody tests reports zero problems whether it is working or asleep, and
this one has already been wrong once: it rejected Grüezi as a misspelling of
itself, because the list was written in ASCII and folding ü to ue collided the
correct spelling with a banned variant. Both directions are asserted here.

    python .github/scripts/dialect_test.py
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dialect  # noqa: E402

NEWLINE = chr(10)


def pack_of(*lines):
    return {"lessons": [{"id": "t-01", "sn": [{"s": l} for l in lines]}]}


MUST_FAIL = [
    (u"Ich fahre mit dem Fahrrad.",            u"Fahrrad"),
    (u"Er liegt im Krankenhaus.",              u"Krankenhaus"),
    (u"Eine Fahrkarte nach Bern.",             u"Fahrkarte"),
    (u"Sahne auf den Kuchen.",                 u"Sahne"),
    (u"Der Friseur hat zu.",                   u"Friseur"),
    (u"Wir haben dort geparkt.",               u"geparkt"),
    (u"Ein Brötchen, bitte.",                  u"Brötchen"),
    (u"Das war wirklich lecker.",              u"lecker"),
    (u"Die Strasse heißt anders.",             u"eszett"),
    (u"Gib mir eine Tüte.",                    u"Tüte"),
    (u"Er wartet auf dem Bahnsteig.",          u"Bahnsteig"),
    (u"Salli zusammen.",                       u"Salli"),
    (u"Das ist tipptopp.",                     u"tipptopp"),
    (u"merci villmal für alles.",              u"merci villmal"),
]

# Every one of these is correct Swiss Standard German and must pass untouched.
MUST_PASS = [
    u"Grüezi mitenand, ich nehme das Velo.",
    u"Ein Billett nach Luzern, bitte.",
    u"Er liegt im Spital.",
    u"Sali, alles tiptop?",
    u"merci vielmal, uf Wiederluege.",
    u"Hoi zäme, wir grillieren heute.",
    u"Ich habe das Auto parkiert und ein Gipfeli gekauft.",
    u"Das Tram fährt über die Strasse.",
    u"Rahm und Rüebli aus dem Sack.",
    u"Das Poulet war fein.",
    u"Wir gehen schlitteln, wenn es schneit.",
    # Words that would be false positives if the list were careless.
    u"Das Huhn steht im Garten.",          # Huhn is fine, only Hähnchen is not
    u"Im Winter liegt Eis auf dem See.",   # Eis is frozen water, not Glace
    u"Karotten und Paprika kaufen.",       # both fine in Switzerland
    u"Der Sack ist voll.",                 # Sack is the Swiss word, not banned
    u"Es hat kein Abendessen gegeben.",    # only Abendbrot is German
]

fails = []

for line, expect in MUST_FAIL:
    problems, warnings, _ = dialect.check(pack_of(line))
    if not problems:
        fails.append(u"NOT CAUGHT (%s): %s" % (expect, line))

for line in MUST_PASS:
    problems, warnings, _ = dialect.check(pack_of(line))
    if problems:
        why = u"; ".join(u"%s: %s" % (p[1], p[2]) for p in problems)
        fails.append(u"FALSE POSITIVE: %s -- %s" % (line, why))

# The allow-list must exempt a line that teaches the contrast, by id only.
teach = {"lessons": [{"id": "p0-06", "sn": [
    {"s": u"Hier sagt man Weggli, nicht Brötchen."}]}]}
if not dialect.check(teach)[0]:
    fails.append(u"the teaching line was not caught without an allow entry")
if dialect.check(teach, {"lines": ["lesson p0-06"]})[0]:
    fails.append(u"the allow-list did not exempt lesson p0-06")

report = [u"must fail  %d lines" % len(MUST_FAIL),
          u"must pass  %d lines" % len(MUST_PASS),
          u"allow-list exempts by story id"]
report += fails
report.append(u"dialect gate: %s" % (u"all clean" if not fails
                                     else u"%d FAILURE(S)" % len(fails)))
io.open(os.path.join(HERE, "dialect-test-report.txt"), "w",
        encoding="utf-8").write(NEWLINE.join(report) + NEWLINE)
for line in report:
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode("ascii"))
sys.exit(1 if fails else 0)
