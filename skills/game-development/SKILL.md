---
name: game-development
description: "Builds and changes playable games, covering mechanics, presentation, and playtesting. Use when creating a game, adding a gameplay feature, or fixing game behaviour."
---

# Game development

Complete the experience requested in the brief. Continue through implementation, asset integration, playtesting, and fixes within the authorized scope. Make routine decisions without waiting for another prompt. A prototype or narrow fix should stay that size; a complete game needs all requested content and progression.

Aim for excellent controls, art direction, sound, pacing, and performance at the requested scale. A running loop or attractive opening scene does not establish completion. Track the requested mechanics, modes, levels, and player-facing states through implementation and verification. Report concrete blockers and complete unaffected work when a dependency prevents finishing.

## Choose the relevant work

Inspect the affected project files, engine version, input conventions, art style, and existing tests. Preserve the established stack and unrelated user work.

- For a new game or substantial design change, define the primary verb, objective, pressure, reward, failure/retry path, first minute, target controls, and scope. Inspect comparable games and actual gameplay evidence to resolve design decisions. Reuse relevant recorded research and keep source URLs and timestamps. Implement the core interaction early, then complete the requested experience.
- For a feature or bug fix, reproduce the affected behaviour and work within the existing design. Use engine documentation or focused design references where needed. A technical fix or menu typo does not require fresh game research, new assets, or a new test harness.
- For a review, inspect and report evidence without modifying the game unless asked.

Read only the relevant references:

| Work | Reference |
| --- | --- |
| Real-time loop, input, physics, or gameplay randomness | [Simulation](references/simulation.md) |
| Jumping, camera, impacts, or response tuning | [Movement and feedback](references/movement-and-feedback.md) |
| Generated terrain, moving water, or streaming collision | [Procedural worlds](references/procedural-worlds.md) |
| Save data or persistent settings | [Saving](references/saving.md) |
| Gameplay implementation or behavioural verification | [Playtesting](references/playtesting.md) |
| Optimisation or measured performance problems | [Performance](references/performance.md) |

## Integrate presentation

Produce assets only where the task needs them. Use `game-development-asset-generation` when available for asset selection, concepts, and runtime checks. Authored, generated, and procedural work must fit the same visual direction. Replace temporary stand-ins in finished deliverables; preserve intentional prototype scope.

Inspect characters, threats, and feedback at gameplay size and in motion. Measure spritesheet frames, margins, and spacing before importing them. Menus and HUDs must remain legible over busy scenes, survive target screen sizes, and work with the required controls. Keep audio levels consistent and effects from clipping. Effects must return to rest.

Use available companion skills only for their part of the task: `research-backed-frontend-development` for interface design, `view-video` for footage, `visual-inspection-improvement` for visual review, and `natural-writing` for player-facing text. Reuse evidence across these workflows. Missing companion skills do not remove the checks described here.

## Verify and deliver

Play affected journeys through real inputs. Check resulting state and inspect actual captures; calling a gameplay function directly does not verify input handling. Reuse fixtures for hard-to-reach visual states, but test transitions through real controls. Check logs and fix failures caused by the change. Expand verification only for new failures, shared-system changes, or unresolved concerns.

Before operating a browser or preview, follow `polite-browser-use` when available: mute before play, avoid unexpected windows, and close the tabs and test processes you started.

Finish when the requested content and interactions work, affected checks pass, and inspected presentation meets the brief without unresolved visible defects within scope. Report what was played, the evidence, and any unverified target or concrete blocker. Do not claim fun, polish, or performance without supporting observations. Do not publish, upload, or submit the game unless the user requests it.
