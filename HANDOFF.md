# Handoff — writing the Fluidez German course

> **If you are a fresh agent, read `NEXT.md` first.** It says what to build
> next, in order, in one page. This file is the reference behind it, and it
> carries every decision made so far and why, so that nothing here gets
> relitigated by somebody arriving cold.

Decisions dated 2026-08-24 unless stated.

---

## 1. What this is and who it is for

Fluidez is Kevin Wagner's language app. The first course was Nicaraguan
Spanish. This is the second: **Swiss Standard German, anchored in Luzern.**

**The Nicaraguan course's framing was a device, not autobiography.** Its
handoff says the course exists because "his wife is Nicaraguan". Kevin's own
words on 2026-08-24: *"The whole his wife was nicaraguan was to just teach
something that other apps didn't."* The immigrant arc was the vehicle that
made teaching real regional language natural. Same vehicle here. Do not build
anything on a literal reading of the Spanish course's premise.

**What makes Fluidez different, in Kevin's words:** *"it teaches you deep
emotional connected words that other apps dont. Yes it teaches you surface
level words like Duolingo, but the heart is learning culture and connecting
with people."*

That sentence is the brief. It is why phases 4 and 5 carry sixty stories
between them, and why an early draft of the phase plan that was all logistics
and bureaucracy was rejected.

---

## 2. The variety, and the line that was drawn

**We teach Swiss Standard German.** That is a real, documented, written
standard: what Swiss newspapers, schools, signage and formal speech actually
use. It is not a compromise invented for this course.

**We do not teach dialect.** Kevin: *"I want it to be Swiss-German, but we
both know that that is impossible."* He is right. Schweizerdeutsch has no
standard orthography, varies by canton, and writing it would mean inventing
spellings.

### The dialect ramp that was proposed and killed

An early design had dialect appear as **comprehension only**, ramping through
the phases, on the argument that Swiss people speak dialect to each other and
switch to Standard German for foreigners, so the course could end when people
stop switching.

**Kevin killed it:** *"I dont think it is a good idea. to switch. You are then
making people unlearn and relearn. That is too much for a beginner. Pick one
and stick to it."*

He is right, and it removes the largest accuracy risk in the project at the
same time. **One variety, story 1 to story 192. No Mundart sentences anywhere,
comprehension included.**

### What survives

A short **pinned list** of fixed lexical items that everybody in Luzern says
inside otherwise-standard sentences. These are vocabulary, not a second
grammar, and the learner produces them from day one:

**Greetings and farewells:** Grüezi, Grüezi mitenand, Hoi, Hoi zäme, Sali,
Ade, Tschüss, Uf Wiederluege
**Courtesy:** merci, merci vielmal, bitte
**Replies:** tiptop

Two of these came from Kevin rather than from me and both were right:

- **Sali.** From French *salut*. Informal, to anyone you would du, strongest in
  Zurich, Basel, Aargau and the centre, understood everywhere.
- **Tiptop.** More useful than a greeting because it is an *answer*. *Wie
  gaht's?* gets *Tiptop* more often than anything from a textbook.
  **Honest caveat that must not be lost:** tiptop is not exclusively Swiss.
  German German has *tipptopp*. It is far more everyday in Switzerland and
  worth teaching, but it does not mark you out the way Velo or Grüezi does.
  The spelling splits usefully: Duden writes *tipptopp*, Switzerland writes
  **tiptop**, and we pin tiptop.

### The ending

Not *ya sos nica*. Switzerland does not do that. The last story, `p7-18`
**Niemand wechselt ins Englische**, is the moment four people in a
conversation carry on in German and not one of them changes language for you.
Nobody announces anything. That is the arc's finish line.

---

## 3. The gates — what will reject your work

Ported in spirit from es-ni, where every gate exists because a specific class
of error already shipped once. **Do not weaken a gate to make content pass.**
If a gate fires, first ask whether the content is wrong. It usually is.

### The Swiss gate (`dialect.py`, to be rewritten for German)

**1. No eszett. Ever.** Switzerland abolished it. Always ss. Absolute, and
mechanically checkable. Already enforced in the spine build.

**2. No Germanism where a Helvetism is the Swiss standard.**

| Say | Not |
|---|---|
| Velo | Fahrrad |
| Billett | Fahrkarte |
| Spital | Krankenhaus |
| Trottoir | Bürgersteig |
| Rahm | Sahne |
| Poulet | Hähnchen |
| Glace | Eis |
| Coiffeur | Friseur |
| parkieren | parken |
| Weggli | Brötchen |
| Gipfeli | Croissant |
| tönen | klingen |
| Znüni, Zvieri, Zmorge | Frühstück-adjacent German forms |

The list is a seed, not the finished thing. It grows as the course is written.

**3. A line that names the German word in order to teach the contrast is
exempt BY LINE, never by word.** Allowing a word globally lets a real slip
through everywhere else.

**Every line carries its own position now** (2026-08-25), so an entry names one
line rather than a whole story:

    lesson p0-06 #41       one sentence
    lesson p0-06           the whole story, if that is really what you want
    scene sc02 option 3.3  one reply on the third step

It used to be `lesson p0-06` for all ninety-odd sentences in p0-06, so
exempting the one line that teaches the contrast stopped checking the other
ninety. The coarse form still works, and `dialect_test.py` asserts it.

**Better still, do not need it.** `p0-06` teaches Weggli and Gipfeli without
ever writing the German German word in German — the contrast lives in the
English gloss and in a scene option that is marked wrong. Only two lines in the
whole of phase 0 are exempt, both of them deliberately-wrong scene answers.

`dialect.py collect()` reads lessons, scenes, mascot lines, the interface, the
phase ladder, **the emergency phrasebook and every stated verb form.** The last
two were outside the gate at first, and the phrasebook is the worst possible
place for a hole.

**4. No invented dialect spelling.** The retired `scenicprints/fluidez-gsw-lu`
repo is this failure sitting on disk: an invented Luzerndütsch orthography,
"Wohär chunsch?", "Es Kafi", "De Bahnhof". It is a cautionary example, not a
base to build on, and it should not be mined for content.

**5. One spelling per pinned word, forever.** Since no dialect spelling is
objectively correct, ours becomes the course's orthography. If Sali appears
three ways across 184 lessons it reads as sloppy rather than authentic. The
gate fails any story that spells a pinned word differently.

### The verb gate (`verbs.py`, and it has no es-ni original)

There is no gate on `verbs.json` in either course today, and that is how es-ni's
Verb Trainer taught *cerro* and *perdo* for years: the app's `conjugate()`
falls back to the regular table whenever an irregular is missing a tense, so a
hole in the data does not throw, it teaches the wrong thing quietly.

German's drill never calls `conjugate()`, so that failure is gone. The one that
replaces it is a form nobody wrote, or worse, a form somebody guessed.

1. **Every required field is present and stated.** `en`, `pres3`, `pres2`,
   `past3`, `pp`, `aux` on every verb, `aux` being `hat` or `ist` and nothing
   else. A prefix comes with a `sep`, and a separable verb writes its `pres3`
   separated.
2. **Every drilled verb is a lemma the course teaches.** A drill on a verb no
   story contains is a flashcard. With an empty dictionary this warns rather
   than fails, which is the only thing here that depends on content existing.

`verbs_test.py` fires it at 13 poisoned files and 7 good ones. The full account
of why German's drill is principal parts rather than a conjugation table is in
`NEXT.md` §11.

### The schedule gate (`schedule.py`, built 2026-08-25)

- **Coverage:** at least 88% of a story's dictionary words already introduced,
  ramping from 60% over the first 50 stories — phases 0 and 1 are 38 stories
  between them and are where the base vocabulary is built.
- **Density:** every warm-up word appears at least 5 times in its own story.
- **Return:** every declared content word reappears in at least 6 LATER
  stories, judged only once 25 stories exist after it. Function words
  (`prep art conj contr pron num`) are exempt, and so is a one-scene word.

**These three exist to serve the teaching method in §6 and nothing else.**
Understand that before touching their numbers.

**Two things German changes, and both are load-bearing:**

1. **Every lookup goes through `lemma_of`, exact spelling first.** es-ni
   lower-cases each token, which here would find no noun at all and the gate
   would silently measure the function words only.
2. **Separable verbs count as one word across their two halves**, via
   `forms.separable_bindings()`, the twin of the reader's binder. Counting
   token by token scored ankommen at zero in the story that is full of it, and
   would have had four good stories rewritten to fix a fault in the gate.

It fired on 15 of 16 stories the first time and it was right about 37 of the
40: the writing was landing at three or four uses where the rule asks for five.
61 sentences were added rather than the number being moved.

**RETURN arrives late and it arrives all at once.** A word is judged only once
25 stories exist after it, so a phase's vocabulary is unjudged while it is
being written and judged in full the moment the next phase lands. Phase 2 took
44 warm-up cards away from phases 0 and 1 on the day it was committed, and
every one of them was a real hole: the flat, the laundry and the bills had
stopped being mentioned. **Budget for that sweep as part of writing a phase**,
not as a surprise. 129 sentences closed it.

Phase 3 took **28**, and it was written knowing that would happen: 84
sentences closed it. The number falls when the writing carries the last phase
forward on purpose, and it will never reach zero, because that is simply what
a course getting longer costs. **A separable verb does not count as its base**,
either: six of those 28 closed on the first try and `bringen` did not, because
every sentence written for it said `mitbringen`.

**One-scene is a share, not a count**, and that makes it fragile in the
opposite direction: a word exempt because 60% of its uses are in its own story
loses the exemption when a later story mentions it once. Two words broke that
way during the sweep that fixed forty. Re-run the check after every sweep.

---

## 4. The eight phases

Named for what you can do, with the grammar that rides underneath. **This
ladder is German's, not the Spanish course's relabelled.** Kevin's
instruction: *"The phases should be unique to each language."*

| | Phase | Grammar underneath | Stories |
|---|---|---|---|
| 0 | Landing | der/die/das, present tense, numbers | 16 |
| 1 | Settling In | modal verbs, accusative, verb second | 22 |
| 2 | Making Friends | perfect tense, dative | 27 |
| 3 | Getting About | separable verbs, two-way prepositions | 21 |
| 4 | **Close to the Heart** | the emotional register | **36** |
| 5 | Hard Things | subordinate clauses, Konjunktiv II | 26 |
| 6 | Sounding Swiss | Modalpartikeln: halt, eben, doch, mal | 26 |
| 7 | Belonging | passive, idiom, the long tail | 18 |

**The order is Kevin's**, and it is narrative: you land, you settle into a
flat, you make friends, and only then do you go out and see the country, with
them. It replaced an earlier order that had Getting About at position 1.

**Do not reorder it.** Three things depend on it:

- **Two-way prepositions need both cases first.** *In die Stadt* versus *in
  der Stadt* cannot be taught before accusative (phase 1) and dative (phase 2)
  are in hand. The original order taught them in phase 1, out of two cases the
  learner had not met. Kevin's reorder fixed a real bug.
- **The Hausordnung is modal verbs and nothing else.** *Man darf nach zehn
  nicht duschen. Du musst die Waschküche eintragen.* Settling In at position 1
  means the building teaches you the grammar.
- **Getting About is where you meet Selina.** A light phase between two heavy
  ones, and the hinge into phase 4.

**Phase names are hardcoded in the app**, in `PHASES` in
`scenicprints/fluidez/docs/js/engine.js`, and currently read Nicaragua's.
Moving them into the content pack is an app-repo job. See `NEXT.md` §4.

---

## 5. The cast

**Planned with its endings already known**, because a funeral in phase 5 for
somebody introduced in phase 5 is a vocabulary exercise, while a funeral for
the woman across the landing who has been correcting your recycling since
story 17 is the thing this app exists to do.

| Who | Arrives | What they are |
|---|---|---|
| **Frau Amrein** | Phase 1 | Seventies, the flat across the landing. Explains the Hausordnung whether you asked or not, judges your recycling, feeds you anyway. The building's newspaper. **Dies in phase 5**, after roughly 130 stories. |
| **Ruedi Zemp** | Phase 1 | The Hauswart. Rules are rules. Thaws at about one degree per phase and the learner notices the exact moment. |
| **Lea** | Phase 0 | Mid twenties, works the café. First person your own age who speaks to you like a person. |
| **Nuno** | Phase 1 | Portuguese, eighteen years in Luzern, kitchen work. Cheerfully wrong about cases. Your first real friend, because he remembers arriving. A quarter of Switzerland was born somewhere else and pretending otherwise would be a lie. |
| **Timo** | Phase 2 | Your age, from Stans. Owns Getting About. |
| **Selina** | Phase 3 | Comes along on one of Timo's trips. Phase 4 is her. |
| **The Odermatts** | Phase 4 | Her parents, in Kriens. Sunday lunch, and being assessed. |
| **Beat** | Phase 5 | Guggenmusik and a Verein. Pulls you back out of grief without asking how you are. |
| **Fatlum** | Phase 5 | Born in Luzern, Kosovar name, Swiss in every way that counts, still gets asked where he is really from. |
| **Vreni** | Phase 5 | Frau Amrein's sister. Turns up after, and is not a replacement. |
| **Anna** | Phase 7 | The next arrival. You hand her the notebook. |

**The protagonist has no backstory and needs none.** An early draft asked
whether they arrive on a work permit, as a student, or following a partner.
Kevin: *"I dont think this actually matters. You are just there."* Do not
invent one.

---

## 6. How the app actually teaches, in Kevin's words

This is the most important section in this file, and it was got wrong once
already by describing the machinery instead of the method.

> *"You learn words because when you are reading you see the same word several
> times in different contexts. While you are figuring out the word you have to
> think through the context what that word means and that is how you learn it
> and figure it out."*

**The inference is the learning.** Not the translation, not the flashcard. The
word arrives slightly differently each time, the learner triangulates it, and
by the sixth meeting they own it because they built the meaning themselves.

Everything in the build protects that:

- **Coverage 88%** so there is enough known context around a new word to
  squeeze meaning out of it.
- **Density 5** so the word comes back inside the same story from a different
  angle.
- **Return 6-of-25** so it keeps coming back afterwards.
- **The English stays hidden per line** in the reader, because reading the
  translation is skipping the inference.
- **Tapping a word counts against you** in the memory model, because tapping
  is skipping the inference.
- **Reading alone caps memory strength at 0.79**, just under "Locked in".
  Green means "I have produced this", not "this went past my eyes".

### What that means for writing German specifically

**Repetition must be varied repetition.** Five sentences using *Zug* the same
way teach nothing. *Zug* in a ticket queue, *Zug* missed, *Zug* delayed,
somebody's *Zug* to work, the last *Zug* home. Different grammatical slots so
the form varies with it: *der Zug*, *den Zug*, *mit dem Zug*, *die Züge*.
Each meeting is a different problem.

**German gives two levers Spanish did not have:**

- **Compounds are inferable.** Once *waschen* and *Küche* are solid,
  *Waschküche* cracks itself open. Teach the parts well and the learner
  decodes words the course never taught them. The early phases should be dense
  in the pieces that build things.
- **Separable verbs teach themselves through context.** *Ich steige in Zürich
  um.* The *um* is stranded at the end and nobody has to explain that. Seeing
  it happen a dozen times lands the pattern. Explaining it up front would be
  worse.
  **And the reader now shows it happening.** `separableBindings()` marks both
  halves and opens the same card from either, so the stray little word at the
  end is visibly the front of the verb. Sixty-five sentences in phase 0 do it.
  See `NEXT.md` §13 — it was very nearly shipped as a known limitation, and
  Kevin's call was *"do whatever teaches you the proper language."*

---

## 7. The loop for writing content

Same as es-ni's, and it exists so nobody hand-verifies what a gate has already
proven:

1. **Write** the JSON. Emit a batch from one throwaway Python file rather than
   one tool call each.
2. `python .github/scripts/stage.py --root .`
3. **Add the dictionary entries** it lists in `content/plan/needs-entry.txt`.
   Lemmas only. Skip proper nouns.
4. `python .github/scripts/reconcile.py --root .` — rewrites every warm-up
   from the text, so a warm-up can never claim a word the story does not teach.
   It is idempotent, and `--dry-run` shows what it would change. **It gives each
   word to the story that owns it most**, not to the first one that qualifies,
   which is what stops "Der See" losing `See` to a lake glimpsed from a train
   eight stories earlier. See `NEXT.md` §15.
5. Repeat 2 until there are no `PROBLEM:` lines, then commit.

**`git pull --rebase` before pushing.** CI commits the rebuilt pack back to
main, so a plain push is rejected.

---

## 8. Traps already paid for, on this machine

Inherited from es-ni and all still true:

- **Shell heredocs mangle apostrophes and accents here.** Write Python and
  JSON with a file-writing tool, never `bash <<'EOF'` with accented content.
  This matters more in German than in Spanish because of the umlauts.
- **Console output is cp1252** and accented characters print as `?`. Write
  results to a file and read the file rather than trusting the terminal.
- **`/tmp` in Python is not the bash `/tmp`.** Use relative paths.
- **Every form `forms.py` produces is either STATED or genuinely regular.**
  The suppletive presents (sein, haben, werden, tun, the modals), noun plurals
  and the umlauting comparatives are written out; only the endings that never
  vary are ruled. `IRREGULAR_PRESENT` exists because ruling *sein* produced
  *seie* and *seit* and lost **sind** and **bin** entirely.
- **Never let a conjugated form or a plural be its own dictionary entry** when
  the lemma exists. In es-ni 62 were, and the commonest verbs in the language
  each had their memory split in two. German will be worse: every strong verb
  has four principal parts and every noun has a plural.
- **Irregulars must be stated, never rule-generated.** es-ni's verb tables
  turned *estar* into *esto*. German strong verbs will do the same thing with
  ablaut if a rule is allowed near them.
- **To check a change in the real app**, seed `localStorage` and reload. The
  cached pack lives at `fl:c:pack:de-ch` and is stored in `applyPack` shape,
  not the shape `pack.json` ships: `dictionary` becomes `dict`, lessons get
  `sentences` from `sn` and `warmup` from `wu`. Seed it raw and nothing is
  tappable and no story will open. Writes to Firestore are already blocked on
  localhost.

---

## 9. Where everything lives

| What | Where |
|---|---|
| This repo (the German course) | `scenicprints/fluidez-de-ch` (not yet created) |
| The app | `scenicprints/fluidez` |
| The Spanish course, and the reference for every script | `scenicprints/fluidez-es-ni` |
| Language registry | `scenicprints/fluidez-languages` |
| Retired Swiss dialect attempt, do not mine | `scenicprints/fluidez-gsw-lu` |
| Live app | https://scenicprints.github.io/fluidez/ |

**Read `scenicprints/fluidez-es-ni/HANDOFF.md` and `NEXT.md`.** Every gate in
this project is a port of one of theirs, and the reasoning for each is written
down there in full. Do not rediscover it.

---

## 10. The look, and how it was arrived at

Decided 2026-08-25, on Kevin's call after several rejected passes. Recorded
because none of it is recoverable from the code.

### Bluemli, the mascot

A **Braunvieh** cow, the breed of central Switzerland, not the black and white
Holstein people picture from abroad. Named Bluemli, a real traditional Swiss
cow name, and the `-li` diminutive is the most Swiss German thing in the app.
Same trick Momo plays by being Nicaragua's national bird.

**Why a cow, when a marmot was drawn first and recommended.** The bell. Momo's
entire idle is a racket-tipped tail swinging like a pendulum, and a bell on a
strap is that same motion except a bell is meant to swing, so it inherits the
best mechanical idea in the app for free. Kevin also caught that "it is a
cliche" does not survive the precedent: Momo is the postcard animal of
Nicaragua and that works fine.

**Rejected, with reasons, so they are not re-proposed:**

| | Why not |
|---|---|
| **Mungg**, alpine marmot | Genuinely good, still drawn, parked in `creatures.js` as a one-line swap. Its advantages are aesthetic; the cow's are mechanical. |
| **Alpendohle**, alpine chough | A bird, so every animation ports untouched and it is cheaper. But two courses in a row with a bird makes the app feel like one course in two hats. |
| **Pilatus dragon** | The most Luzern-specific option, but invented rather than observed. What makes Momo work is that his idle is real motmot behaviour. |
| **Steinbock** | Majestic rather than warm, and the horns are illegible at forty pixels. |

**Three drawing passes were rejected before the fourth landed.** Written down
so a redraw does not reintroduce them:

- The head was nearly square. A cow's is **tall**, roughly half skull and half
  muzzle, narrowing through the cheek before the nose pad flares again.
- Every form was one flat fill. Momo reads round because each shape carries a
  lighter cap and a darker trailing edge. Without that it is clip art.
- The muzzle was a rounded rectangle. It is a flared pad with a philtrum groove
  and kidney nostrils that open outward.
- The ears pointed straight out sideways. They sweep out **and down**, and they
  join the skull rather than floating beside it.
- The collar was a flat trapezoid with two straight stripes, which read as a
  flag, and it sat inside the swinging group so the strap rotated with the
  bell. **The collar is static and only the bell swings.**

### Alpine night

**Swiss red and white on neutral charcoal.** Two earlier attempts failed and
both failures are instructive:

1. **Cooling the ground only.** The grounds went warm-black to cool charcoal
   and Kevin correctly said it looked unchanged, because `--oro` was painting
   every button, tab, ring, glow and chip, and gold-on-dark *is* the Nicaraguan
   signature. Changing what sits underneath a loud accent changes nothing.
2. **Glacier blue.** Exactly backwards: **blue and white is Nicaragua's own
   flag**, so it made the second course look more like the first. Switzerland's
   colour is red.

**The fix that made it possible** is an improvement to the app regardless of
palette: `--oro` was doing two jobs, meaning both "growing" in the memory model
and "this app" as the brand colour, so no second course could be repainted
without changing what a colour *means*. Chrome now reads `--accent` and
`--chrome-grad`; the memory ramp keeps `--oro`.

**The rule that constrains any future palette:** the three memory-strength
colours (jade locked in, gold growing, clay fading) are **identical in every
course, on purpose**. A locked-in word looks the same whatever you are
learning. Identity lives in the ground, the text and the chrome. Do not tint
the memory colours per language.

The chrome is a red/white gradient with white compressed into the first ~40%,
so a white label always sits on red. Worn by the primary button, level chip,
active tab pill, streak ring, progress bar, perch glow, the under-construction title and
the picker selection. **Not** by ghost buttons, or the primary stops meaning
anything.

### The interface is ENGLISH

**Reversed 2026-08-25 on Kevin's own call, looking at it:** *"All of the tiles
are in german. Why is the UI in German? It should be English."*

It shipped German first (Heute, Weg, Szenen, Woerter, Wiederholen, Wortstellung,
Nachsprechen, plus German phase names) on the reasoning that a beginner meets a
dozen interface words on day one and never looks them up again. That is wrong
here, and the Spanish precedent is what hid it: es-ni's interface is in Spanish
and it reads fine **because he already reads Spanish.** He is learning German
from zero, so a German interface is not a dozen free words, it is the whole
frame of the app being unreadable while he is trying to read a story.

**The German course ships no `ui` block at all.** `t()` falls back to the `EN`
table in the app's `js/ui.js`, so there is nothing here to keep in step with
the app's own strings. The phase ladder is English too: Landing, Settling In,
Making Friends, Getting About, Close to the Heart, Hard Things, Sounding Swiss,
Belonging. Do not re-translate any of it.

The one thing that stays German is **the content**: story titles, the lesson
text, the scenes. That is the course.

The Path tab carries its own icon per course: a volcano for Nicaragua, a
**gondola** (`ic-gondola`) for Switzerland.

### Under construction

A cable car climbing over a fogged valley. Every tile of a course with no
lessons lands there. The screen said **Im Bau** while the interface was German;
it reads "Under construction" now, along with the rest of it. Governed by `underConstruction()` in `content.js`, which
is just `content.lessons.length === 0`, so **it disappears on its own the
moment phase 0 publishes.** Nobody has to remember to remove it.
