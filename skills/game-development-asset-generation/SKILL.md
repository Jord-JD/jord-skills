---
name: game-development-asset-generation
description: Agent advice for generating assets for game development projects. Use this skill when you're doing game development and might need to generate images, textures, 3D models, sound effects, music, etc. for the game you're working on. Use it even if you're just planning to do one of these things.
---

# Finish the game's assets in the first turn

Support delivery of the full requested game in the first turn, with AAA-level visual and audio quality as the target. Plan and produce assets for all requested content and player-facing states. Do not stop at assets for a showcase scene or defer animation, sound, music, or the remaining levels to a follow-up prompt. Follow an explicit request for a prototype or individual asset when that is the task.

Start asset production early enough to integrate, inspect, and revise the results during development. Keep perspective, scale, palette, materials, lighting, and animation consistent across the game. Inspect assets at their actual gameplay size and in motion; check animation transitions, transparency, texture seams, and audio loops where relevant. Replace temporary stand-ins before delivery. A generated file is only finished when it works well in the game.

# Choose the asset pipeline for the art direction

The user's brief and existing project style govern the choice. For an individual asset or feature, produce what that change needs; do not expand it into a full-game asset replacement. Preserve the established pipeline unless the user asks for a change or the requested result requires one.

Choose per asset or system:

* Use image generation or authored sprites and textures when painted detail, a specific character, or a consistent illustrated style matters.
* Use Blender or a suitable model generator for hero objects that need controlled silhouettes, materials, rigging, and editable geometry.
* Use procedural geometry, shaders, or code-drawn 2D art when they serve the visual direction, simulation, variation, or scale. Terrain, water, vegetation, and reactive effects can benefit from this approach. A procedural environment and an authored vehicle can work well together.
* Use generated audio, samples, or intentional synthesis according to the sound direction. Tune variation, envelopes, layering, and the mix; generic oscillator beeps do not count as finished audio.

Judge the result in gameplay. Procedural art must meet the same standards for silhouette, composition, readability, lighting, detail, and motion as imported assets. Generated files need the same scrutiny. Replace generic stand-ins, but do not replace successful procedural work merely because it was made in code.

# Establish visual targets before producing the set

For a new game or substantial visual redesign, create or use supplied concept images for the important gameplay states. Save them in the project with short notes about palette, materials, camera, lighting, and the qualities to preserve. Compare in-game captures against these targets at a similar framing and scale. Reuse established references for small additions instead of restarting concept development.

For a hero model, prepare clear views from the angles needed to resolve its shape, such as front, side, rear, and three-quarter views. Check that the views agree before modelling. Inspect silhouette and materials in renders, then inspect the exported asset in the game. Follow `blender-workflow` when using Blender. Keep editable source separate from the runtime export and check rendering cost, including material batches and draw calls as well as triangles.

# Tools for producing assets

Use available tools that suit the asset and the project. External generation is one option, not a requirement. Examples include:

* imagegen skill - If you're an OpenAI or Codex agent, you probably have access to the imagegen skill which is great for generating textures instead of using flat colours or gradients. Remember you can also prompt image models to make tileable textures when that's appropriate.
* Higgsfield Skills - https://higgsfield.ai/skills - Great for generating images (textures), textured 3D models (via Meshy AI), sound effects (Note: avoid using the Higgsfield websites skill and do not publish games to Higgsfields at all unless the user specifically asks you to)
* ElevenLabs Skills - https://github.com/elevenlabs/skills - Great for text-to-speech (if your game characters need to talk), also sound effects and music generation
* MeshyAI Skills - https://github.com/meshy-dev/meshy-3d-agent - Great for 3D model generation (textured or otherwise) from either text prompts or image prompts - sometimes it is good to generate a reference image and supply it to the image-to-3D endpoint
* Blender - Use Blender (install it if necessary) and use its headless Python interpreter to make 3D models entirely yourself for free. Useful if you need something entirely bespoke and matching very specific requirements.
* 3D model rigging - You can use MeshyAI for this also, but it is limited. It can be better to get a 3D model from Higgsfield/MeshyAI and then rig it yourself in code.
* 3D model animation - MeshyAI can do this, but again it is limited. If you rig the 3D models yourself, you can also animate them yourself.

See what relevant services/skills you have available in your environment and use what you can. There are also plenty of other services available online other than those listed above, so feel free to search for others online if needed.

Use available tools within the user's authorization. If a preferred service is unavailable, continue with a suitable local or procedural alternative that meets the art direction. Ask for access only when it is necessary for the requested result; finish unaffected work and state the specific dependency.

# Self review

Check the assets covered by the request in their actual gameplay states. Confirm consistency with the saved visual targets, legibility in motion, and the quality of animation and audio where relevant. For hero models, inspect the runtime export as well as the editable source. Resolve applicable gaps before delivery, or state the concrete blocker and what remains unverified.
