# Handoff prompt

Paste the block below into a fresh session. It is deliberately short: the
detail lives in `NEXT.md` and `HANDOFF.md`, and duplicating it here would just
create a second copy to go stale.

---

You're picking up **Fluidez**, Kevin Wagner's language-learning app. Two courses exist: Nicaraguan Spanish (published, 185 stories) and Swiss Standard German (**finished**, 192 of 192). You're on the German one.

**Read these first, in this order.** They carry every decision and the reasoning, so nothing gets relitigated by somebody arriving cold:

- `C:\Users\jkevi\fluidez-de-ch\NEXT.md` — what to build next, in order
- `C:\Users\jkevi\fluidez-de-ch\HANDOFF.md` — the reference behind it; §10 covers the mascot and palette and what was rejected
- `C:\Users\jkevi\fluidez\README.md` — "Adding a language", the per-course architecture
- `C:\Users\jkevi\fluidez-es-ni\HANDOFF.md` and `NEXT.md` — every gate in German is a port of one of theirs, and the reasoning is written down there in full

Local clones, all on GitHub under `scenicprints`: `fluidez` (the app), `fluidez-de-ch` (German course), `fluidez-es-ni` (Spanish course), `fluidez-languages` (registry).

**Where it stands.** **THE COURSE IS WRITTEN.** All 192 stories, 117,863 running words, 2,420 dictionary words, 530 verbs, 67 patterns, 56 scenes, 117 Blüemli lines, an emergency phrasebook, 98.5% of the page tappable, every gate clean. CI rebuilds the pack on every push. The interface is ENGLISH — the German course ships no `ui` block, which was reversed on Kevin's call and is not up for re-translating. The app carries the mascot, palette, phase ladder and Blüemli per course from the pack.

**There is no next phase.** Phase 7 landed 2026-09-01 and `p7-18` **Niemand wechselt ins Englische** is the last story: five people at a table on a warm evening and nobody switches to English all night. Nobody announces it and the protagonist tells nobody. `NEXT.md` §23 has the numbers.

**Do not start writing more stories.** The spine is 192 and it is finished. If Kevin wants more, that is a spine decision and it is his, not yours.

**What is actually open, in his priority order to be confirmed:**

1. **Nobody has fact-checked the Swiss German** and it is now 117,863 words long. Every `NEXT.md` phase section ends with a "known, and worth flagging" list; those are the judgement calls. This has been the biggest risk since 2026-08-24 and it is unchanged.
2. **Phase 7's own vocabulary has never been through RETURN.** A word is judged once 25 stories exist after it, and there are none after `p7-18`. Anything introduced in the last eighteen stories is taught once and untested by the gate. Structural, not fixable by writing.
3. **Nothing checks whether a story is good.** The gates check shape, Swissness, recycling and tappability. A read-through by an actual learner is the missing test.
4. **`aufpassen` and `aufwachen` finished at one use each**, seven phases running. In the dictionary, effectively untaught. Drop them or find them a home.

**Three things every phase has now taught, in the same order.** RETURN judges the previous phase's vocabulary the moment the new one lands and takes warm-up cards away: 44, then 28, then 32, 10, 16 and 11 across the seven phases that had one. **Budget the recycling sweep as part of writing the phase**; it falls when the writing carries the last phase forward on purpose, and it will never reach zero. Every sweep then breaks one or two words that relied on being one-scene, so re-run the check after it, every time — phase 5 was the first time it came back clean, which is not a reason to skip it. There is no eighth sweep: phase 7 has no phase after it. And adding a word can break one that already resolved, by making a form ambiguous: `ansprechen` cost `spricht` and `ausladen` cost `lädt`, both pinned now. **Read the AMBIGUOUS list, not only the unmapped one.**

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
