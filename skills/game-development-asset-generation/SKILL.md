---
name: game-development-asset-generation
description: "Plans, creates, and integrates game images, models, animation, and audio. Use when a game task needs new or revised sprites, textures, 3D models, animations, sound effects, music, or voice."
---

# Game assets

Produce the assets required by the game or feature brief, integrate them, and check them in gameplay before delivery. Begin production early enough to revise results. Preserve explicit prototype scope and existing assets that already fit the task.

## Choose the asset pipeline for the art direction

The user's brief and existing project style govern the choice. For an individual asset or feature, produce what that change needs; do not expand it into a full-game asset replacement. Preserve the established pipeline unless the user asks for a change or the requested result requires one.

Choose per asset or system:

* Use image generation or authored sprites and textures when painted detail, a specific character, or a consistent illustrated style matters.
* Use Blender or a suitable model generator for hero objects that need controlled silhouettes, materials, rigging, and editable geometry.
* Use procedural geometry, shaders, or code-drawn 2D art when they serve the visual direction, simulation, variation, or scale. Terrain, water, vegetation, and reactive effects can benefit from this approach. A procedural environment and an authored vehicle can work well together.
* Use generated audio, samples, or intentional synthesis according to the sound direction. Tune variation, envelopes, layering, and the mix; generic oscillator beeps do not count as finished audio.

Judge the result in gameplay. Procedural art must meet the same standards for silhouette, composition, readability, lighting, detail, and motion as imported assets. Generated files need the same scrutiny. Replace generic stand-ins, but do not replace successful procedural work merely because it was made in code.

## Establish visual targets before producing the set

For a new game or substantial visual redesign, create or use supplied concept images for the important gameplay states. Save them in the project with short notes about palette, materials, camera, lighting, and the qualities to preserve. Compare in-game captures against these targets at a similar framing and scale. Reuse established references for small additions instead of restarting concept development.

For a hero model, prepare clear views from the angles needed to resolve its shape, such as front, side, rear, and three-quarter views. Check that the views agree before modelling. Inspect silhouette and materials in renders, then inspect the exported asset in the game. Follow `blender-workflow` when using Blender. Keep editable source separate from the runtime export and check rendering cost, including material batches and draw calls as well as triangles.
## Tool selection

Use available tools within the user's authorization. Read [asset tools](references/asset-tools.md) when selecting an unfamiliar service or local tool. External generation is optional. If a preferred tool is unavailable, use a suitable local or procedural alternative; ask for access only when the requested result depends on it. Do not publish or upload the game through a generation service unless requested.

## Completion

Inspect the integrated assets at actual gameplay size and in motion. Check consistency, silhouette, transparency, seams, animation transitions, audio loops, and mix where applicable. For hero models, inspect the runtime export as well as the editable source. Compare against established visual targets. Fix observed gaps, then recapture affected states; identify any concrete blocker or unverified output.
