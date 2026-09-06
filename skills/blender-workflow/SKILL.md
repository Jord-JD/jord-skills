---
name: blender-workflow
description: Best-practice workflow for using Blender. Use this skill whenever you create, edit, inspect, render, animate, rig, export, or otherwise automate Blender content. Prefer reproducible Blender Python run through the real Blender executable, with structured checks and rendered visual inspection; use Blender MCP or GUI control as optional live-session tools rather than the primary modelling interface.
---

# Blender workflow

## Default approach

Treat Blender Python as the primary control interface.

For substantial work, prefer this order:

1. Write or update version-controlled Python using `bpy`, `bmesh`, `mathutils`, and Blender's data APIs.
2. Run that code with the actual Blender executable, normally in background mode.
3. Inspect both machine-readable scene state and rendered images.
4. Iterate until the structural and visual checks pass.
5. Use Blender MCP when a live Blender session is genuinely useful.
6. Use GUI/computer-control tools only for tasks that are awkward or impossible through Blender's programmatic interfaces.

Do not replace a good Python workflow with a long sequence of opaque GUI clicks or granular MCP mutations. Substantial edits should be represented in scripts where practical so they can be diffed, rerun, debugged, and reused. The `.blend` file is still a legitimate project artefact; not every existing scene needs to be regenerated from scratch.

## Run scripts through Blender

Prefer the project's real Blender installation over a standalone `pip install bpy` environment unless there is a specific reason to use the Python module build.

A typical command is:

```bash
blender scene.blend \
  --background \
  --python-exit-code 1 \
  --python scripts/change_scene.py
```

For a greenfield scene, a script may start from an empty/factory scene instead. Pass script-specific arguments after `--` when useful.

Always:

- capture stdout and stderr;
- treat a non-zero exit status as failure;
- save the intended output `.blend` explicitly;
- avoid silently overwriting a valuable source file unless that is intentional;
- keep repeatable scripts in the repository rather than hiding substantial logic in one-off shell snippets.

If Blender is not available, first look for an existing project-specific installation or documented setup. Install Blender only when the environment permits it and doing so is appropriate for the task.

## Write robust Blender automation

Prefer Blender's data API and `bmesh` over context-sensitive `bpy.ops` where practical. Operators are fine when they are the clearest solution, but many depend on selection, active objects, editor areas, modes, or other UI context that may not exist in headless execution.

For scripts you expect to iterate on:

- give important objects, collections, materials, cameras, and lights stable descriptive names;
- make important dimensions and tunable values explicit constants or parameters rather than scattering magic numbers through the script;
- make scripts deterministic and reasonably idempotent where practical;
- use explicit units and be careful about scale and transform assumptions;
- preserve unrelated user-authored scene content when modifying an existing file;
- prefer non-destructive modifiers where they make iteration safer;
- create a checkpoint before destructive edits to an important existing scene;
- do not run Blender API work from arbitrary background Python threads; Blender's Python integration is not generally thread-safe.

Do not depend on the currently selected object, current mode, active editor, or viewport state unless the task specifically requires interactive context.

## Inspect, render, then iterate

A script completing without an exception does not mean the result is correct. After every meaningful modelling, layout, material, lighting, rigging, or animation change, inspect the result.

Whenever useful, produce a small review bundle such as:

```text
output/blender-review/
  scene-info.json
  perspective.png
  front.png
  side.png
  top.png
```

The exact files should fit the task. Do not create unnecessary output just to satisfy a template.

### Structured inspection

Have Blender emit machine-readable facts that matter for the task. Useful checks include:

- object names and types;
- locations, rotations, scales, dimensions, and world-space bounding boxes;
- vertex/edge/face counts;
- materials and modifiers;
- camera and light settings;
- collection membership;
- missing links or unexpected duplicate objects;
- relevant distances and clearances.

For fabrication or 3D-printing work, also check the things that determine physical correctness: units, overall dimensions, wall thicknesses, mating clearances, disconnected geometry, non-manifold/open edges, normals, and whether exported geometry has the intended scale.

For animation or rigging, inspect key frames, frame ranges, parent/bone relationships, constraints, and representative poses.

### Visual inspection

Render several useful diagnostic views, normally including a perspective view plus orthographic or close-up views that expose likely problems. Render them as separate images rather than a contact sheet so each can be inspected closely.

Use inexpensive preview settings during iteration. Do not spend time on a high-sample final render while geometry, framing, lighting, intersections, materials, or proportions are still being corrected.

Actually inspect the rendered images before declaring the work finished. Look for issues such as:

- intersections and floating objects;
- wrong scale or proportions;
- bad camera framing;
- shading, normal, smoothing, or material problems;
- visible gaps, clipping, z-fighting, or unexpected booleans;
- lighting that hides the form;
- details that technically exist but are visually unreadable.

If a problem is visible, fix it, rerender the affected views, and inspect again.

## MCP is a live-session side channel

If Blender's official MCP integration is available, use it when interacting with an already-open Blender session is valuable: inspecting the current scene or selection, understanding live state, examining something that is cumbersome to serialise, or applying a small interactive change.

Do not assume MCP is inherently better than Python. For substantial work, prefer writing the durable Blender Python in the repository and executing it through Blender. If MCP is the only convenient route into the live session, use it to execute or support that scripted workflow rather than turning a coherent modelling operation into dozens of opaque micro-calls.

Treat any Blender MCP capable of executing generated Python as powerful local code execution. Keep it local/trusted and respect the surrounding sandbox and approval model.

## GUI/computer control is supplemental

Use GUI automation when visual editor interaction is genuinely required or when no reliable structured interface exists. Do not use mouse/keyboard automation for ordinary scene changes that can be expressed reliably in `bpy`.

A good hybrid workflow is:

```text
agent
  -> repository Python scripts
  -> Blender background execution
  -> scene-info / validation output
  -> preview renders
  -> visual + structural inspection
  -> iterate

optional: Blender MCP or GUI inspection of a live session
```

## Finishing checklist

Before handing Blender work back to the human:

- rerun the relevant automation from a clean, understood starting state;
- confirm Blender exits successfully with no important warnings or tracebacks;
- confirm the intended `.blend` and requested exports were actually written;
- inspect the final diagnostic renders;
- verify dimensions, scale, object state, and other task-specific structural checks;
- if exporting STL, GLB, FBX, OBJ, or another delivery format, verify the exported file exists and, when practical, re-import or otherwise validate it;
- leave the scripts and important parameters understandable for the next agent or human who needs to modify the work.
