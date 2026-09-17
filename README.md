# jord-skills

A collection of [Agent Skills](https://agentskills.io/) I've made. Each skill lives in its own directory under `skills/` and follows the open `SKILL.md` format.

## Skills

| Skill | Summary |
| --- | --- |
| [`blender-workflow`](skills/blender-workflow/SKILL.md) | Studies visual references, builds with reproducible Blender Python, and checks scene data, renders, and requested exports. Keeps small edits proportionate. |
| [`commit-authorship`](skills/commit-authorship/SKILL.md) | Keeps commit authorship with the human by preventing agents from adding themselves as co-authors unless explicitly asked. |
| [`electronics-design`](skills/electronics-design/SKILL.md) | Guides circuit and PCB engineering across CAD tools, covering requirements, component sourcing, power and layout constraints, manufacturing cost, engineering review, and prototype validation. Use alongside the CAD-specific skill when building or changing a board. |
| [`game-development`](skills/game-development/SKILL.md) | Researches comparable gameplay, builds the requested experience, and verifies it through real controls and inspected captures. Keeps specialised technical checks in one short reference. |
| [`game-development-asset-generation`](skills/game-development-asset-generation/SKILL.md) | Studies comparable art or sound, establishes a consistent direction, produces assets with suitable tools, and checks them at gameplay scale. |
| [`kicad-workflow`](skills/kicad-workflow/SKILL.md) | Handles KiCad installation discovery, structured schematic and PCB operations, design-rule configuration, ERC/DRC and parity checks, visual inspection, and consistent manufacturing exports. Pair with `electronics-design` for engineering decisions. |
| [`lithium-battery-safety`](skills/lithium-battery-safety/SKILL.md) | Adds safety checks for lithium battery use, charging, warning signs, storage, and disposal. It requires current product research for compatibility questions and local official guidance for emergencies. |
| [`natural-writing`](skills/natural-writing/SKILL.md) | Mandatory guidance for human-readable writing. Requires reading comparable examples from at least two independent online sources before new content or substantial rewrites, preserves voice, and cuts AI writing habits, fluff, and excessive headings. |
| [`polite-browser-use`](skills/polite-browser-use/SKILL.md) | Mandatory before browser, Electron, or preview operation: mute audio, avoid disruptive windows, and clean up owned resources without disturbing the user's tabs. |
| [`research-backed-frontend-development`](skills/research-backed-frontend-development/SKILL.md) | Mandatory for every frontend, UI, and UX task. Grounds new design decisions in two visually inspected products, relevant UX/UI guidance, and videos or live demos for interactions. Verifies the rendered result and keeps small fixes proportionate. |
| [`screeps-world-ai`](skills/screeps-world-ai/SKILL.md) | Guides Screeps World bot development and live operation across codebases, covering CPU, movement, economic accounting, remote mining, planning, expansion, combat, and verification of actual behaviour. |
| [`small-tasks-small-answers`](skills/small-tasks-small-answers/SKILL.md) | Keeps responses proportionate to straightforward requests such as small edits, simple calculations, server starts, and commit-and-push tasks. |
| [`view-video`](skills/view-video/SKILL.md) | Uses the bundled helper to find relevant video moments, inspect actual frames and speech, and report timestamped evidence. Keeps extraction and troubleshooting details in a reference. |
| [`visual-inspection-improvement`](skills/visual-inspection-improvement/SKILL.md) | Captures and inspects affected views against the brief. Reviews report supported findings; improvement tasks fix visible defects and recapture affected states until the requested criteria are met. |

## Install skills

### Codex + Claude Code

Install all skills globally for both Codex and Claude Code, without prompts:

```bash
npx skills add Jord-JD/jord-skills -g -s '*' -a codex claude-code -y
```

This installs the skills at user level so they are available across all projects. The `-a` flag restricts the install to Codex and Claude Code; `--all` is deliberately not used because it targets every supported agent.

### Interactive install

To choose skills and agents interactively while still installing globally:

```bash
npx skills add Jord-JD/jord-skills -g
```

### Install one skill

For example, to install only `natural-writing` globally for Codex and Claude Code:

```bash
npx skills add Jord-JD/jord-skills -g -s natural-writing -a codex claude-code -y
```

These commands use the [skills CLI](https://github.com/vercel-labs/skills). Omit `-g` to install into the current project instead.
