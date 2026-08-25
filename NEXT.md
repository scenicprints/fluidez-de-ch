# START HERE — where the German course stands

**Nothing is written yet. The plan is finished and it is not up for
relitigating.** `content/plan/spine.json` holds all 192 stories across 8
phases, each with the German it teaches, the Switzerland it carries and what
happens in it. Read `HANDOFF.md` beside this file for every decision and the
reasoning behind it. This file is the short version and says what to do next.

| | | |
|---|---|---|
| Language | **Swiss Standard German** | code `de-ch`, repo `scenicprints/fluidez-de-ch` |
| Anchored in | **Luzern** | you land at Zurich Kloten and take the train |
| Stories planned | **192** | 8 phases, 0 written |
| App support | **shipped** | v2.8.25, mascot + palette + German interface + switcher |
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
| `forms.py` | **after phase 0 is written** | German morphology. It maps forms that ACTUALLY OCCUR, so it wants a real corpus to build against. Writing 16 stories first makes it a smaller, sharper job than guessing which forms matter. |
| `schedule.py` | after `forms.py` | Coverage 88%, density 5, return 6-of-25. **Blocked on `forms.py`**: without lemma resolution *spricht*, *sprach* and *gesprochen* count as three words and the arithmetic is noise. |
| `reconcile.py` | after `forms.py` | Rewrites warm-ups from what a story actually hammers. |
| `build-pack.py` | before publishing | Bundles the pack and runs every gate. Port from es-ni, which now also carries `ui`, `phases`, `mascot` and `icons` through from the manifest. |
| `verbs_build.py` | when the verb trainer is wanted | German verb tables. Strong-verb ablaut must be STATED, never rule-generated. |

**2. Phase 0, sixteen stories**, plus the dictionary entries they need. Written
un-schedule-gated, because that gate does not exist yet; re-checked once
`forms.py` and `schedule.py` land. Sixteen stories is a small enough bet that
rewriting them is cheap. Doing this to all 192 would not be.

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
  to English. The Path tab takes its own icon per course: volcano for es-ni,
  `ic-gondola` for de-ch.
- **Chrome** reads `--accent` / `--chrome-grad`, split from `--oro`, which used
  to mean both "growing" and "this app". `[data-course="de-ch"]` on `<html>`
  paints alpine night: Swiss red and white on charcoal. **The three memory
  colours are identical in both courses on purpose.**
- **`Im Bau`** screen: a course with no lessons shows its tiles but routes every
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
