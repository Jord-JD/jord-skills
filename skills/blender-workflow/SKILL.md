---
name: blender-workflow
description: "Use for Blender modelling, materials, scenes, rigging, animation, rendering, inspection, and exports. Research visual references for new or substantially changed artwork, build with reproducible Blender Python, and inspect renders and scene data before delivery."
---

# Blender workflow

Use Blender Python as the main interface. Keep substantial work in rerunnable scripts; preserve existing scene content and the user's chosen style.

## Study the subject

Before a new model or scene, or substantial changes to its shape, materials, lighting, or composition, find and visually inspect references from at least two independent relevant sources. Study actual images, renders, or video frames, not search snippets or page descriptions. Choose references that resolve the task's questions: silhouette and construction, material response, proportions, composition, or motion. Use several angles when one view leaves the form ambiguous.

Briefly note the sources and what you observed before modelling. Borrow useful principles without copying a distinctive design or overriding the brief. Supplied references count; reuse evidence already inspected for this task. A small correction or mechanical export needs only the relevant existing reference and checks, not a new mood board. If visual access fails, try alternatives, then disclose any remaining gap.

When an API or workflow is uncertain, check the official Blender manual or Python API documentation for the installed Blender version. Do not guess context requirements or assume an example for another version still works.

## Build with Python

Use the project's real Blender executable, normally in background mode:

```bash
blender scene.blend --background --python-exit-code 1 --python scripts/change_scene.py
```

For a new scene, use an explicit clean starting state. For an existing project, inspect it first and preserve unrelated objects. Keep substantial automation in the repository, capture output and failures, and explicitly save the intended `.blend`. Make a checkpoint before destructive changes to valuable source content.

Prefer `bpy` data APIs, `bmesh`, and `mathutils` over context-sensitive operators. When using `bpy.ops`, explicitly establish the required active object, selection, mode, and other context; do not rely on an interactive viewport existing in background mode. Keep Blender API work on its main thread.

Use stable object names, explicit units and parameters, and repeatable operations that avoid accidental duplicates. Account for transforms and world-space dimensions. Use non-destructive modifiers where useful. Live Blender tools or GUI control can help with inspection or awkward operations; keep substantial changes reproducible in scripts.

If Blender is unavailable, check the project's documented installation. Do not present unexecuted code as a verified scene.

## Inspect and deliver

Run the automation in Blender and check both scene data and rendered images. A successful script alone proves neither visual nor structural correctness.

Check the facts that matter: dimensions and transforms, object and collection state, materials, modifiers, missing dependencies, or clearances. Render inexpensive previews from views that expose likely problems. Actually open and inspect those images for silhouette, proportions, intersections, floating parts, shading, lighting, and framing. Correct visible defects and inspect fresh renders before making the final render. A small edit needs focused checks; a complex object may need perspective, orthographic, and detail views.

For fabrication, check units, wall thickness, mating clearances, disconnected geometry, non-manifold or open edges, and normals. Verify export scale; a convincing render does not establish physical correctness.

For rigs and animation, check frame ranges, parenting, bones, constraints, deformations, and intersections. Inspect representative poses and transitions or short sequences when motion matters. Verify exported animation in the target runtime when available.

Confirm the saved `.blend` and requested exports exist. Re-import or independently inspect exports where practical, checking scale, materials, geometry, and animation as applicable. Deliver the editable source and scripts alongside requested outputs, with a brief account of what was verified and any remaining limitations.
