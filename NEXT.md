# START HERE — where the German course stands

**Nothing is written yet. The plan is finished and it is not up for
relitigating.** `content/plan/spine.json` holds all 184 stories across 8
phases, each with the German it teaches, the Switzerland it carries and what
happens in it. Read `HANDOFF.md` beside this file for every decision and the
reasoning behind it. This file is the short version and says what to do next.

| | | |
|---|---|---|
| Language | **Swiss Standard German** | code `de-ch`, repo `scenicprints/fluidez-de-ch` |
| Anchored in | **Luzern** | you land at Zurich Kloten and take the train |
| Stories planned | **184** | 8 phases, 0 written |
| App support | **shipped** | v2.8.24, mascot + palette + German interface + switcher |
| Stories on people | **60** | phases 4 and 5, a third of the course |

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
- [x] **The spine.** All 184 stories in `content/plan/spine.json`.

## What is next, in order

**1. The gates.** Nothing should be written before these exist, because the
whole method of this project is to lean on gates rather than re-check work by
hand. Port from `scenicprints/fluidez-es-ni/.github/scripts/`:

| Script | Port difficulty | What changes |
|---|---|---|
| `schedule.py` | easy | Language-agnostic already. Coverage 88%, density 5, return 6-of-25. Change the exempt part-of-speech list for German. |
| `stage.py` | easy | Reads the spine, checks story shape, writes `PROGRESS.md`. Rename the `spanish` field to `german`. |
| `build-pack.py` | easy | Bundles the pack, runs every gate. Mostly a rename job. |
| `dialect.py` | **rewrite** | Becomes the Swiss gate: no eszett, no Germanism where a Helvetism is standard, pinned spellings for the produced-dialect list. See `HANDOFF.md` §3. |
| `forms.py` | **hard, and it is the big job** | German morphology. See below. |
| `reconcile.py` | medium | Rewrites warm-ups from what a story actually hammers. Depends on `forms.py`. |
| `verbs_build.py` | medium | German verb tables. Six tenses, strong and weak verbs, separable prefixes. |

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

**2. The dictionary seed**, written alongside phase 0 rather than up front.

**3. Write phase 0**, sixteen stories, and run the loop in §7 of `HANDOFF.md`
until nothing prints `PROBLEM:`.

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
  a lot. A candidate for a cut.

---

## Kevin's working preferences

Plainest possible output. No option menus for simple asks. Do exactly what he
says and do not generalise to adjacent scope. Do not over-explain after a
correction — fix it and move on. He prefers big batched updates over a stream
of small ones. He watches agent usage, so work in large batches and lean on
the gates rather than re-verifying what they have already proven.

**Never commit or push without his explicit go-ahead.**
