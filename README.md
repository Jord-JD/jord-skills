# jord-skills

A collection of [Agent Skills](https://agentskills.io/) I've made. Each skill lives in its own directory under `skills/` and follows the open `SKILL.md` format.

## Skills

| Skill | Summary |
| --- | --- |
| [`commit-authorship`](skills/commit-authorship/SKILL.md) | Keeps commit authorship with the human by preventing agents from adding themselves as co-authors unless explicitly asked. |
| [`game-development`](skills/game-development/SKILL.md) | Engine-neutral guidance for making games people want to play twice. It covers working out the core verb, researching comparable games, building a fixed-step loop with named input actions and seeded randomness, tuning jump and hit feedback with real starting values, using purpose-made art and sound, and playing the game with scripted input and screenshots before calling it done. |
| [`game-development-asset-generation`](skills/game-development-asset-generation/SKILL.md) | Guides game projects towards purpose-made images, textures, 3D models, sound effects, and music instead of bland code-generated stand-ins. It points agents to specialised generation tools or Blender, respects an existing game's style, and requires a final self-review. |
| [`lithium-battery-safety`](skills/lithium-battery-safety/SKILL.md) | Adds safety checks for lithium battery use, charging, warning signs, storage, and disposal. It requires current product research for compatibility questions and local official guidance for emergencies. |
| [`natural-writing`](skills/natural-writing/SKILL.md) | Applies to any prose a human will read. It favours plain, specific language, preserves the author's voice when editing, and removes filler and common AI-writing habits. |
| [`polite-browser-use`](skills/polite-browser-use/SKILL.md) | Makes browser and Electron testing quiet and unobtrusive. It requires muted audio, avoids unexpected visible windows, and cleans up tabs, processes, and test servers when the work is done. |
| [`research-backed-frontend-development`](skills/research-backed-frontend-development/SKILL.md) | Applies research-led design and visual QA to any UI, including websites, apps, games, kiosks, and embedded-device displays. It sets a high visual-quality bar while accounting for target-specific controls, display constraints, implementation, and verification. |
| [`small-tasks-small-answers`](skills/small-tasks-small-answers/SKILL.md) | Keeps responses proportionate to straightforward requests such as small edits, simple calculations, server starts, and commit-and-push tasks. |
| [`visual-inspection-improvement`](skills/visual-inspection-improvement/SKILL.md) | Provides an iterative visual QA process: capture the relevant user-facing states, inspect them closely, make improvements, and repeat until the visible problems are gone. |

## Install skills

Install all skills globally so they are available across your projects:

```bash
npx skills add Jord-JD/jord-skills -g
```

To install one skill globally:

```bash
npx skills add Jord-JD/jord-skills --skill natural-writing -g
```

These commands use the [skills CLI](https://github.com/vercel-labs/skills). Omit `-g` to install into the current project instead.
