---
name: game-development
description: "MANDATORY for game development tasks: new games, gameplay design, features, fixes, and playtesting. Research comparable games before choosing new mechanics, inspect actual gameplay, and verify changes by playing through real controls. Keep small fixes within the existing design."
---

# Game development

Build the experience the user asked for, at the requested scale. Preserve the project's engine, controls, style, and unrelated work. A prototype can stay a prototype; a complete game needs its requested content, progression, failure, and retry paths.

## Understand the game before building

For a new game or substantial gameplay redesign, research at least two comparable games. Watch relevant gameplay or inspect a playable demo, rather than relying on descriptions, trailers, or search snippets alone. Study the player's actions, timing, feedback, difficulty, and recovery from mistakes. Read relevant engine documentation when implementation details are uncertain.

Keep brief notes with sources, footage timestamps or played sequences, observations, and the decisions they support. Verify that both examples were actually inspected before proposing the design. Prefer short relevant footage or accessible demos. If a fetch fails, try another source and another available access method, such as a browser or direct download. Use the normal approval path for sandbox-blocked operations; one tool's network failure does not establish that research is unavailable. If alternatives remain blocked, explain the evidence missing. Reuse current project research. A bug fix or small addition within an established design needs focused reproduction and inspection, not a new research project.

Define the primary action, objective, challenge, reward, controls, and first minute of play. Implement the core interaction early and play it before building the rest around it. Tune from observed behaviour; borrowed timing values are starting points, not universal rules. For design-only requests, give the requested proposal and distinguish reference observations from untested ideas.

## Build the requested experience

Make actions readable and responsive. Connect gameplay, animation, camera, sound, and interface feedback so the player can tell what happened. Keep effects proportionate and ensure they return to rest. Include required input methods and a clear way to pause, fail, retry, and finish where applicable.

Use the existing architecture and the simplest implementation that supports the brief. Read [technical checks](references/technical-checks.md) only for changes involving simulation, movement, procedural worlds, persistence, or performance.

Use `game-development-asset-generation` for assets and `research-backed-frontend-development` for menus and HUDs when available. Reuse their research rather than repeating it. Integrate presentation during development and inspect it at gameplay size and in motion. Preserve intentional placeholder scope; replace stand-ins when delivering finished art.

## Play, inspect, and fix

Exercise the affected journeys through real keyboard, pointer, touch, or controller inputs. Calling a gameplay function directly does not test the input path. Check consequences: a hit changes health, defeat changes state, and retry restores a playable game. Use repeatable fixtures for hard-to-reach states, but also test the transitions into them.

Actually view screenshots or recordings from play, check logs, and fix observed problems before replaying the affected scenario. Check readability, camera framing, collision, feedback, and relevant screen sizes. Use existing tests; add a focused regression check when it will catch the failure. A successful build alone does not establish correct gameplay.

Apply `polite-browser-use` before browser or preview operation, and `view-video` for recordings when available. Finish when the requested behaviours and relevant checks pass, or explain a concrete blocker. Report what was played and what remains unverified. Do not publish or upload the game unless requested.
