# How we work — collaboration protocol
_Our contract for this sprint. Read me first each session._

## The contract (non-negotiable)
- **No lying, no inventing.** Every number/fact comes from your files or a verified source. If I must approximate or a source is unverified, I say so *before* using it, and we agree how.
- **Real data, fact-checked, project-logic-driven.** No trying things in circles. Goal-oriented, scientific, practice-proven.
- **I state my limits honestly** — complexity, time, and capability. If something is beyond what's reliable in the time we have, I tell you and propose the pragmatic alternative.

## Who does what
| Task | Who |
|---|---|
| Download data from portals (browser) | **Carlton** (I can't reach gov portals; can drive Chrome if connected) |
| Audit data, read real attribute codes, build reclass tables | **Claude** (headless GDAL/Python here) |
| Clip / reproject / reclassify / compute hectares / erosion / flow | **Claude** (headless — hand you finished layers) |
| PyQGIS scripts, styles (.qml), layouts (.qpt), Atlas | **Claude** writes → **Carlton** runs in QGIS |
| Final styling, panel assembly (Figma), print export | **Carlton** (I stage assets + give exact settings) |
| Writing: memory text, narrative, planting calendar, legends | **Claude** |
| Verification / fact-check pass | **Claude**, you confirm |

## Version control — always GitHub Desktop
- Claude may **create, update, and delete** files directly in the repo folder.
- **Never give Sonya git CLI commands.** For commit / push / pull / sync she uses **GitHub Desktop**.
- Repo: `sonyanacheva/landscape-2025`. Heavy geodata stays git-ignored.

## Managing my context limit (important)
I degrade when a single conversation gets very long. Antidote:
1. **One block per session.** We work a block (see budget), then checkpoint.
2. **`PROGRESS/LOG.md` is the memory.** I log what's done, decisions, verified data, and the exact next step. A fresh chat + this log ≈ full context — so when a thread gets long, start a new one and say _"read 00_ADMIN, continue from LOG."_
3. I update the log at natural checkpoints (block done, decision made, data verified) — rigorously but not spammily.

## How to get the best from me
- Point me at **one goal** at a time; batch independent sub-steps.
- If I drift or over-engineer, say "checkpoint" and I'll log + reset scope.
- I can spawn a **helping hand** (parallel subagent) for independent work — e.g. drafting the A4 memory while the main thread does QGIS. Use when tasks are well-defined.
- Tell me your panel-layout vision per block so I stage exports to match, and we watch the panel form incrementally.

## Refined time budget (~12 working hrs)
Sections 1 (lynx/rabbit — not yours, handled separately) and 2 (green corridor — you like it, just needs image extraction/formatting later) are **out of the heavy sprint**.

| Block | Work | Deliverables | Est |
|---|---|---|---|
| **A (now)** | De-CORINE land cover | 4.5 agri matrix (+ha), 4.6 forest/scrub | 2.5 h |
| **B** | Upgrade diagnosis | 5.2 resistance, 5.1 habitat, re-run LCP/corridor | 2.5 h |
| **C** | Strategy | 6 masterplan + Hunilla link + Forman sections | 2.5 h |
| **D** | Interventions | 7 · 5 sheets @1:5000 (Atlas) + sections (needs 2 m DEM) | 2.5 h |
| **E** | Time + text | 8 phased barranco sections, planting calendar, project name, A4 memory | 2 h |
| **F** | Assembly (incremental) | Panels in Figma, A3 dossier, 300 dpi export, verification | 1.5 h ongoing |

Panels assembled incrementally: each block's finished map gets staged onto its panel so we see it forming.
