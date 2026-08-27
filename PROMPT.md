# Handoff prompt

Paste the block below into a fresh session. It is deliberately short: the
detail lives in `NEXT.md` and `HANDOFF.md`, and duplicating it here would just
create a second copy to go stale.

---

You're picking up **Fluidez**, Kevin Wagner's language-learning app. Two courses exist: Nicaraguan Spanish (published, 185 stories) and Swiss Standard German (phases 0 to 4 written, 122 of 192). You're on the German one.

**Read these first, in this order.** They carry every decision and the reasoning, so nothing gets relitigated by somebody arriving cold:

- `C:\Users\jkevi\fluidez-de-ch\NEXT.md` — what to build next, in order
- `C:\Users\jkevi\fluidez-de-ch\HANDOFF.md` — the reference behind it; §10 covers the mascot and palette and what was rejected
- `C:\Users\jkevi\fluidez\README.md` — "Adding a language", the per-course architecture
- `C:\Users\jkevi\fluidez-es-ni\HANDOFF.md` and `NEXT.md` — every gate in German is a port of one of theirs, and the reasoning is written down there in full

Local clones, all on GitHub under `scenicprints`: `fluidez` (the app), `fluidez-de-ch` (German course), `fluidez-es-ni` (Spanish course), `fluidez-languages` (registry).

**Where it stands.** **Phases 0 to 4 are written and every script is built.** 122 stories, 1,905 dictionary words, 386 verbs, 44 patterns, 37 scenes, 90 Blüemli lines, an emergency phrasebook, 98.5% of the page tappable, every gate clean. CI rebuilds the pack on every push. The interface is ENGLISH — the German course ships no `ui` block, which was reversed on Kevin's call and is not up for re-translating. The app carries the mascot, palette, phase ladder and Blüemli per course from the pack.

**Next job: phase 5, Hard Things, twenty-six stories,** `p5-01` to `p5-26`. Illness, goodbyes, money, saying the difficult thing. **Frau Amrein dies in this phase**, after roughly 130 stories of correcting your recycling and feeding you anyway — that was planned from the start and `HANDOFF.md` §5 says why. **Beat**, **Fatlum** and **Vreni** arrive. The grammar is Konjunktiv II, which is still untouched, plus the systematic treatment of the subordinate clauses phase 4 introduced.

**Subordinate clauses now arrive at `p4-10`, not phase 5.** The spine asked for them in three phase 4 stories and the content required them; phases 0 to 3 and `p4-01` to `p4-09` are still clean, so the `dass` lands as an event. Konjunktiv II was kept out entirely and is phase 5's to teach. `NEXT.md` §19 carries the reasoning and it is reversible.

**Three things every phase has now taught, in the same order.** RETURN judges the previous phase's vocabulary the moment the new one lands and takes warm-up cards away: 44, then 28, then 32 across a phase half again as long. **Budget the recycling sweep as part of writing the phase.** Every sweep then breaks one or two words that relied on being one-scene, so re-run the check after it, every time — three for three so far. And adding a word can break one that already resolved, by making a form ambiguous.

**The hard rules:**

- **Swiss Standard German only.** Not dialect, not German German. One variety start to finish — Kevin killed a dialect-comprehension ramp because it makes a beginner unlearn and relearn.
- **No eszett, ever.** Always ss.
- **Never weaken a gate to make content pass.** If a gate fires, ask whether the content is wrong. It usually is.
- **A word is learned by meeting it five or six times in different situations.** The inference is the learning, not the translation. Every gate serves that and nothing else.

**Run after every change, and commit only when nothing prints `PROBLEM`:**

```
cd C:\Users\jkevi\fluidez-de-ch
python .github/scripts/stage.py --root .
python .github/scripts/dialect_test.py
python .github/scripts/verbs_test.py
```

`stage.py` runs the Swiss gate, the verb gate, `forms.py` and `schedule.py` in one pass. After changing stories also run `reconcile.py --root .`, which rewrites the warm-ups from the text, then `build-pack.py --root .`, which refuses to write the pack if a gate fires.

**Traps that have already cost hours:**

- The console is cp1252 and prints umlauts as `?`. Write results to a file and read the file rather than trusting the terminal.
- Shell heredocs mangle accented characters. Write Python and JSON with a file-writing tool.
- Python's `/tmp` is not the bash `/tmp` on this machine. Use relative paths.
- A language switcher that looks missing is the registry, not the code — every switcher hides itself when `fluidez-languages` lists one language.
- `git pull --rebase` before pushing a content repo; CI commits the rebuilt pack back to main.

**Settled, do not reopen.** The stranded separable prefix is resolved at sentence level in the reader (`separableBindings()` in the app's `engine.js`) — Kevin chose that over living with the limitation. The verb trainer is principal parts, not a conjugation table. The interface is English. `NEXT.md` §11, §13 and `HANDOFF.md` §10 carry the reasoning.

**Still open, and it is the biggest risk in the project:** nobody can fact-check the Swiss German. Phase 0 is 7,500 running words of it, including judgement calls no gate can catch — *Kaffee crème* as the default order, *Schale* as the milky one, and the Swiss perfect auxiliary (*ich bin gestanden / gesessen / gelegen*, which is southern and Swiss and would be *habe* in Hamburg). Flag anything below certain rather than asserting it, and keep the flag with the content.

**How Kevin works.** Plainest possible output. No option menus for simple asks. Do exactly what he says and do not generalise to adjacent scope. Do not over-explain after a correction — fix it and move on. He prefers big batched updates over a stream of small ones, and he watches agent usage, so lean on the gates rather than re-verifying what they have already proven.

**Push when a phase is finished.** That is his standing instruction, given 2026-08-26: *"we should be pushing after each phase is complete."* A finished phase means the stories, dictionary, verbs, patterns and scenes are all written, every gate is clean and the pack builds. Do not sit on it waiting to be asked. Anything smaller than a finished phase, or anything outside the content repos, still needs his go-ahead.
