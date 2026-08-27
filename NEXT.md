# START HERE — where the German course stands

**Phases 0 to 3 are written. The plan is finished and it is not up for
relitigating.** `content/plan/spine.json` holds all 192 stories across 8
phases, each with the German it teaches, the Switzerland it carries and what
happens in it. Read `HANDOFF.md` beside this file for every decision and the
reasoning behind it. This file is the short version and says what to do next.

| | | |
|---|---|---|
| Language | **Swiss Standard German** | code `de-ch`, repo `scenicprints/fluidez-de-ch` |
| Anchored in | **Luzern** | you land at Zurich Kloten and take the train |
| Stories planned | **192** | 8 phases, **86 written** (phases 0 to 3 complete) |
| App support | **shipped** | v2.8.25, mascot + palette + English interface + switcher |
| Stories on people | **62** | phases 4 and 5, a third of the course |

---

## The one-paragraph version

Kevin Wagner is building Fluidez to teach what other apps refuse to: real
regional language and the culture that comes with it. Nicaraguan Spanish was
the first. German is the second, and it teaches **Swiss Standard German** as
spoken and written in Luzern. Every word must be Swiss rather than German
German, and that is enforced by a build gate rather than by care. The heart of
the course is phases 4 and 5, love and grief, because deep emotional
vocabulary is the thing Fluidez exists to deliver and Duolingo never will.

---

## What is done

- [x] **The variety chosen and the line drawn.** Swiss Standard German, one
      variety, start to finish. No dialect ramp. See `HANDOFF.md` §2.
- [x] **The eight phases**, in Kevin's order, with the grammar ladder under
      each. See `HANDOFF.md` §4.
- [x] **The cast**, planned with its endings already known. `HANDOFF.md` §5.
- [x] **The spine.** All 192 stories in `content/plan/spine.json`.
- [x] **The Swiss gate and the staging script** (2026-08-25), both tested.
- [x] **The eight culture gaps closed** (2026-08-25). An audit found the course
      had seven Fasnacht stories and no Schwingen at all. Added, each placed
      where the calendar puts it rather than appended: `p3-14` Das Schwingfest,
      `p3-17` Der Alpabzug, `p3-18` Der erste Schnee, `p4-17` Der WK, `p4-18`
      Der Samichlaus, `p6-22` Der erste August, `p6-23` Alphorn und Jodel,
      `p2-22` Räbeliechtli. **Re-run that audit after any spine edit** — the
      script is trivial and the gap was invisible until somebody looked.

## What is next, in order

**Every script is now built.** The loop for writing content is:

```bash
python .github/scripts/stage.py --root .        # shape, Swiss, verbs, forms, schedule
python .github/scripts/reconcile.py --root .    # rewrite the warm-ups from the text
python .github/scripts/build-pack.py --root .   # bundle, and refuse to if a gate fires
```

`reconcile.py` WRITES content, so it is a step in the writing loop and not a
gate. Run it after the stories change and before the build. `--dry-run` reports
what it would change and writes nothing.

**1. The gates — dialect and stage are DONE (2026-08-25).**

- **`dialect.py`** — the Swiss gate. No eszett, no Germanism where a Helvetism
  is standard, one spelling per pinned dialect word. The word list is
  `helvetisms.json` **with a source on every entry** (`duden-ch`, `admin`,
  `common`), which is the answer to "nobody can fact-check this": it is a list
  with citations rather than a list from memory. Anything not attested is a
  `warn`, never a `fail`.
- **`dialect_test.py`** — asserts the gate fires on 14 poisoned lines and stays
  silent on 16 correct ones. **Run it after touching the word list.** It exists
  because the gate was wrong once: written in ASCII, `fold('Grüezi')` gives
  `grueezi`, which was listed as a *wrong* variant, so it rejected the correct
  spelling of the course's most important word. Germanisms are matched folded
  (Möhre and Moehre are one mistake); **pinned words are matched on exact
  spelling, because the umlaut IS the difference.** Same split es-ni uses for
  tú forms versus foreign vocabulary.
- **`stage.py`** — shape of every story, the Swiss gate over all of them, the
  dictionary debt to `plan/needs-entry.txt`, and it rewrites `plan/PROGRESS.md`
  every run so that file cannot go stale.

```bash
python .github/scripts/stage.py --root .
python .github/scripts/dialect_test.py
```

**Still to port, and the order changed on purpose:**

| Script | When | What changes |
|---|---|---|
| ~~`forms.py`~~ | **DONE 2026-08-25** | 99.2% tappable. See §3 above. |
| ~~`schedule.py`~~ | **DONE 2026-08-25** | Clean. See §14. |
| ~~`reconcile.py`~~ | **DONE 2026-08-25** | Clean and idempotent. See §15. |
| ~~`build-pack.py`~~ | **DONE 2026-08-25** | Bundles the pack and runs every gate. Port from es-ni, which now also carries `ui`, `phases`, `mascot` and `icons` through from the manifest. It must also load `verbs.json` and `emergency.json` and run `verbs.py`. |

**`verbs.py` and `verbs_test.py` are DONE (2026-08-25)** and replace the
`verbs_build.py` row that used to sit here. There is no German verb *builder*,
on purpose: a builder is a rule, and a rule near German ablaut produces
*er sprecht*. Every form is written by hand and the gate checks that every
one of them was. See §11 below.

**2. Phase 0 — DONE, 2026-08-25, and built as one batch.** Kevin's
instruction: *"You will be building all of the stuff together. That means
Scenes, Review, Verbs, Word Order, Listening, Shadowing, Words, Patterns and
Path gets all built at the same time. Especially so Scenes and the stories
match."*

| | | |
|---|---|---|
| Stories | **16** | `p0-01`–`p0-16`, about 1,500 sentences |
| Dictionary | **637** | lemmas only, every noun with its der/die/das and its plural |
| Verbs | **102** | principal parts, all stated by hand |
| Patterns | **10** | every trigger checked against the dictionary before writing |
| Scenes | **8** | written against the stories, not alongside them |
| Emergency | **5 groups, 40 phrases** | |

**Six of the nine tiles needed no authoring at all** and came alive the moment
the stories and the dictionary existed: Path, Review, Word Order, Listening,
Shadowing, Words. That is worth knowing before the next phase is planned — the
authoring load is stories, dictionary, verbs, patterns, scenes, and nothing
else.

Written un-schedule-gated, because that gate does not exist yet; re-check once
`forms.py` and `schedule.py` land. Sixteen stories is a small enough bet that
rewriting them is cheap.

### What phase 0 taught, that the next phase should copy

- **Write the stories first, then everything else against them.** Lea says
  Crème in `sc03` because that is what she says in `p0-05`. es-ni proved the
  other order costs forty scenes.
- **Phase 0 is present tense and main clauses**, and it does not stay that way
  by itself. A sweep over the finished sixteen found 45 lines that had drifted
  into Präteritum, the Perfekt or a verb-final subordinate clause. `weil` was
  replaced with **`denn`** throughout, which means the same thing and keeps the
  verb in second position — weil sends it to the end, which is phase 5.
- **Let the gates find the gaps.** `verbs.py` caught `schauen` missing from the
  dictionary; the pattern check caught `nicht` missing. Neither was visible by
  reading.
- **`p0-06` teaches Weggli and Gipfeli without ever writing the German German
  word in German.** The contrast lives in the English gloss and in a scene
  option, so the story needs no allow-list entry at all. Prefer that.

**3. `forms.py` — DONE, 2026-08-25. 99.2% of the page is tappable**, against
es-ni's 97.9%, from 313 mapped inflections. **Every word still missing is a
proper noun**: Lea, Luzern, Migros, Coop, Zürich, Pilatus, Kloten, Deutschland.
That is the ceiling, and it is the same 1.9% es-ni stops at.

Checked in the real app rather than from the report: *fährt* opens fahren,
*Häuser* opens Haus, *Bergen* opens Berg, *hält* opens halten, *Münzen* opens
Münze, *teurer* opens teuer. Scenes are at 97.9%.

`stage.py` prints the number every run, so it cannot quietly rot.

### What it states rather than rules, and why each one is there

- **The suppletive presents.** `IRREGULAR_PRESENT` holds sein, haben, werden,
  tun and every modal. Ruling them produced *seie* and *seit*, and left **sind
  and bin** — 68 occurrences in phase 0 alone — resolving to nothing.
- **Noun plurals**, read out of the dictionary. Haus/Häuser and Stadt/Städte
  have no rule behind them and a rule that guessed would be wrong more often
  than right.
- **The umlauting comparatives**, all fifteen of them, in `COMPARATIVES`.
  alt/älter, gross/grösser, hoch/höher, gut/besser.
- **The closed classes**, written out. Every case form of the definite article
  points at `der` on purpose: all three entries gloss as "the", so the card
  reads the same either way and the learner's memory of "the" consolidates on
  one word instead of splitting three ways over a distinction the gloss does
  not carry.

What IS ruled: the ich/wir/ihr present endings (the stem change lives in du and
er, and both of those are stated in `verbs.json`), the Präteritum paradigm off
the stated third person, adjective endings, and the epenthetic e in *wartet*,
*atmet*, *regnet*.

**Compound heads are a WEAK claim and a real German multiplier.** An unknown
capitalised word ending in a known noun maps to that noun, so *Samstagabend*
answers "evening" and *Vierwaldstättersee* answers "lake". Weak, because it is
a guess about where the seam is, so anything with a real claim takes it.

**`forms-overrides.json` is applied inside `forms.build`**, not by each caller.
In es-ni the three callers used to disagree and a warm-up card turned on which
one happened to be right. Two entries so far: `gehört` is pinned to gehören
(it is also hören's participle, and all three places the course writes it, it
is gehören — revisit when phase 2 brings the perfect tense in), and `crème` to
Crème.

**`forms.py` is the largest single piece of work in this project and it should
be sized honestly before it is started.** Spanish inflects predictably and
es-ni reaches 97.9% of words on the page resolving to a dictionary entry.
German has to handle:

- **Separable verbs**, where the prefix detaches and lands at the end of the
  clause. *Ich steige in Zürich um* has to resolve `steige … um` to `umsteigen`.
  Nothing in the Spanish version has to look two words away.
- **Four cases declining both articles and adjectives**, with strong, weak and
  mixed adjective endings depending on what article precedes.
- **Umlaut plurals** (`Haus`/`Häuser`, `Stadt`/`Städte`) and the classes that
  take them.
- **Strong verb ablaut** (`sprechen`/`spricht`/`sprach`/`gesprochen`), which
  like Spanish's irregulars must be **stated, never rule-generated**.
- **Compounds.** `Waschküche` should resolve, and ideally credit both
  `waschen` and `Küche`, because compound decoding is a real German skill and
  a genuine multiplier the Spanish course never had.

**4. The app changes — DONE, shipped 2026-08-25 in v2.8.23.** All four seams
are live in `scenicprints/fluidez` and the Spanish course is pixel-identical:

- **Mascots** live in `docs/js/creatures.js` behind one rig; `mascot.js` drives
  behaviour and no longer knows the species. **Blüemli**, a Braunvieh with a bell
  hanging where the motmot's tail hangs, is the Swiss mascot. A marmot named
  **Mungg** is parked in the same file as a one-line swap.
- **Phases** come from the pack (`setPhases`), falling back to the old ladder.
- **Interface strings** come from the pack (`setStrings` / `t()`), falling back
  to English. **The German course ships no `ui` block on purpose**, so the whole
  interface and the phase ladder are English. Reversed on Kevin's call
  2026-08-25; the reasoning is in `HANDOFF.md` §10 and it is not up for
  re-translating. The Path tab still takes its own icon per course: volcano for
  es-ni, `ic-gondola` for de-ch.
- **Chrome** reads `--accent` / `--chrome-grad`, split from `--oro`, which used
  to mean both "growing" and "this app". `[data-course="de-ch"]` on `<html>`
  paints alpine night: Swiss red and white on charcoal. **The three memory
  colours are identical in both courses on purpose.**
- **The under-construction** screen: a course with no lessons shows its tiles but routes every
  one of them there. Governed by `underConstruction()`, which is just
  `content.lessons.length === 0`, so it disappears by itself when the first
  lesson publishes.
- CI gates `docs/js/creatures.test.mjs` as well as the engine test.

**5. The registry — DONE, 2026-08-25.** `fluidez-languages` lists `de-ch`
alongside `es-ni`, so the Settings row, the language chip on Today and the
picker after account creation are all back.

**Worth knowing, because it looked like a missing feature:** every switcher in
the app hides itself when the registry holds one language, deliberately, on the
grounds that a picker with one destination is a dead end. The consequence while
German was unlisted was that there was no way to change course at all. If a
switcher ever seems to have vanished, check the registry before the code.

**And the deadlock that made this bite twice, fixed in v2.8.25:** a returning
boot read the registry from cache only, and the only path that refetched it
with network was the picker, behind the hidden switchers. So a registry update
could never reach an existing install. Boot now refreshes the registry in the
background after launch, and Settings retries it itself while it only knows
one language.

Two bugs fixed in v2.8.24 at the same time:

- `launch()` painted the mascot only if there was not one already, so switching
  course chose the new creature and left the old one on the branch. It rebuilds
  when the species changes now, and `createMascot()` has a `destroy()` built on
  an AbortController so the swap does not stack a second set of pointer
  handlers on the perch.
- The whole Settings screen was English constants, which is exactly where the
  switcher lives. Twenty-six strings now go through `t()`.

---

## The ten screens, gone through with Kevin on 2026-08-25

Every tile the app can show was read out of the source and each one settled.
**Do not reopen these.**

**Six come free with the 192 stories** and need no separate authoring: Path,
Review, Word Order, Listening, Shadowing, Words. Review generates its four
exercise kinds out of the dictionary and the lesson sentences; Word Order
scrambles 3-to-7-word lines from stories already read; Listening and Shadowing
read those same lines aloud.

**Two are their own projects and both wait for the stories:** Scenes and
Patterns. German has none of either. A scene must be written against the lesson
it pays off, which es-ni proved by binning forty written the other way round,
and a pattern trigger has to resolve to a lemma, so Patterns additionally waits
on `forms.py`.

**Emergency stays.** It was proposed for cutting on the grounds that Central
Switzerland is not Nicaragua, and Kevin rejected that outright: *"We still need
Emergency. It should have never been cut."* It needs `content/emergency.json`
in es-ni's shape, a list of groups of `{title, phrases:[{es, en}]}` — the key
stays `es` even in German because `openPhrases` reads `ph.es` — plus
`"emergency": "emergency.json"` in the manifest and the two passthrough lines
in `build-pack.py`.

**Audio stays as it is.** `speech: de-CH`, no platform ships a Swiss voice, and
`bestVoice()` falls back to the base tag, so it will read Swiss Standard German
in a German German voice and will say Grüezi and merci wrong. Same trade es-ni
took with es-MX. Dropping `audio` would cost Listening, Shadowing and the
reader's read-aloud to fix an accent. Do not reopen it.

## 11. The verb trainer, which is German's own and not Spanish's

**Settled 2026-08-25 after the wrong answer was given first.** The proposal was
to cut the verb tile from German. Kevin: *"So why dont we not be lazy and
create it's own to use."* He was right, and that is what exists now.

### Why the Spanish drill cannot be reused

`startVerbs()` draws a subject, an infinitive and four **single-word** buttons.
Spanish fits that exactly: every cell of its table is one word, and 90
hand-written endings across three regular tables generate every form of 72 of
its 123 verbs. The ending carries the person, so the paradigm is the difficulty
and drilling the paradigm is drilling the language.

German does not fit it, and the reason is structural rather than anything to do
with how much of the course is written:

- **Perfekt, Futur and Konjunktiv II are not conjugations.** They are an
  auxiliary plus a participle or an infinitive, and in a real clause the two
  halves sit apart with everything else in between. They cannot go on a button
  without lying about word order, which is the thing that matters.
- **Präteritum fits on a button but Swiss people write it and do not say it.**
  The Perfekt does nearly all spoken past reference.
- **That leaves the present**, where the endings arrive free from reading and
  only the strong-verb stem changes are hard.

### What was built instead

**Principal parts**: sprechen, spricht, sprach, hat gesprochen. Eight modes,
cycled the way `generateExercises` cycles its kinds — present3, present2, past,
perfect, aux, infinitive, imperative, separable. Distractors are the **same
slot pulled from other verbs**, so every option is shaped like a real answer.

Two of those modes are worth calling out. **imperative** drills *sprich*,
*nimm*, *fahr*, which is still undrillable in es-ni because a one-form tense
hands `startVerbs()` an `undefined` subject; a principal-parts card has no
subject at all, so the problem does not exist here. And **separable** asks
where the prefix goes, of separable *and* inseparable verbs both, because um-
comes off *umsteigen* and does not come off *umarmen* and no prefix list settles
it. Running it only on separable verbs would make the answer always the split
one and the card playable without reading it.

**The app side is live** in `scenicprints/fluidez`: `verbPartItems()` and
`PART_MODES` in `engine.js`, `startVerbParts()` and `renderVerbParts()` in
`screens.js`, branched on `verbs.kind === 'principal-parts'` so the published
Spanish course is untouched. **`conjugate()` is never called on the German
path**, which kills by construction the silent regular-table fallback that
taught *cerro* and *perdo* for years.

It scores itself and **does not touch vocabulary memory**, exactly as the
Spanish drill does. It briefly did feed the memory model, on the argument that
the gate guarantees every drilled verb is a taught lemma. Kevin: *"Do it how
Spanish does it."* Both drills pass `null` now.

### The file and its gate

`content/verbs.json` is **empty on purpose**. Its `_` block carries the whole
schema. Required per verb: `en`, `pres3`, `pres2`, `past3`, `pp`, `aux`.
Optional: `imp`, `pre`, `sep`, `k2`. A separable verb writes its `pres3`
separated, `"steigt um"`.

`verbs.py` enforces two rules. **Every required field is present and stated**,
because a field left out is a form nobody wrote and a field guessed at is worse
than one missing. And **every drilled verb is a lemma the course teaches**,
which is the pattern-trigger lesson: es-ni shipped two patterns and sixteen
mascot lines that could never fire. That second rule is why the verbs wait for
the stories. With an empty dictionary it warns rather than fails, or no course
could ever carry a verb file before it carried words.

`verbs_test.py` fires the gate at 13 poisoned files and checks it stays silent
on 7 good ones. It exists because `dialect.py` was wrong once and nobody knew.

**`dialect.py collect()` now also reads the emergency phrasebook and every
stated verb form.** Both were outside the Swiss gate. The phrasebook is the
worst possible place for a hole, since it is read in a hurry by somebody who
cannot yet check the words, and Spital-not-Krankenhaus would have gone straight
through it.

## 12. The app fix phase 0 forced: capitalised words

**Found by measuring, not by reading, and it had cost half the course.**

`resolve()` was handed a lower-cased word, which is right for Spanish and wrong
for German, where **every noun is capitalised**. 217 of the 637 words in the
dictionary are, so Mann, Frau, Koffer, Bahnhof and Grüezi were all untappable,
recorded no exposure and counted towards no memory. Tappability measured
**53.9%**.

Worse than the misses were the two pairs where the capital IS the word:
**der Morgen** is the morning and **morgen** is tomorrow, **der Weg** is the way
and **weg** means gone. A lower-cased lookup answered both backwards.

`dictKey()` in `engine.js` now tries the **exact spelling first and the
lower-cased one second**, and `resolve()` takes the word as written. Sentence-
initial capitals still fall through, so *Ich* lands on `ich`. **Nothing changes
for Spanish**: its keys are lower case, the exact try always misses, and every
lookup ends where it always did. Tappability went to **72.3%** and the rest is
`forms.py`'s.

The same lower-cased lookup was in `generateExercises`, so **every gap exercise
in the German course would have been built out of the function words** — no
German noun could ever be the blank. Fixed with the same helper.

Two smaller ones fixed at the same time:

- **`generateExercises` had a hardcoded Spanish fallback item** for when it
  could build nothing. In any other course that is the app teaching the wrong
  language. It returns nothing now and `startReview()` says so.
- **`renderTyped` said "Write this in Spanish"** in every course. It reads
  "Write this in Swiss German" now, from the language's own name.
- **A scene never re-checked pattern unlocks.** Scenes record exposures, so a
  scene could push a pattern over its threshold and the pattern would sit
  reading "0 more words to go" and stay locked until a lesson happened to be
  read next. `answerScene` calls `checkPatterns()` now.

## 18. Phase 3 — Getting About, 21 stories, DONE 2026-08-27

| | | |
|---|---|---|
| Stories | **86** total | 21 new, 12,050 running words |
| Dictionary | **1,579** | +260 |
| Verbs | **296** | +48, every form stated |
| Patterns | **35** | +8 |
| Scenes | **28** | +6 |
| Blüemli | **81** lines | +10 |
| Tappable | **98.4%** whole course | |
| Warm-ups | 471 words, 0 stories with none | |

The country opens up. **Selina arrives on the summit of Pilatus in `p3-10`**,
which is where the spine always had her, and the two stories after it are the
gondola down and the message on Wednesday evening. Timo's Stans gets a statue
of a man who pulled spears into his own body, his uncle spends three months a
year in a hut making cheese, and the last train home turns out to be the reason
nobody has to decide when an evening ends.

The grammar is **separable verbs and the two-way prepositions**, and the phase
is built so both arrive through the transport system rather than through a
table: *ich steige in Luzern ein*, *ich steige in Stans aus*, *wir fahren auf
den See hinaus* against *wir sind auf dem See*.

### What the phase taught about writing the next one

- **The recycling discipline works and it is measurable.** Phase 2's arrival
  took 44 warm-up cards away from phases 0 and 1. Phase 3's arrival took **28**
  away from phase 2, and phase 3 was written knowing that would happen. 84
  sentences closed it against phase 2's 129. Expect the number to keep falling
  and never to reach zero: it is the cost of the course getting longer.
- **A separable verb does not count as its own base.** Six of those 28 were
  closed on the first try and `bringen` was not, because every sentence added
  for it said *mitbringen*. The binder is right and the gate is right: they are
  two words. Add a plain one.
- **The spine's German column is a hint, not the ladder.** `p3-18` asks for
  *wenn* clauses. Phase 5 owns subordinate clauses and phases 0 to 2 were
  written without them, so the story teaches the same winter with main clauses
  and `denn`. `HANDOFF.md` §4 is the load-bearing document; the spine's grammar
  notes were written before any of it existed. Flag a conflict rather than
  quietly following either one.
- **`können Sie mir ...` is taught as `können Sie mir helfen` / `den Weg
  zeigen`,** not `können Sie mir sagen, wo ...`, which is a subordinate clause
  wearing a politeness formula. Same lesson, same register, no phase-5 grammar.
- **Coverage bit exactly once, at `p3-14`,** the Schwingfest, which is the one
  story carrying a whole sport's vocabulary. Two one-use words came out and it
  passed. The Schwingfest is worth the other twenty-two.

### Known and small

- **`Stock` is a floor and a pole.** `Stöcke` is pinned to it, so a ski pole
  opens a card that says floor. It has always been both words in German; if it
  reads badly in phase 4, split it with a `Wanderstock` entry.
- **`aufpassen` and `aufwachen` still appear once each**, three phases running.
  Phase 4 or drop them.

## 17. Phase 2 — Making Friends, 27 stories, DONE 2026-08-26

Same batch as before: stories first, then the dictionary, verbs, patterns and
scenes written against them.

| | | |
|---|---|---|
| Stories | **65** total | 27 new, 15,300 running words |
| Dictionary | **1,319** | +369 |
| Verbs | **248** | +71, every form stated |
| Patterns | **27** | +9 |
| Scenes | **22** | +8 |
| Blüemli | **71** lines | +14, and `fein` is finally taught |
| Tappable | **98.5%** whole course | |
| Warm-ups | 389 words, 0 stories with none | |

**Timo arrives** and brings the mountain with him. **Rosmarie Amrein** stops
being Frau Amrein. **Marco** turns out to have been waiting six months for you
to ask him something. The grammar underneath is the perfect tense and the
dative, and the phase is built so the two arrive through what people do with
them rather than through a table.

### What the phase taught about writing the next one

- **The rule that relaxes is the bracket, not the subordinate clause.** Phase
  5 owns weil, dass and wenn, so phase 2 stays on main clauses and `denn`. What
  it adds is the second bracket: `habe … getrunken` sits exactly where phase
  1's `muss … spülen` sat, so the learner meets a shape they already own with a
  new thing inside it. Every indirect question in the batch was rewritten as a
  direct one for the same reason it was in phase 1.
- **Präteritum is allowed for `war` and `hatte` and nothing else.** That is
  what people actually say: *er hatte nie einen anderen Chef*, but *er hat
  vierzig Jahre gearbeitet*. `p2-15` says so out loud, in the story where an
  eighty-year-old talks about her husband, which is the only place it would not
  read as a grammar note.
- **RETURN went live for phase 1 the day phase 2 landed, and it took 44 cards
  away.** A word is judged once 25 stories exist after it, so phase 1's words
  were unjudged at 38 stories and judged at 65. Forty-four of them lost their
  warm-up: Rechnung, Waschküche, Hauswart, Krankenkasse, Gemeinde, Schalter,
  Miete, waschen, putzen, bestellen. Read as a list it is one sentence long:
  **the flat, the laundry and the bills stopped being mentioned the day the
  protagonist made friends.** That is a fault in the writing and not in the
  gate, and **129 sentences** across three passes put that life back. All 44
  are taught again and nothing else was moved.
- **Adding a use can COST a word its card.** One-scene is a share, not a
  count, so a word that qualified by living almost entirely in one story loses
  the exemption when a later story mentions it once. `Nacht` and `Maschine`
  were both fine until the recycling sweep put them somewhere else, and both
  had to be put back rather than propped up. Re-run the check after every
  sweep: fixing forty words is how you break two.
- **Adding a verb can break a word that already worked.** `meinen` went into
  the dictionary and `meine` immediately became ambiguous between it and the
  possessive, so the reader dropped it and 22 taps stopped working. It is
  pinned in `forms-overrides.json` now. **Check the ambiguous list after every
  batch**, not just the unmapped one: a word that used to resolve and now does
  not never appears in the gaps report.
- **Coverage bites at the end of the ramp, not the start.** One story fired,
  `p2-11`, at 86% against a required 87%. The fix was to cut five new words it
  did not need rather than to move the number, and four of them were in
  sentences that read better shorter.
- **Check a new pattern against the ones already written.** `sie_du` and phase
  0's `sie_und_du` came out as two cards with almost the same title. The new
  one is now `duzen_siezen`, "Wollen wir du sagen?", and it opens by naming
  what phase 0 already said instead of repeating it.
- **The dialect gate does not catch invented dialect spelling** and it is rule
  4 all the same. A draft of `p2-26` explained the written dialect by spelling
  four words of it. Cut, and the point is made without them: read it aloud and
  the German word is in there.

### Known and small

- **`Prost` is offered as an `ok` answer in `sc18`,** not a wrong one. It is
  heard in Switzerland; `Zum Wohl` is simply what an apéro in Luzern mostly
  says. Nothing on the helvetism list, because a list with a citation is the
  rule and there is no citation for banning it.
- **`aufpassen` and `aufwachen` still appear once each.** Phase 2 did not pick
  them up. Phase 3 or drop them.
- **The Swiss perfect widens.** `p2-15` writes *er ist davor gestanden* and
  `perfekt_sein` states the rule, including that Hamburg would say *hat*. This
  is a judgement call nobody in the project can fact-check, and it is now
  written into a pattern card rather than only into stories.

## 16. Phase 1 — Settling In, 22 stories, DONE 2026-08-26

Built the same way phase 0 was: stories first, then the dictionary, verbs,
patterns and scenes written against them, all in one batch.

| | | |
|---|---|---|
| Stories | **38** total | 22 new, ~18,300 running words |
| Dictionary | **950** | +284 |
| Verbs | **177** | +73, every form stated |
| Patterns | **18** | +8 |
| Scenes | **14** | +6 |
| Tappable | **97.8%** phase 1, 99.2% phase 0 | |
| Warm-ups | 289 words, median 8 | |

The cast arrives: **Frau Amrein** across the landing, **Ruedi Zemp** the
Hauswart, **Herr Bucher** below, **Nuno** in the restaurant kitchen. The
building teaches the grammar — the Hausordnung is modal verbs and nothing
else, which is exactly why Kevin put Settling In at position 1.

### What the phase taught about writing the next one

- **Phase 1's own grammar is the discipline.** It teaches VERB SECOND, and a
  subordinate clause is precisely where verb-second stops applying. Writing
  *Sie fragt, wie ich heisse* while teaching V2 undercuts the lesson, so the
  sweep replaced 43 of them — mostly by turning indirect questions into direct
  ones, which is inside the phase AND better writing: *Sie fragt: Wie heissen
  Sie?* is what she actually says.
- **schedule.py fired again and was right again.** 86 sentences were added to
  lift phase 1's central words from three or four uses to five. Warm-ups went
  from 237 words to 289. Same lesson as phase 0: the story is ABOUT those
  words and was only mentioning them.
- **RETURN is finally live.** With 38 stories it judges 94 of 281 declared
  words, and 54 are exempt as one-scene. It abstained entirely on phase 0.
- **`forms.py` had a real bug that only 38 stories exposed.** The epenthetic-e
  rule was the one you find in a grammar — "a consonant plus m or n" — and it
  is too broad: it turned *wohnen* into *wohnet* and *lernen* into *lernet*.
  Only a short list of clusters genuinely needs the e (dm, tm, gn, chn, ffn,
  dn, tn). Tappability went 97.4% → 98.2% on that one fix.
- **Hoi, Sali and tiptop are taught now**, in `sc14` where Nuno greets you, so
  the three Blüemli lines mascot.py pulled in phase 0 are back. **fein** is
  still untaught and its line is still waiting.

### Known and small

`aufpassen` and `aufwachen` accumulate no memory: each appears once, and once
is not enough for the reader to bind. Not a bug — they are simply barely used.
If phase 2 does not pick them up, drop them from `verbs.json`.

## 15. `reconcile.py` — DONE, and it does one thing es-ni's does not

The warm-up is a CLAIM: these are the words this lesson will hammer. Written by
hand the claim drifts, so it is not written by hand any more. `reconcile.py`
derives every warm-up from the text, and the text is the only thing that can be
wrong.

    warm-ups   16 stories, 164 words, median 10, 0 with none

**Idempotent**: a second run changes nothing, which is the property a
derivation should have.

Every warm-up now leads with what its story is about:

| | |
|---|---|
| `p0-02` | **Gleis, Automat, Perron, Billett**, Nummer, suchen, finden |
| `p0-06` | **Weggli, frisch, Gipfeli**, essen, Brot, Bäckerei, leer, Morgen |
| `p0-09` | **laufen, Durst, Brunnen, Flasche, gratis**, voll, trinken, sauber |
| `p0-13` | **Punkt, Entschuldigung, Viertel, beginnen, Termin**, spät, halb |
| `p0-15` | **Föhn, Schirm, Wetter, Wind, schneien**, Regen, nass |

### The change: the word goes to the story that OWNS it

**es-ni assigns in reading order, and its own header records the cost:** the
early stories claim every common word and everything after them starves — 95 of
185 stories ended with no warm-up at all. Its fix was the GAP, letting a word be
re-claimed twenty-five stories later.

That is necessary and it is not sufficient, and German showed why inside
sixteen stories. Assigning in reading order, **"Der See" was refused `See`**,
because `p0-03` watches a lake go past a train window six times on the way to
Luzern and got there first. `p0-12` lost gehen, stehen and schauen the same
way.

So candidates are now ranked by **how much of the word belongs to its story**
and handed out best-first, with GAP still blocking a second claim inside
twenty-five stories. The lake story gets the lake. Port this back to es-ni if
its warm-ups are ever revisited.

### The German trap: BORING is matched on EXACT spelling

`weg` means gone and belongs in BORING. **`der Weg` is the way, and it is what
"Wo ist die Post?" is about.** Lower-casing the test — which is what es-ni does,
correctly, for Spanish — killed Weg along with weg, and Morgen along with
morgen. Every BORING entry is lower case and a German noun is not, so exact
matching separates them by construction. `p0-06` warms up **Morgen** and no
story warms up **morgen**, which is the right answer to both.

**BORING is also deliberately shorter than es-ni's.** Theirs is calibrated
against a finished 185-story course where a card for *hacer* in story 140
teaches nobody. Phase 0 is where gehen, kommen and sagen are being taught for
the first time, so only the structural words are banned and the ownership
ranking sinks the ubiquitous ones on its own.

## 14. `schedule.py` — DONE, and it found 37 real things

The recycling gate, ported with es-ni's numbers intact: **coverage 88%**
ramping from 60%, **density 5**, **return 6 later stories**.

**It fired on 15 of the 16 stories the first time it ran, and it was right.**
40 warm-up words were used three or four times where the rule asks for five.
That is not a gate being fussy — the whole method is that a word arrives
slightly differently each time until the reader triangulates it, and four is
not five. **61 sentences were added**, each a different angle on its word
rather than a restatement. Median encounters went 4 → 5, words reaching ten
went 168 → 175, and it is clean.

Where it stands on phase 0:

    stories    16
    running    7,525 words
    taught     620 words, median 5 encounters, 175 reach ten
    return     0 of 158 declared words judged
    schedule   clean

**Return correctly abstains.** A word is judged only once 25 stories exist
after it, and there are 16 in total. Scaling that down for a short tail is what
flagged 109 words in story one of es-ni. It will start biting in phase 1.

### Three of those 40 were the gate being wrong, and that mattered more

Before rewriting a single sentence, four words scored **zero** in stories that
are full of them. That was the gate, not the writing:

- **`ankommen(0x)`, `aussteigen(0x)`, `mitkommen(0x)`** — separable verbs. The
  gate counted token by token, so "Der Zug kommt in Luzern an" scored *kommen*
  and never *ankommen*. **`schedule.py` now uses `forms.separable_bindings()`,
  the Python twin of the reader's own binder**, and counts the two halves as
  one word exactly as the reader resolves them. Had that not been caught, the
  gate would have had four perfectly good stories rewritten to fix a fault in
  itself.
- **`möchten(0x)`** — *möchte* resolved to **mögen**, because it genuinely is
  mögen's Konjunktiv II and `forms.py` states it as such. Correct German, wrong
  answer for a learner: the course teaches möchten as its own word, the polite
  want. Pinned in `forms-overrides.json`.

**Keep the twin in step.** If `separableBindings()` in the app's engine.js ever
changes, `separable_bindings()` in `forms.py` has to change with it, or the
gate starts judging stories on a reading nobody gets.

### What it does NOT measure, and should not be made to

The gate counts **occurrences**; the app records **one exposure per word per
lesson read**. Those are different on purpose. Density serves the inference —
five contexts inside one story is what lets the meaning be worked out. Return
serves the memory model — it is later stories that turn five contexts into
spaced encounters. Do not "fix" one to match the other.

## 13. The stranded prefix — SETTLED 2026-08-25, and it is built

    Ich steige in Zürich um.

*steige* and *um* are four words apart and can be twelve. Kevin was given the
choice between accepting that and resolving at sentence level, and chose:
*"Do whatever teaches you the proper language."* So it is built.

**`separableBindings()` in the app's `engine.js`** joins them, using German's
own bracket: **a stranded prefix sits at the end of its clause.** Look at the
last word of each clause; if it is a prefix that would build a real separable
verb out of an earlier verb in the same clause, the two are one word. Both
halves resolve to the separable lemma, both take the `.wsep` marker, and both
count as one exposure.

**The end-of-clause rule is the whole reason it is safe.** The naive version —
any prefix-looking word anywhere after a verb — gets these wrong, and they are
not rare:

| | naive | correct |
|---|---|---|
| Ich stehe **auf** dem Perron. | aufstehen | nothing, *auf* is a preposition |
| Ich schaue **auf** den Boden. | anschauen | nothing |
| Ein Mann kommt **an** mir vorbei. | ankommen | **vorbeikommen** |
| Eine Frau steigt **aus** einem Bus **aus**. | ambiguous | **aussteigen**, on the second aus |

All four are asserted in `engine.test.mjs`.

**Measured across phase 0: 65 sentences bind, over 17 separable verbs.** Before
this, every one of the 18 separable verbs in the course had **zero** exposures
no matter how often it was read, because only the infinitive and the participle
ever resolved. All 18 accumulate now.

`python .github/scripts/forms.py --root . --separable` is kept, but it is now
an **audit** of where brackets occur, not a thing to act on — its crude matcher
flags 80 clauses to the reader's 65, and the difference is exactly the false
positives above.

**forms.py itself does not guess and must not be made to.** For a separable
verb it emits the infinitive, the participle, and the bare finite forms mapped
to the base verb, which is correct in its own right: outside a bracket, *kommt*
is kommen.

## Open, and it needs an answer before 148,000 words are written on top of it

**Nobody can fact-check the Swiss German.** For Spanish there was a native
speaker in the house. For German there is not, and Kevin is learning from
zero, so he cannot catch an error either. The gate catches mechanical things
(eszett, banned Germanisms) but it cannot catch a word that is merely wrong,
or right in Zurich and odd in Luzern.

`p0-06` is the live example: *Weggli not Brötchen*. Weggli is Swiss and that
part is safe, but whether it is the right word for that specific roll in
Luzern is exactly the class of detail that needs a checker. This was raised
with Kevin on 2026-08-24 and is **not yet resolved**. Do not quietly assume it
away.

Until it is settled, follow the es-ni discipline: anything below certain gets
flagged rather than asserted, and the flag travels with the content.

---

## Kevin's own review notes on the spine

Raised when the spine was delivered, not yet acted on:

- **`p5-01` to `p5-14` is one continuous fourteen-story thread** where Frau
  Amrein sickens, dies and is buried. It is the only place in the course where
  the plot takes the wheel that hard. Either the best thing in here or too
  much.
- **Phase 4 has 34 stories and no event in it**, deliberately. If it reads
  thin on writing, that is where to add.
- **Fasnacht appears three times**: `p1-20` as spectator, `p2-13` in a
  costume, and `p6-10` to `p6-16` from inside a Guggenmusik. Seven stories is
  a lot. Less lopsided now that Schwingen, the Alpabzug and 1. August exist,
  but still the largest single block in the course.

---

## Kevin's working preferences

Plainest possible output. No option menus for simple asks. Do exactly what he
says and do not generalise to adjacent scope. Do not over-explain after a
correction — fix it and move on. He prefers big batched updates over a stream
of small ones. He watches agent usage, so work in large batches and lean on
the gates rather than re-verifying what they have already proven.

**Never commit or push without his explicit go-ahead.**
