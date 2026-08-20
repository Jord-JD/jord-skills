---
name: game-development-asset-generation
description: Agent advice for generating assets for game development projects. Use this skill when you're doing game development and/or you might need might need to generate images, textures, 3d models, sound effects, music, etc. for the game you're working on. Use it even if you're just planning to do one of these things.
---

# When should you generate assets?

Currently a lot of standard AI generated games make their assets in code. This typically make games that look quite bland, flat and similar to one another.

* For 3D games, you might want to create 3D models for your Three.js games using code and colour them in code. This isn't how real, good quality games are typically made. They use proper 3D models with proper textures. You should do this to.
* For 2D games, you may be tempted to make all your images as SVGs or similar. This often gives all games the same flat feeling, and reduces the amount of detail you can put in to them. Also, it's much harder to make good graphics with SVGs or making them in code. Most real games use deliberate textures. You should probably do this too unless SVG/vector style graphic are essential for the style of your game.
* For sound, you're probably thinking about generating sound effects or music in code. Maybe if you're doing a web game, you're planning to use Web Audio or something. This sounds tinny, like an old arcade game, and is quite a tell that the game is a low quality AI generated game. You likely don't want to do this unless the goal is a retro or arcade style.

Of course, if the game you're working on already has a certain style or way of doing asset generation, do not deviate from that / make the game style inconsistent, unless your human specifically asks you to.

# How should I generate game assets instead?

You probably need to use alternative services / skills. You're probably not good enough to make high quality graphics/textures, 3D models, music/audio, etc. on your own. You need help from other services. Here are a few examples:

* imagegen skill - If you're an OpenAI / Codex agent, you probably have access to the imagegen skill which is great for generating textures instead of using flat colours or gradients. Remember you can also prompt image models to make tileable textures when that's appropriate.
* Higgsfield Skills - https://higgsfield.ai/skills - Great for generating images (textures), textured 3D models (via Meshy AI), sound effects
* ElevenLabs Skills - https://github.com/elevenlabs/skills - Great for text to speech (if your game characters need to talk), also sound effects and music generation
* MeshyAI Skills - https://github.com/meshy-dev/meshy-3d-agent - Great for 3D model generation (textured or otherwise) from either text prompts or images prompts - sometimes it is good to generate a reference image and supply to the Image to 3D endpoint
* 3D model rigging - You can use MeshyAI for this also, but it is limted. It can be better to get a 3D model from Higgsfield/MeshyAI and then rig it yourself in code.
* 3D model animation - MeshyAI can do this, but again it is limited. If you rig the 3D models yourself, you can also animate them yourself.

See what relevant services/skills you have available in your environment and use what you can. There are also plenty of other services available online other than those listed above.

Try to do this yourself if you can, however if you can't find anything appropriate, you should consider asking the user if you can use one or more of these services, rather than potentially produced a worse game.
