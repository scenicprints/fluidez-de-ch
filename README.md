# Fluidez — Swiss Standard German (de-ch)

Content repository for the Fluidez language app, anchored in Luzern.

    content/
      plan/spine.json        THE PLAN — all 184 stories
      plan/PROGRESS.md       auto-written; what is done
      manifest.json          what the pack build reads
      dictionary/*.json      the dictionary
      lessons/*.json         the stories
      scenarios/*.json       the scenes
      patterns/*.json        grammar explainers

The app reads `content/pack.json`, rebuilt by CI on every push, so publishing
a lesson never needs an app release.

**Read `NEXT.md` first, then `HANDOFF.md`.**

We teach **Swiss Standard German**, not dialect and not German German.
No eszett, ever.
