# START HERE — where the German course stands

**THE COURSE IS WRITTEN. All 192 stories, phases 0 to 7, finished
2026-09-01.** `content/plan/spine.json` holds all 192 stories across 8
phases, each with the German it teaches, the Switzerland it carries and what
happens in it. Read `HANDOFF.md` beside this file for every decision and the
reasoning behind it. This file is the short version and says what to do next.

| | | |
|---|---|---|
| Language | **Swiss Standard German** | code `de-ch`, repo `scenicprints/fluidez-de-ch` |
| Anchored in | **Luzern** | you land at Zurich Kloten and take the train |
| Stories written | **192 of 192** | 8 phases, 117,863 running words, all complete |
| App support | **shipped** | v2.8.38, mascot + palette + English interface + switcher |
| Stories on people | **62** | phases 4 and 5, a third of the course, both written |

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

## 23. Phase 7 — Belonging, 18 stories, DONE 2026-09-01. The course is written.

**192 of 192.** 117,863 running words, 2,420 dictionary words, 530 verbs, 67
patterns, 56 scenes, 117 Blüemli lines, 484 warm-up words, 98.5% of the page
tappable, every gate clean.

| | | |
|---|---|---|
| Stories | **192** total | 18 new, 14,469 running words |
| Dictionary | **2,420** | +104 |
| Verbs | **530** | +36 |
| Patterns | **67** | +5 |
| Scenes | **56** | +5 |
| Blüemli | **117** lines | +9 |

Five years on. You give somebody directions without thinking about it, you say
a whole paragraph and afterwards cannot remember which language it was in, and
you make a pun that only works in German. Kurt asks your opinion about
something that matters to him, because you are the only person in that family
who wants nothing from him. Timo gets married and you give a speech in German
with two grammar mistakes in it that nobody notices.

Then **Anna arrives**, three weeks into the country, and the second half of the
phase is the whole course handed over: the rubbish, the laundry rota, why
Grüezi matters, why nobody has invited her yet and how long that takes, an
evening telling her about Frau Amrein, and a lamp in the Brockenhaus that she
does not buy. In `p7-16` you give her your first notebook, and about a third of
it is wrong.

**`p7-18` is the ending the plan has had since 2026-08-24.** Five people at a
table on a warm evening and nobody switches to English all night. Nobody
announces it. The protagonist does not say it out loud, because saying it would
put them all back to watching for it.

### What the last phase taught

- **The final sweep was 11 cards** — 44, 28, 32, 10, 16, 11. It is the last one,
  because there is no phase 8 to judge phase 7's vocabulary. **Phase 7's own
  words have never been through RETURN and never will be.** That is a real hole
  and it is structural: anything introduced in the last eighteen stories is
  taught once and not tested by the gate. If the course is ever extended, run
  the sweep again first.
- **Anna is the mechanism that made the phase writable.** Half of what the
  learner has been taught can only be said out loud by explaining it to
  somebody newer. `p7-09` to `p7-11` are the earlier phases said back, and the
  protagonist catches himself defending a laundry rota he spent two years
  complaining about.
- **The two puns are real German and they pay off phase 3.** *umfahren* and
  *übersetzen* mean opposite things depending on whether the prefix comes off,
  which is exactly the separable-verb rule the course has taught since `p3-01`.
- **The famous dialect word for a kitchen cupboard is deliberately not
  written.** `p7-03` names the situation, says foreigners are asked to say it,
  and refuses to spell it. Rule 4 has no exceptions and the story is better for
  the refusal.

### Known, and worth flagging

- **`würde` opens the card for `werden`** in the reader, glossed "to become".
  It is correct — würde is werden's Konjunktiv II — and it reads oddly the
  first time. The `an_deiner_stelle` pattern card carries the explanation. Not
  worth a second entry.
- **`Zivilstandsamt`, `Trauzeuge` and the two-part wedding** are the usual
  class of unverifiable detail. So is the claim in `p7-07` that the church
  ceremony is now often skipped.
- **`aufpassen` and `aufwachen` finished the course at one use each**, seven
  phases running. They are in the dictionary and they are effectively untaught.
  Either drop them or find them a home if the course is ever extended.

### What is left

The writing is done. What is not done:

1. **Nobody has fact-checked the Swiss German.** This is the same open item it
   was on day one and it is now 117,863 words long. Everything flagged in these
   sections is a judgement call by somebody who cannot verify it.
2. **A full read-through by a learner.** The gates check shape, vocabulary,
   recycling and Swissness. Nothing checks whether a story is good.
3. **Phase 7's vocabulary is untested by RETURN**, as above.

## 22. Phase 6 — Sounding Swiss, 26 stories, DONE 2026-08-31

The light phase after the heavy one, and the one that finally teaches the words
that have been on every page since story one without ever being named.

| | | |
|---|---|---|
| Stories | **174** total | 26 new, 18,574 running words |
| Dictionary | **2,316** | +241 |
| Verbs | **494** | +64, every form stated |
| Patterns | **62** | +9 |
| Scenes | **51** | +6 |
| Blüemli | **108** lines | +9 |
| Tappable | **98.6%** whole course | |
| Warm-ups | 471 words, 0 stories with none | |

**halt, eben, doch and mal** get a story each, then understatement, being
teased, dry humour, and complaining as a social form. `p6-10` to `p6-16` are
Fasnacht from inside a Guggenmusik: the weekly rehearsal from November, playing
badly in public, the mask, the Urknall at five in the morning, confetti in a
jacket in July, six days that run together, and a town that is clean by nine on
Ash Wednesday. Then swearing at the local strength, the Germans, Zurich, the
Röstigraben, the first of August, alphorn and yodelling as clubs with
committees, voting, and the last two: how an opinion is put down loosely, and
Nuno saying *du tönst schon fast wie einer von hier*.

**Beat pays off exactly as `p5-18` set him up.** He hands nobody an
instrument twice; the drum arrived in phase 5 and `p6-10` is the season that
follows it. Margrit, seventy-one and forty-four years in the band, is the only
new person of any weight, and she gets the moment the whole phase turns on.

### What the phase taught about writing the next one

- **The particle stories cannot be grammar lessons.** Each one had to arrive
  through an event — a cancelled train, two men in a courtyard, a shut window,
  a plate of food — or the story is a table with sentences round it. `p6-02` is
  the test case: an entire negotiation in forty words, six of them *eben*.
- **The sweep was 16 cards, up from 10.** Higher than phase 5 because phase 6
  moves away from the flat and the funeral, so phase 5's own vocabulary aged
  fast: `Abdankung`, `sterben`, `Kiste`, `Kasten` and `leider` all needed
  putting back. 50 sentences closed it, and the re-run came back clean.
- **A word that is hard to bring back is not exempt.** Nobody mentions a
  funeral service casually. It still has to return or it is taught once and
  forgotten, and there were four honest places for it: the same church at
  Aschermittwoch, Herr Bucher on the stairs, and the Jodelklub, who sing at
  them.
- **`halt` needed a dictionary entry and it collides with `halten`.** The
  particle is on nearly every page of this phase; `halt` is also halten's du
  imperative. The particle wins the exact-spelling lookup, `halte` is pinned
  back to halten, and both were checked in the reader. Worth knowing before
  anybody "fixes" it.
- **A line exemption carries a POSITION and the sweep moves it.** `p6-21`'s
  Bürgersteig line was exempt at `#52`, and inserting sweep sentences pushed it
  to `#54`, so the gate fired on content that was already approved. **Fix the
  number after the sweep, not before**, and re-run.

### Known, and worth flagging

- **`Grinde`, `Räppli`, `Sujet`, `Hock` and `Seich` are Luzern words** written
  the way the local papers write them. All attested, none verifiable from here.
  `p6-12` names Basel's `Larve` beside Grinde, and `p6-14` names Konfetti, so
  the learner has both halves.
- **`Couvert` is what `p6-24` teaches for the voting envelope**, and phase 5's
  `p5-14` used `Umschlag`. Both are used in Switzerland; Couvert is the more
  Swiss and Kuvert was already in the dictionary. Not a contradiction, and not
  a thing anybody here can settle.
- **`Weichmacher` for a softening word** is my label rather than a term
  anybody uses. It is glossed and it is honest, and if it reads as jargon it
  can go.
- **The Urknall detail is from the public account of it**, not from having
  stood there: five o'clock, Schmutziger Donnerstag, in the dark. Same class of
  risk as everything else in this phase.
- **`aufpassen` and `aufwachen` have now gone six phases at one use each.**
  Phase 7 or drop them. Sixth time of writing this line.

## 21. Phase 5 — Hard Things, 26 stories, DONE 2026-08-28

The phase the cast was planned around. **Frau Amrein dies in `p5-07`**, after
128 stories of correcting your recycling and feeding you anyway, and the
fourteen stories from `p5-01` to `p5-14` are one continuous thread: the shut
door, the ward, the visits, the doctor, the favour, the death, the Hauswart in
the doorway, the condolences, the Abdankung, the notice in the paper, the flat
emptied in a morning, the sister, and one photograph in an envelope.

| | | |
|---|---|---|
| Stories | **148** total | 26 new, 17,713 running words |
| Dictionary | **2,075** | +170 |
| Verbs | **430** | +44, every form stated, Konjunktiv II on six more |
| Patterns | **53** | +9 |
| Scenes | **45** | +8 |
| Blüemli | **99** lines | +9 |
| Tappable | **98.5%** whole course | |
| Warm-ups | 440 words, 0 stories with none | |

**Beat**, **Fatlum** and **Vreni** arrive. Beat rings once, says when he is
coming and hangs up, which is the second way people help here and the one that
costs the person being helped nothing. Fatlum has answered *woher kommst du
wirklich* four thousand times and answers it again. Vreni has the same voice as
her sister, lives twenty minutes away, and saw her twice a year.

### The grammar, and where it lands

**Konjunktiv II arrives in `p5-06`**, in the story where a woman who does not
ask for anything takes four minutes to ask for something. That is the whole
argument for putting it there: hätte, wäre, könnte and würde are not politeness
decoration, they are **what leaves the other person room to say no**, and the
first time you meet them should be the time somebody needs them.

`p5-01` to `p5-05` are clean of it, checked by a scan rather than by reading.
The rest of the phase uses it freely, and `p5-25` is the full treatment.

The **passive** is `p5-12`, where a flat is emptied and nobody is named, and
`p5-04`, where a doctor can only say what is being done. Subordinate clauses
run through the whole phase, which is what phase 4's `p4-10` opened the door
for.

### What the phase taught about writing the next one

- **The recycling sweep was 10 cards, against 44, 28 and 32.** Not because the
  gate relaxed — because this phase was written knowing it was coming, and
  carried the flat, the building, the Zeitung and the Friedhof forward on
  purpose. 36 sentences closed it. The number falls when the writing does the
  work, exactly as phase 3 predicted.
- **And the sweep broke nothing this time.** Three phases running it took one
  or two words down with it; this is the first time re-running it came back
  zero. Re-run it anyway. It costs one command.
- **A phase full of subordinate clauses exposed a real hole in `forms.py`.**
  A separable verb goes back together at the end of a subordinate clause —
  *weil er anfängt*, *dass es mich betrifft* — and the joined form was emitted
  nowhere, so it resolved to nothing. It is generated now, from the stated
  parts, and claimed for the separable verb rather than its base, because the
  prefix is right there on the word. Same class of bug as phase 1's epenthetic
  e: a rule that was right for the shapes the course happened to contain, until
  the course contained a new shape.
- **Ordinals declined nowhere either.** `viert`, `sechst`, `zwanzigst` are
  stored as stems and *der vierte* is genuinely regular, so it is ruled now.
- **Adding two verbs cost two words their mapping**, exactly as `meinen` cost
  `meine` in phase 2. `ansprechen` made `spricht` ambiguous with `aussprechen`,
  and `ausladen` made `lädt` ambiguous with `einladen`. Both are pinned. **Read
  the AMBIGUOUS list after every batch**, three phases running now.
- **The course teaches `reden` and not `sprechen`**, which came out of that
  check: `sprechen` has never had a dictionary entry and `spricht` occurs once
  in 148 stories. That is Swiss and it looks deliberate. Left alone.

### Known, and worth flagging

- **`Abdankung` is what the spine asked for and it is the word in the notices.**
  It is used across Switzerland; it is more at home in a Reformed parish than a
  Catholic one, and Rosmarie goes to church every Sunday in Catholic Luzern.
  `p5-10` names **Beerdigung** and **Trauerfeier** in the same breath, so the
  learner has all three. **Below certain, and flagged rather than asserted.**
- **`Leidmahl`** for the meal afterwards, **`Hock`** for the sit-down after a
  rehearsal, and **`Ambulanz`** beside Krankenwagen are the same class of call:
  attested, ordinary, and unverifiable from here.
- **Eleven flowers and never thirteen**, from the shop in the hospital. Stated
  as a rule rather than as superstition because that is how it was described.
  Nobody in the project can check it.
- **`aufpassen` and `aufwachen` have now gone five phases at one use each.**
  Phase 6 or drop them. This is the fifth time this line has been written.
- **`Stock` is still a floor and a ski pole.**

## 20. The download banner that would not go away — FIXED 2026-08-27

Reported by a tester on Chrome: *"the banner saying there's lessons to download
keeps popping up"*, and a weird message when he tried. Two separate faults in
the app, and they end in the same place — **the version on the device never
advances, so the app offers the same download again forever.**

**1. The pack was written to local storage twice.** `applyBundle` copied
`bundle.lessons` and `bundle.scenarios` into the `manifest` it stored, on top
of the reshaped copies it also stored. Nothing has ever read either field: the
only things anything reads out of a cached manifest are `version`, `features`
and the phrasebook. The cost, measured rather than guessed:

| stored pack | was | is |
|---|---|---|
| de-ch | 4.34 MB | **2.43 MB** |
| es-ni | 5.99 MB | 3.49 MB |

Those are UTF-16 bytes, which is how a browser counts its quota. **The Spanish
course alone was over a 5 MB limit.** When the write failed, `cacheWrite`
returned false, the setup screen said *"Downloaded, but this browser would not
keep it offline"* — the tester's weird message — and nothing was kept, so the
banner came back on the next launch, forever.

**2. The file-by-file fallback cached a course with no version at all.** If
`pack.json` does not come down — 1.7 MB against a 20 second timeout on a phone,
or a 429 from raw.githubusercontent — the app assembles the course from 160
separate files and stored `manifest.json` as its manifest. **Neither course has
ever had a `version` in `manifest.json`**, so `packVersion()` answered null and
null can never equal the live version. That path now takes its version from
`content/version.json`, the same sidecar the update check reads.

### What is in the app now

- **The version stamp is its own key**, `fl:c:ver:<code>`, about forty bytes,
  and it is written **only when the pack write actually succeeded**. A version
  we did not manage to store is a version we do not have. It also means the
  "anything new?" question on every launch stopped parsing two megabytes.
- **A pack that will not fit evicts the OTHER course's pack and retries.** The
  course you are not reading costs one download to get back.
- **If it still will not fit, the version is recorded in `fl:c:nofit:<code>`
  and the banner stops offering it.** A banner you cannot dismiss by doing what
  it asks is the worst thing a banner can be. Settings still checks and
  downloads on request, because that is the learner asking.
- **A partial download is not stamped.** The fallback drops a file it cannot
  fetch rather than failing the lot, which is right, but stamping the version
  on it would tell the app it is up to date with stories it has never seen.
- **The phrasebook is fetched on the fallback path too.** `manifest.emergency`
  is a path there and the data in the bundle, and only the data was ever read,
  so a course assembled file by file showed the Emergency tile with nothing
  behind it.

`docs/js/content.test.mjs` covers all of it, including a storage stub that
throws over a byte budget, and CI runs it. **The one thing not verified in a
real browser is the eviction**: the Browser pane's local storage swallowed 51
MB without complaining, so the quota path cannot be provoked there. It is
asserted in the test and reasoned from the code, not watched happening.

**Do not put anything back in the stored manifest that no screen reads.**

## 19. Phase 4 — Close to the Heart, 36 stories, DONE 2026-08-27

The largest phase in the course and the one `HANDOFF.md` §1 says the whole
thing exists for.

| | | |
|---|---|---|
| Stories | **122** total | 36 new, 20,400 running words |
| Dictionary | **1,905** | +326 |
| Verbs | **386** | +90, every form stated |
| Patterns | **44** | +9 |
| Scenes | **37** | +9 |
| Blüemli | **90** lines | +9 |
| Tappable | **98.5%** whole course | |
| Warm-ups | 548 words, 0 stories with none | |

Selina, four hours of conversation you cannot afterwards remember, and three
things you can. **The Odermatts arrive**: Kurt, who asks two questions in five
hours and both of them matter; Marianne, who asks forty and one of them is
about your pension; Reto, who is rude exactly once and is not defended; and
Hedi at ninety-one, who tells a stranger the thing she has never told her own
daughter, because a stranger is a safe place for a story.

The phase is the emotional register: the first argument nobody raises their
voice in, an apology that has to name the thing, two days of silence that both
people think they are giving as a kindness, a permit with a date on it, and a
sentence about ten years' time said while cleaning a floor.

### The call that had to be made, and it is reversible

**Subordinate clauses arrive here, at `p4-10`, with a pattern card.** The
spine asks for them in three places (`dass` in `p4-10`, `wenn/dann` in
`p4-24`, "subordinate clauses under pressure" in `p4-31`), and the content
genuinely requires them: you cannot write *I thought you meant something else*
without one. `HANDOFF.md` §4 labels phase 5 "subordinate clauses, Konjunktiv
II", and this is the third phase running where the two documents disagreed.

The resolution: **phases 0 to 3 and `p4-01` to `p4-09` stay clean**, so the
`dass` in `p4-10` lands as an event and gets named on the page. **Konjunktiv
II is untouched and stays in phase 5**, along with the systematic treatment.
Flagged to Kevin at the start of the phase; reversible by rewriting nine
stories rather than thirty-six.

### What the phase taught about writing the next one

- **The recycling number is now a per-story rate, and it is falling.** 44 cards
  after phase 2, 28 after phase 3, **32 after phase 4** — but phase 4 is 36
  stories, so per story it is the lowest yet. 103 sentences closed it.
- **Every sweep breaks something.** `Glocke` fell out the moment a phase 4
  sentence mentioned bells, exactly the way `Nacht` and `Maschine` did in phase
  2 and phase 3. Re-run RETURN after the sweep, every time. It is now three for
  three.
- **A phase this size passes coverage on the first run.** Not one story fired,
  across 36. Writing 80 sentences of ordinary vocabulary around 10 new words is
  a rate that works, and it is the same rate phases 1 to 3 settled on.
- **The dialect rule bites in unexpected places.** A draft of `p4-20` wrote
  *es guets Neus* to teach the New Year greeting. Attested, and still an
  invented-orthography entry in a course that has none. Cut, and the point is
  made without it.

### Known and small

- **`Stock` is still a floor and a ski pole**, carried over from phase 3.
- **`aufpassen` and `aufwachen` have now gone four phases at one use each.**
  Phase 5 or drop them.
- **Nobody can fact-check the emotional register**, which is the same standing
  risk as the vocabulary and it is larger here. *Schade* as a heavy word,
  *im Unrecht sein* as very rare, praise arriving through three other people:
  all of it is judgement, all of it is consistent with what the earlier phases
  claim, and none of it is verified.

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
