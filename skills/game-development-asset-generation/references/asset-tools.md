# Tools for producing assets

Consult this catalogue when choosing an unfamiliar asset tool. Check current capabilities and availability before relying on a service. Use available tools that suit the asset and the project. External generation is one option, not a requirement. Examples include:

* imagegen skill - If you're an OpenAI or Codex agent, you probably have access to the imagegen skill which is great for generating textures instead of using flat colours or gradients. Remember you can also prompt image models to make tileable textures when that's appropriate.
* Higgsfield Skills - https://higgsfield.ai/skills - Great for generating images (textures), textured 3D models (via Meshy AI), sound effects (Note: avoid using the Higgsfield websites skill and do not publish games to Higgsfields at all unless the user specifically asks you to)
* ElevenLabs Skills - https://github.com/elevenlabs/skills - Great for text-to-speech (if your game characters need to talk), also sound effects and music generation
* MeshyAI Skills - https://github.com/meshy-dev/meshy-3d-agent - Great for 3D model generation (textured or otherwise) from either text prompts or image prompts - sometimes it is good to generate a reference image and supply it to the image-to-3D endpoint
* Blender - Use Blender (install it if necessary) and use its headless Python interpreter to make 3D models entirely yourself for free. Useful if you need something entirely bespoke and matching very specific requirements.
* 3D model rigging - You can use MeshyAI for this also, but it is limited. It can be better to get a 3D model from Higgsfield/MeshyAI and then rig it yourself in code.
* 3D model animation - MeshyAI can do this, but again it is limited. If you rig the 3D models yourself, you can also animate them yourself.

See what relevant services/skills you have available in your environment and use what you can. There are also plenty of other services available online other than those listed above, so feel free to search for others online if needed.

Use available tools within the user's authorization. If a preferred service is unavailable, continue with a suitable local or procedural alternative that meets the art direction. Ask for access only when it is necessary for the requested result; finish unaffected work and state the specific dependency.
