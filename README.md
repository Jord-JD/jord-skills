# jord-skills

A collection of [Agent Skills](https://agentskills.io/) I've made. Each skill lives in its own directory under `skills/` and follows the open `SKILL.md` format.

## Skills

| Skill | Summary |
| --- | --- |
| [`blender-workflow`](skills/blender-workflow/SKILL.md) | Guides Blender work towards reproducible `bpy` scripts run by the real Blender executable, with structured scene checks and iterative render inspection. Blender MCP and GUI control are treated as optional live-session side channels rather than replacements for durable Python automation. |
| [`commit-authorship`](skills/commit-authorship/SKILL.md) | Keeps commit authorship with the human by preventing agents from adding themselves as co-authors unless explicitly asked. |
| [`electronics-design`](skills/electronics-design/SKILL.md) | Guides circuit and PCB engineering across CAD tools, covering requirements, component sourcing, power and layout constraints, manufacturing cost, engineering review, and prototype validation. Use alongside the CAD-specific skill when building or changing a board. |
| [`game-development`](skills/game-development/SKILL.md) | Guides complete games and focused changes through implementation, presentation, and real-input playtesting. Loads simulation, movement, procedural-world, saving, and performance guidance only for relevant tasks. |
| [`game-development-asset-generation`](skills/game-development-asset-generation/SKILL.md) | Guides game projects towards purpose-made images, textures, 3D models, sound effects, and music instead of bland code-generated stand-ins. It points agents to specialised generation tools or Blender, respects an existing game's style, and requires a final self-review. |
| [`kicad-workflow`](skills/kicad-workflow/SKILL.md) | Handles KiCad installation discovery, structured schematic and PCB operations, design-rule configuration, ERC/DRC and parity checks, visual inspection, and consistent manufacturing exports. Pair with `electronics-design` for engineering decisions. |
| [`lithium-battery-safety`](skills/lithium-battery-safety/SKILL.md) | Adds safety checks for lithium battery use, charging, warning signs, storage, and disposal. It requires current product research for compatibility questions and local official guidance for emergencies. |
| [`natural-writing`](skills/natural-writing/SKILL.md) | Mandatory guidance for human-readable writing. Requires reading comparable examples from at least two independent online sources before new content or substantial rewrites, preserves voice, and cuts AI writing habits, fluff, and excessive headings. |
| [`polite-browser-use`](skills/polite-browser-use/SKILL.md) | Makes browser and Electron testing quiet and unobtrusive. It requires muted audio, avoids unexpected visible windows, and cleans up tabs, processes, and test servers when the work is done. |
| [`research-backed-frontend-development`](skills/research-backed-frontend-development/SKILL.md) | Routes new interfaces, existing-interface changes, and reviews through the relevant research, design, implementation, and visual checks. Small fixes reuse established design evidence. Supports web, native, game, and embedded displays. |
| [`screeps-world-ai`](skills/screeps-world-ai/SKILL.md) | Guides Screeps World bot development and live operation across codebases, covering CPU, movement, economic accounting, remote mining, planning, expansion, combat, and verification of actual behaviour. |
| [`small-tasks-small-answers`](skills/small-tasks-small-answers/SKILL.md) | Keeps responses proportionate to straightforward requests such as small edits, simple calculations, server starts, and commit-and-push tasks. |
| [`view-video`](skills/view-video/SKILL.md) | Downloads videos with yt-dlp, extracts timestamped frames with FFmpeg, reads subtitles, and requires actual image inspection. Supports focused follow-ups, original timeline offsets, and optional local transcription. |
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
