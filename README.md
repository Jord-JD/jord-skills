# jord-skills

A collection of [Agent Skills](https://agentskills.io/) I've made. Each skill lives in its own directory under `skills/` and follows the open `SKILL.md` format.

## Skills

| Skill | Summary |
| --- | --- |
| [`commit-authorship`](skills/commit-authorship/SKILL.md) | Keeps commit authorship with the human by preventing agents from adding themselves as co-authors unless explicitly asked. |
| [`game-development-asset-generation`](skills/game-development-asset-generation/SKILL.md) | Guides game projects towards purpose-made images, textures, 3D models, sound effects, and music instead of bland code-generated stand-ins. It points agents to specialised generation tools or Blender, respects an existing game's style, and requires a final self-review. |
| [`lithium-battery-safety`](skills/lithium-battery-safety/SKILL.md) | Adds safety checks for lithium battery use, charging, warning signs, storage, and disposal. It requires current product research for compatibility questions and local official guidance for emergencies. |
| [`natural-writing`](skills/natural-writing/SKILL.md) | Applies to any prose a human will read. It favours plain, specific language, preserves the author's voice when editing, and removes filler and common AI-writing habits. |
| [`polite-browser-use`](skills/polite-browser-use/SKILL.md) | Makes browser and Electron testing quiet and unobtrusive. It requires muted audio, avoids unexpected visible windows, and cleans up tabs, processes, and test servers when the work is done. |
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
