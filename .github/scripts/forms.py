# -*- coding: utf-8 -*-
"""Maps the inflected words that appear in the course back to their dictionary entry.

Same job as es-ni's, same contract - build(dictionary, texts, verbs) returns
(forms, ambiguous, seen) - and a different language underneath.

Without it a reader who taps *spricht*, *Haeuser* or *grossen* gets nothing:
no meaning, no exposure, no colour, and the memory of *sprechen* never grows.
Only forms that ACTUALLY OCCUR in this course's own text are emitted, so the
pack stays small and every mapping can be checked against real usage.

Three tiers decide who owns a form, in this order:

  1. STATED - verbs.json says so. Ablaut has no rule, so the principal parts
     are facts and they beat anything a rule produced.
  2. RULED - the paradigms built off a stated part, noun plurals (also stated),
     adjective endings, and the closed-class tables.
  3. WEAK - claims that lose every argument. Compound heads, and the finite
     forms of a separable verb whose base verb is not itself taught.

A form two lemmas could both produce is DROPPED, not guessed at. A word that
shows nothing is recoverable; a word that shows the wrong meaning is not.

---------------------------------------------------------------------------
SEPARABLE VERBS ARE NOT THIS FILE'S JOB, AND THAT IS SETTLED

    Ich steige in Zuerich um.

*steige* and *um* are four words apart and can be twelve. A form-to-lemma map
is a dictionary of single words and cannot join them. **It does not try.**

The reader joins them instead, where the whole sentence is in hand:
`separableBindings()` in the app's engine.js, using German's own bracket - a
stranded prefix ends its clause. Both halves then resolve to the separable
lemma, both are marked, and both count as one word.

So what this file emits for a separable verb is the infinitive, the participle,
and the bare finite forms mapped to the BASE verb where the course teaches one.
That is correct in its own right: outside a bracket, *kommt* is kommen.

**Do not make this file guess.** A static map that decided which *kommt*
belonged to *ankommen* would be wrong every time the *an* was a preposition -
and the --separable report below makes exactly that mistake on "Ein Mann kommt
an mir vorbei", which is vorbeikommen. That report is kept as an AUDIT of where
brackets occur, not as a thing to act on.

    python forms.py --root . --separable
---------------------------------------------------------------------------
"""
import argparse, io, json, os, re, sys

TOKEN = re.compile(u"[^\\W\\d_]+", re.UNICODE)
NEWLINE = chr(10)


def tokens(text):
    return TOKEN.findall(text or u"")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


# ── verb paradigms ──────────────────────────────────────────
# Built off the parts verbs.json states. Nothing here invents a stem change:
# the du and er forms are read out of the file, and only the endings that are
# genuinely regular - the ich, wir, ihr and sie forms - are produced.

def stem_of(infinitive):
    """sprechen -> sprech, sammeln -> sammel, tun -> tu."""
    if infinitive.endswith(u"en"):
        return infinitive[:-2]
    if infinitive.endswith(u"n"):
        return infinitive[:-1]
    return infinitive


# Stated, because a rule reaches none of them. sein is suppletive, and every
# modal has an ich form that is identical to its er form and shares neither
# with the infinitive stem - ich kann, er kann, wir koennen. Ruling these
# produced "seie", "seit" and "koenne", and left sind and bin, two of the
# commonest words in the language, resolving to nothing at all.
IRREGULAR_PRESENT = {
    u"dürfen":  [u"darf", u"darfst", u"dürfen", u"dürft"],
    u"sein":    [u"bin", u"bist", u"ist", u"sind", u"seid"],
    u"haben":   [u"habe", u"hast", u"hat", u"haben", u"habt"],
    u"werden":  [u"werde", u"wirst", u"wird", u"werden", u"werdet"],
    u"tun":     [u"tue", u"tust", u"tut", u"tun"],
    u"können":  [u"kann", u"kannst", u"können", u"könnt"],
    u"müssen":  [u"muss", u"musst", u"müssen", u"müsst"],
    u"wollen":  [u"will", u"willst", u"wollen", u"wollt"],
    u"sollen":  [u"soll", u"sollst", u"sollen", u"sollt"],
    u"mögen":   [u"mag", u"magst", u"mögen", u"mögt"],
    u"wissen":  [u"weiss", u"weisst", u"wissen", u"wisst"],
    u"möchten": [u"möchte", u"möchtest", u"möchten", u"möchtet"],
}


def needs_e(stem):
    """atmen -> atmet, warten -> wartet, regnen -> regnet.

    A stem ending in t, d, or in a consonant plus m or n, takes an extra e
    before the ending or it cannot be said.
    """
    if stem.endswith((u"t", u"d")):
        return True
    if stem.endswith((u"m", u"n")) and len(stem) > 1 and stem[-2] not in u"aeiouäöülmnr":
        return True
    return False


def present_forms(inf, v):
    """The present tense, with du and er taken from the file rather than ruled.

    The ich form is the bare stem plus -e, which holds even for the strong
    verbs: ich spreche, ich fahre, ich nehme. The stem change lives in du and
    er only, and both of those are stated.
    """
    if inf in IRREGULAR_PRESENT:
        return set(IRREGULAR_PRESENT[inf]) | set(
            f for f in (v.get("pres2"), v.get("pres3")) if f)
    st = stem_of(inf)
    e = u"e" if needs_e(st) else u""
    out = set()
    out.add(st + u"e")                       # ich spreche
    out.add(inf)                             # wir/sie sprechen
    out.add(st + e + u"t")                   # ihr sprecht, ihr wartet
    for f in (v.get("pres2"), v.get("pres3")):
        if f:
            out.add(f)
    return out


def past_forms(v):
    """The Praeteritum, off the stated third person.

    Weak verbs state a past3 ending in -te and take -test/-ten/-tet; strong
    verbs state a bare stem and take -st/-en/-t. Which of the two a verb is
    can be read off the stated form, so nothing has to be guessed.
    """
    p = v.get("past3")
    if not p:
        return set()
    out = set([p])
    if p.endswith(u"te"):                    # machte, machtest, machten, machtet
        out |= set([p + u"st", p + u"n", p + u"t"])
    else:                                    # sprach, sprachst, sprachen, spracht
        out |= set([p + u"st", p + u"en", p + u"t"])
        if p.endswith((u"s", u"ss", u"z")):  # du assest, not du asst
            out.add(p + u"est")
    return out


def k2_forms(v):
    k = v.get("k2")
    if not k:
        return set()
    out = set([k])
    if k.endswith(u"e"):
        out |= set([k + u"st", k + u"n", k + u"t"])
    return out


# ── nouns ───────────────────────────────────────────────────
def noun_forms(lemma, entry):
    """Singular, the stated plural, and the case endings German actually adds.

    Plurals are read out of the dictionary, never ruled: Haus/Haeuser and
    Stadt/Staedte have no rule behind them, and a rule that guessed would be
    wrong more often than not.
    """
    out = set([lemma])
    pl = entry.get("pl")
    if pl:
        out.add(pl)
        # Dative plural adds -n unless the plural already ends in -n or -s.
        if not pl.endswith((u"n", u"s")):
            out.add(pl + u"n")
    g = entry.get("g")
    if g in (u"der", u"das"):
        # zu Hause, im Jahre. Archaic in most places and completely alive in
        # the handful of phrases that keep it.
        if len(lemma) <= 5 and not lemma.endswith(u"e"):
            out.add(lemma + u"e")
        # Genitive: -es after a sibilant or a consonant cluster, -s otherwise.
        out.add(lemma + (u"es" if lemma.endswith((u"s", u"ss", u"z", u"x", u"sch", u"t"))
                         else u"s"))
    return out


# ── adjectives ──────────────────────────────────────────────
# Every adjective takes one of five endings depending on the article in front
# of it. Which ending is a question about the sentence; WHICH WORD it is, is
# not, and that is all this has to answer.
ADJ_ENDINGS = (u"e", u"en", u"em", u"er", u"es")


def adj_forms(lemma):
    out = set([lemma])
    base = lemma
    # dunkel -> dunkle, teuer -> teure: the e drops before an ending.
    contracted = None
    if base.endswith((u"el", u"er")) and len(base) > 3:
        contracted = base[:-2] + base[-1]
    for e in ADJ_ENDINGS:
        out.add(base + e)
        if contracted:
            out.add(contracted + e)
    # Comparative and superlative. The umlauting ones (alt/aelter) are stated
    # in COMPARATIVES below, because no rule reaches them.
    for e in (u"", u"e", u"en", u"em", u"er", u"es"):
        out.add(base + u"er" + e)
    sup = base + (u"este" if base.endswith((u"t", u"d", u"s", u"ss", u"z"))
                  else u"ste")
    for e in (u"", u"n", u"m", u"r", u"s"):
        out.add(sup + e)
    return out


# Stated, never ruled. These are the whole list for German - it is a closed
# set, and a rule would umlaut things that do not umlaut.
COMPARATIVES = {
    u"alt": (u"älter", u"ältesten"),
    u"gross": (u"grösser", u"grössten"),
    u"jung": (u"jünger", u"jüngsten"),
    u"kalt": (u"kälter", u"kältesten"),
    u"warm": (u"wärmer", u"wärmsten"),
    u"lang": (u"länger", u"längsten"),
    u"kurz": (u"kürzer", u"kürzesten"),
    u"hoch": (u"höher", u"höchsten"),
    u"nah": (u"näher", u"nächsten"),
    u"stark": (u"stärker", u"stärksten"),
    u"scharf": (u"schärfer", u"schärfsten"),
    u"hart": (u"härter", u"härtesten"),
    u"gut": (u"besser", u"besten"),
    u"viel": (u"mehr", u"meisten"),
    u"gern": (u"lieber", u"liebsten"),
    u"oft": (u"öfter", u"häufigsten"),
    u"wenig": (u"weniger", u"wenigsten"),
}


# ── the closed classes ──────────────────────────────────────
# Articles and pronouns are a short, fixed list, so they are written out rather
# than ruled. Every case form of the definite article points at `der`: all
# three entries gloss as "the", so the card reads the same either way and the
# learner's memory of "the" consolidates on one word instead of splitting
# three ways over a distinction the gloss does not carry.
CLOSED = {
    u"der": [u"der", u"die", u"das", u"den", u"dem", u"des", u"denen", u"dessen", u"deren"],
    u"ein": [u"ein", u"eine", u"einen", u"einem", u"einer", u"eines"],
    u"kein": [u"kein", u"keine", u"keinen", u"keinem", u"keiner", u"keines"],
    u"mein": [u"mein", u"meine", u"meinen", u"meinem", u"meiner", u"meines"],
    u"ich": [u"ich", u"mich", u"mir"],
    u"du": [u"du", u"dich", u"dir"],
    u"er": [u"er", u"ihn", u"ihm"],
    u"es": [u"es"],
    u"wir": [u"wir", u"uns"],
    u"sie": [u"sie", u"ihnen"],
    u"Sie": [u"Sie", u"Ihnen", u"Ihr", u"Ihre", u"Ihrem", u"Ihren"],
    u"man": [u"man"],
    u"dieser": [u"dieser", u"diese", u"dieses", u"diesen", u"diesem"],
    u"jeder": [u"jeder", u"jede", u"jedes", u"jeden", u"jedem"],
    u"wer": [u"wer", u"wen", u"wem"],
    u"niemand": [u"niemand", u"niemanden", u"niemandem"],
    u"jemand": [u"jemand", u"jemanden", u"jemandem"],
    u"alle": [u"alle", u"allen", u"allem", u"aller"],
    u"manche": [u"manche", u"manchen", u"manchem", u"mancher"],
    u"ihr": [u"ihr", u"ihre", u"ihren", u"ihrem", u"ihrer", u"ihres"],
    u"viel": [u"viel", u"viele", u"vielen", u"vieler", u"vielem"],
    u"beide": [u"beide", u"beiden"],
    u"sein": [u"seine", u"seinen", u"seinem", u"seiner", u"seines"],
}


def compound_head(word, nouns):
    """Waschkueche -> Kueche. A WEAK claim, and a real German multiplier.

    Once the parts are solid a compound cracks itself open, and the last piece
    is the word: a Fahrplan is a plan, a Rolltreppe is a staircase. Mapping an
    unknown compound to its head means the reader can answer *Samstagabend*
    with "evening" instead of with nothing.

    Weak, because it is a guess about where the seam is. Anything with a real
    claim on the same spelling takes it.
    """
    if len(word) < 8 or not word[:1].isupper():
        return None
    best = None
    for n in nouns:
        # Three letters is long enough to be a head: Vierwaldstaettersee is a
        # See, and that is the one word in the name a learner can already use.
        if len(n) < 3 or len(n) >= len(word):
            continue
        if word.endswith(n) and (best is None or len(n) > len(best)):
            best = n
        # Fugen-s: Jahreszeit is Jahr + es + Zeit, so the head is capitalised
        # inside the word and matches with its own capital lowered.
        elif word.endswith(n[0].lower() + n[1:]) and (best is None or len(n) > len(best)):
            best = n
    return best


CLAUSE_END = re.compile(u"[,;:.!?]")


def separable_bindings(words, lemma_fn, verbs):
    """Which tokens of a sentence are the two halves of one separable verb.

    The Python twin of separableBindings() in the app's engine.js, and it has
    to stay in step with it: the reader counts an exposure for the separable
    lemma, so anything that measures the course - schedule.py's density and
    return quotas - has to count the same word, or the gate judges a story on
    a reading nobody gets.

    Same rule: a stranded prefix ends its clause. `words` is a list of
    (token, is_clause_end) pairs. Returns {index: lemma}.
    """
    table = (verbs or {}).get("verbs") or {}
    out = {}
    clauses, start = [], 0
    for i, (_w, end) in enumerate(words):
        if end:
            if i > start:
                clauses.append((start, i))
            start = i + 1
    if start < len(words):
        clauses.append((start, len(words)))

    for lo, hi in clauses:
        if hi - lo < 2:
            continue
        last = hi - 1
        prefix = words[last][0].lower()
        for i in range(lo, last):
            lemma = lemma_fn(words[i][0])
            if not lemma:
                continue
            joined = prefix + lemma
            v = table.get(joined)
            if v and v.get("sep"):
                out[i] = joined
                out[last] = joined
                break
    return out


def build(dictionary, texts, verbs=None, overrides=None):
    """form -> lemma, for every form that occurs in `texts`.

    Returns (forms, ambiguous, seen), matching es-ni's signature so stage.py,
    reconcile.py and build-pack.py can all call it the same way.
    """
    verbs = verbs or {}
    table = (verbs.get("verbs") or {}) if isinstance(verbs, dict) else {}

    seen = set()
    for t in texts:
        seen.update(tokens(t))
    lower_seen = set(w.lower() for w in seen)

    stated, ruled, weak = {}, {}, {}

    def claim(bucket, form, lemma):
        if not form or not lemma:
            return
        # Only what somebody actually wrote. Over-generating above is safe
        # because everything nobody wrote is thrown away right here.
        if form not in seen and form.lower() not in lower_seen:
            return
        if form == lemma:
            return
        bucket.setdefault(form, set()).add(lemma)

    # ── tier 1: what verbs.json states ──────────────────────
    for inf, v in table.items():
        if inf.startswith(u"_") or not isinstance(v, dict):
            continue
        pre, sep = v.get("pre"), v.get("sep")

        # Single-word forms always belong to the verb they are written on.
        for f in (v.get("pp"), v.get("k2")):
            claim(stated, f, inf)
        for f in k2_forms(v):
            claim(stated, f, inf)

        if sep:
            # A separable verb's finite forms are written apart, so the token
            # on the page is the bare stem and the prefix is somewhere else in
            # the clause. The bare stem belongs to the base verb where the
            # course teaches one - tapping *kommt* in "kommt an" should open
            # kommen, which is the word the reader actually pointed at.
            base = inf[len(pre):] if pre and inf.startswith(pre) else None
            bucket = ruled if (base and base in dictionary) else weak
            owner = base if (base and base in dictionary) else inf
            for f in present_forms(inf, {}):
                claim(bucket, f.replace(pre, u"", 1) if f.startswith(pre) else f, owner)
            for part in (v.get("pres2"), v.get("pres3"), v.get("imp")):
                if part:
                    claim(bucket, part.split(u" ")[0], owner)
            for f in past_forms(v):
                claim(bucket, f.split(u" ")[0], owner)
            continue

        for f in present_forms(inf, v):
            claim(stated if f in (v.get("pres2"), v.get("pres3")) else ruled, f, inf)
        for f in past_forms(v):
            claim(stated, f, inf)
        if v.get("imp"):
            claim(stated, v["imp"], inf)

    # ── tier 2: the dictionary's own shapes ─────────────────
    nouns = [k for k, e in dictionary.items() if e.get("pos") == "n"]
    for lemma, entry in dictionary.items():
        pos = entry.get("pos")
        if pos == "n":
            for f in noun_forms(lemma, entry):
                claim(ruled, f, lemma)
        elif pos in ("adj", "adv"):
            for f in adj_forms(lemma):
                claim(ruled, f, lemma)
            if lemma in COMPARATIVES:
                comp, sup = COMPARATIVES[lemma]
                for e in (u"", u"e", u"en", u"em", u"er", u"es"):
                    claim(stated, comp + e, lemma)
                base = sup[:-1] if sup.endswith(u"n") else sup
                for e in (u"", u"e", u"n", u"m", u"r", u"s"):
                    claim(stated, base + e, lemma)
        elif pos == "v" and lemma not in table:
            # A verb the trainer does not drill still has a regular present and
            # a regular past, and both are worth mapping.
            st = stem_of(lemma)
            e = u"e" if needs_e(st) else u""
            for f in (st + u"e", st + e + u"st", st + e + u"t", lemma,
                      st + e + u"te", st + e + u"test", st + e + u"ten",
                      st + e + u"tet", u"ge" + st + e + u"t"):
                claim(ruled, f, lemma)

    for lemma, forms in CLOSED.items():
        if lemma not in dictionary:
            continue
        for f in forms:
            claim(ruled, f, lemma)

    # A word with a stated comparative gets it whatever its part of speech:
    # viel is tagged pron and mehr is still its comparative.
    for lemma, (comp, sup) in COMPARATIVES.items():
        if lemma not in dictionary:
            continue
        base = sup[:-1] if sup.endswith(u"n") else sup
        for e in (u"", u"e", u"en", u"em", u"er", u"es"):
            claim(stated, comp + e, lemma)
        for e in (u"", u"e", u"n", u"m", u"r", u"s"):
            claim(stated, base + e, lemma)

    # ── tier 3: the weak guesses ────────────────────────────
    for w in seen:
        if w in dictionary:
            continue
        head = compound_head(w, nouns)
        if head:
            claim(weak, w, head)

    # ── settle ──────────────────────────────────────────────
    candidates = {}
    for f in set(stated) | set(ruled) | set(weak):
        candidates[f] = stated.get(f) or ruled.get(f) or weak.get(f)

    forms, ambiguous = {}, []
    for f, lemmas in candidates.items():
        if f in dictionary:
            continue                      # it is its own entry already
        if len(lemmas) == 1:
            forms[f] = next(iter(lemmas))
        else:
            ambiguous.append((f, sorted(lemmas)))

    # The hand-pinned answers, applied HERE rather than by each caller, so
    # stage.py, reconcile.py and build-pack.py can never disagree about a
    # form - which they did in es-ni, and a warm-up card turned on which one
    # happened to be right. A null blocks a form outright.
    for f, lemma in (overrides or {}).items():
        if f.startswith(u"_"):
            continue                      # a note, not a form
        if lemma is None:
            forms.pop(f, None)
        elif lemma in dictionary:
            forms[f] = lemma
    return forms, ambiguous, seen


# ── what the separable-verb limit actually costs ────────────
def separable_report(dictionary, texts, verbs):
    """Every clause where a prefix is stranded, and how far from its verb.

    Printed rather than acted on, because closing this gap is a change in the
    reader, not here. The decision wants a number.
    """
    table = (verbs.get("verbs") or {})
    seps = dict((inf, v["pre"]) for inf, v in table.items()
                if isinstance(v, dict) and v.get("sep") and v.get("pre"))
    if not seps:
        return []
    bases = {}
    for inf, pre in seps.items():
        bases.setdefault(stem_of(inf[len(pre):]), []).append((inf, pre))

    hits = []
    for t in texts:
        for clause in re.split(u"[.!?]", t or u""):
            ws = tokens(clause)
            low = [w.lower() for w in ws]
            for i, w in enumerate(low):
                for stem, cands in bases.items():
                    if not w.startswith(stem) or len(w) - len(stem) > 3:
                        continue
                    for inf, pre in cands:
                        for j in range(i + 1, len(low)):
                            if low[j] == pre:
                                hits.append((inf, u" ".join(ws), j - i))
                                break
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--separable", action="store_true",
                    help="report what the stranded-prefix limit costs")
    args = ap.parse_args()
    content = os.path.join(os.path.abspath(args.root), "content")

    dictionary = {}
    for name in sorted(os.listdir(os.path.join(content, "dictionary"))):
        if name.endswith(".json") and "override" not in name:
            dictionary.update(read(os.path.join(content, "dictionary", name)))

    texts = []
    ldir = os.path.join(content, "lessons")
    if os.path.isdir(ldir):
        for name in sorted(os.listdir(ldir)):
            if name.endswith(".json"):
                for sn in read(os.path.join(ldir, name)).get("sn") or []:
                    texts.append(sn.get("s") or u"")
    sdir = os.path.join(content, "scenarios")
    if os.path.isdir(sdir):
        for name in sorted(os.listdir(sdir)):
            if name.endswith(".json"):
                for st in read(os.path.join(sdir, name)).get("steps") or []:
                    texts.append(st.get("es") or u"")
                    for o in st.get("options") or []:
                        texts.append(o.get("es") or u"")

    vpath = os.path.join(content, "verbs.json")
    verbs = read(vpath) if os.path.exists(vpath) else {}

    ov_path = os.path.join(content, "dictionary", "forms-overrides.json")
    overrides = read(ov_path) if os.path.exists(ov_path) else {}

    forms, ambiguous, seen = build(dictionary, texts, verbs, overrides)

    words = [w for t in texts for w in tokens(t)]
    hit = sum(1 for w in words
              if w in dictionary or w in forms
              or w.lower() in dictionary or w.lower() in forms)

    lines = [
        u"words      %d on the page, %d distinct" % (len(words), len(set(words))),
        u"forms      %d inflections mapped, %d dropped as ambiguous"
        % (len(forms), len(ambiguous)),
        u"tappable   %.1f%%" % (100.0 * hit / max(1, len(words))),
    ]

    missing = {}
    for w in words:
        if not (w in dictionary or w in forms
                or w.lower() in dictionary or w.lower() in forms):
            missing[w] = missing.get(w, 0) + 1
    lines.append(u"")
    lines.append(u"still unmapped, commonest first:")
    for w, n in sorted(missing.items(), key=lambda x: -x[1])[:40]:
        lines.append(u"  %-22s %d" % (w, n))

    if ambiguous:
        lines.append(u"")
        lines.append(u"dropped as ambiguous:")
        for f, ls in sorted(ambiguous)[:40]:
            lines.append(u"  %-22s %s" % (f, u" / ".join(ls)))

    if args.separable:
        hits = separable_report(dictionary, texts, verbs)
        lines.append(u"")
        lines.append(u"THE STRANDED PREFIX, %d clauses:" % len(hits))
        for inf, clause, gap in hits[:30]:
            lines.append(u"  %-14s gap %d   %s" % (inf, gap, clause))

    out = os.path.join(content, "plan", "forms-report.txt")
    io.open(out, "w", encoding="utf-8").write(NEWLINE.join(lines) + NEWLINE)
    for l in lines[:6]:
        try:
            print(l)
        except UnicodeEncodeError:
            print(l.encode("ascii", "replace").decode("ascii"))
    print("full report in content/plan/forms-report.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
