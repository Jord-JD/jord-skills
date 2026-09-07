---
name: kicad-workflow
description: Operate KiCad projects through structured schematic editing, supported PCB APIs, ERC/DRC, visual inspection, and manufacturing exports. Use for creating, editing, routing, checking, rendering, or exporting KiCad files. Pair with electronics-design when the task also requires circuit or PCB engineering decisions.
---

# KiCad workflow

## Scope and companion skill

This skill owns KiCad operations and CAD evidence. For circuit architecture, component selection, electrical constraints, placement strategy, engineering review, or manufacturing cost decisions, also use `electronics-design` when available. That skill owns the design sequence; this one implements the resulting constraints and checks. If it is unavailable, establish the necessary engineering inputs from project requirements and authoritative component documentation before making design changes.

An export, render, or file-format task does not require a new engineering review. A request to design a board in KiCad normally uses both skills. Do not treat successful CAD checks as proof of electrical performance or safety.

## Default approach

Treat `.kicad_pro`, `.kicad_sch`, and `.kicad_pcb` files as the source of truth. Preserve existing user work rather than rebuilding it to make it script-generated.

Prefer structured schematic editing, the official IPC API for supported PCB operations, and the real KiCad CLI for independent checks and exports. Keep substantial transformations in durable scripts. Use MCP for useful live-session inspection or small changes, and GUI control when a reliable structured operation is unavailable. Avoid turning one coherent edit into hundreds of opaque micro-calls.

## Find and use the latest local KiCad before choosing an API

Check all KiCad installations on `PATH`, system installation locations, and system/user package managers. Always search the entire home directory recursively for AppImages and portable installations, including hidden and ignored folders, even after finding a working installation. On Linux:

```bash
rg --files --hidden --no-ignore \
  --iglob '*kicad*.appimage' --iglob 'kicad-cli' "$HOME"
```

Check user-supplied paths and known symlinked installation directories too. Query each distinct installation's actual version using its CLI or supported launcher; do not infer it from filenames. Compare versions numerically, including prerelease ordering, and use the newest available locally. Report discovery or launch failures instead of silently falling back to an older version.

Record the verified executable or AppImage path, actual version, launch method, library paths, and Python environment in the project's existing environment notes. Reuse that record during the task; repeat discovery if it becomes stale, fails, or the user requests a different installation. Do not download another KiCad installation before completing local discovery. Respect an explicit user-selected version.

Use subcommand-specific `--help` before relying on syntax that may differ between KiCad versions.

For new PCB automation, prefer KiCad's official IPC API through the `kicad-python` package, imported as `kipy`. Do not start new work on the deprecated SWIG `pcbnew` Python bindings unless an existing project already depends on them and migrating is outside the task.

Detect whether the installed version supports the required IPC operations and whether they need a running PCB Editor or offer a headless launch path. Consult that version's help and official API documentation rather than assuming capabilities from a different release.

If a useful Python package is missing, first look for the project's documented environment, lockfile, requirements, or setup scripts. Add dependencies to a project environment only when appropriate, and make the dependency reproducible rather than relying on an unexplained global install.

## Understand the project before changing it

For an existing project, inspect at least the relevant:

- `.kicad_pro`, `.kicad_sch`, and `.kicad_pcb` files;
- `sym-lib-table` and `fp-lib-table` files when present;
- project-local symbol, footprint, and 3D-model libraries;
- custom design rules, net classes, stack-up, keepouts, and board constraints;
- existing scripts, jobsets, fabrication outputs, and documented workflows.

Preserve unrelated user-authored content. Do not silently replace custom symbols, footprints, design rules, board outlines, placement, routing, or manufacturing settings with generic defaults.

Before encoding a new part, obtain its reviewed pin mapping and package requirements. Verify the symbol pin numbers and footprint pad numbers, pitch, orientation, and exposed pad against that exact part. Preserve the supporting source in the project. Circuit selection and operating limits belong to the engineering workflow.

## Build schematics through structured operations

For substantial schematic creation or editing, prefer `kicad-sch-api` when it supports the required KiCad version and project features. It provides structured operations for symbols, wires, labels, hierarchy, connectivity, and file handling without requiring manual construction of KiCad S-expressions.

Keep important schematic-generation code in version-controlled Python where practical. Use stable references and descriptive net names, and make repeated values or design parameters explicit rather than scattering magic coordinates and strings through scripts.

When building a schematic:

- use verified library identifiers and exact symbol pin numbers;
- assign footprints deliberately rather than leaving production parts ambiguous;
- name important power and signal nets clearly;
- place decoupling and support components logically near the devices they serve;
- represent intentionally unused pins explicitly where appropriate;
- keep hierarchical boundaries and sheet names meaningful;
- preserve readable signal flow instead of merely satisfying connectivity;
- avoid overlapping symbols, labels, fields, wires, or junctions;
- do not use global labels everywhere just to avoid drawing understandable connections.

Treat third-party schematic libraries as helpers, not validators. After saving a generated or modified schematic, open or process it with the real KiCad installation and run KiCad's own ERC and export path. If the structured library cannot safely express a feature, use a documented lower-level file operation only for the smallest necessary part and verify the resulting file carefully.

### Run ERC after meaningful schematic changes

Prefer JSON output when available so failures can be inspected programmatically:

```bash
mkdir -p output/kicad-review
kicad-cli sch erc \
  --format json \
  --exit-code-violations \
  --output output/kicad-review/erc.json \
  project.kicad_sch
```

Adjust the command to the installed KiCad version when necessary.

Do not blindly suppress ERC warnings. Fix real electrical problems. If a warning is intentionally excluded, make sure the exclusion is justified by the circuit rather than used to make the report look clean.

## Apply design constraints and synchronise the PCB

Encode the engineering inputs in board setup: outline, stack-up, net classes, clearances, track/via sizes, copper-edge rules, keepouts, and relevant differential-pair or length rules. Check that net-class assignments and custom-rule scopes actually cover the intended nets. Do not invent electrical constraints merely to obtain a clean DRC report.

Use the supported KiCad update/import path to keep PCB footprints and nets synchronised with the schematic. Check references, footprint assignments, pad-net mappings, and parity after the update. Preserve mechanically constrained placements and unrelated routing.

## Use the official IPC API for live PCB work

For supported PCB Editor operations, prefer `kicad-python`/`kipy` over legacy `pcbnew` scripting. The IPC API provides structured access to the open board and supports transactional changes, board items, nets, footprints, geometry, and other PCB state according to the installed KiCad version.

For groups of related mutations, use KiCad transactions/commits when the API supports them so a coherent operation is applied and can be undone as a unit.

Keep substantial placement or routing logic in repository scripts where practical. Stable scripted transformations are easier to rerun, review, diff, and debug than a large number of one-off interactive calls.

Apply the reviewed placement and routing plan using the board's actual geometry and rules. Verify units, layer, rotation, and pad positions when transforming footprints. Keep schematic references and footprint identities stable across edits. Refill and save zones after meaningful copper changes before final DRC.

## Make kicad-cli the independent checker

A script finishing successfully does not mean the circuit or board is correct. Use the real KiCad CLI as an independent validation and export layer.

For PCB checks, prefer JSON DRC output and schematic parity when supported:

```bash
kicad-cli pcb drc \
  --format json \
  --schematic-parity \
  --exit-code-violations \
  --output output/kicad-review/drc.json \
  project.kicad_pcb
```

Use `--refill-zones` when appropriate for the workflow, or explicitly refill and save zones before the final check.

Inspect the report, not just the process exit status. Record errors, warnings, exclusions with reasons, and relevant checks configured as ignored. For an engineering audit, inspect those settings and run otherwise-disabled relevant checks in a review copy when needed; preserve the user's original settings. Never describe a report with exclusions or ignored checks as an unconditional clean bill of health.

Relevant problems include clearance violations, unconnected items, malformed board geometry, silkscreen-to-pad conflicts, courtyard collisions, track/via rule violations, copper-edge problems, and schematic/PCB mismatches.

If the project contains a `.kicad_jobset`, prefer using the project's existing jobset for repeatable outputs when it represents the intended fabrication workflow.

## Export and visually inspect the design

Electrical and geometric checks do not replace visual inspection.

Whenever useful, produce a small review bundle such as:

```text
output/kicad-review/
  erc.json
  drc.json
  schematic/
    *.svg
  pcb-front.png
  pcb-back.png
  pcb-3d.png
```

The exact files should fit the task. Do not generate unnecessary output just to satisfy a template.

For schematics, use `kicad-cli sch export svg` or another appropriate export and inspect every relevant sheet. Look for:

- unreadable signal flow;
- overlapping or clipped text;
- labels that appear connected but are not;
- accidental junctions or near-misses;
- inconsistent net naming;
- confusing power connections;
- excessive whitespace or cramped groups;
- symbols or fields positioned in ways that hide intent.

For PCBs, use `kicad-cli pcb render` and/or layer exports to inspect useful views. Render front and back views when both sides matter, plus a 3D perspective when component placement and mechanical relationships are important.

Look for:

- obviously poor placement or routing even when DRC-clean;
- connectors facing the wrong direction or blocked by other parts;
- polarity/orientation mistakes;
- silkscreen under components, pads, holes, or board edges;
- unreadable or inconsistent reference text;
- traces taking unnecessarily long paths;
- broken-looking return paths or copper pours;
- missing or implausible 3D models that may reveal footprint mistakes;
- components colliding with each other, mounting hardware, or enclosure constraints;
- board-edge, mounting-hole, antenna, keepout, and access problems.

If a problem is visible, fix it, rerun the relevant ERC/DRC, rerender the affected views, and inspect again.

## MCP is a live-session side channel

If a KiCad MCP server is available, use it when interacting with an already-open KiCad session is genuinely useful: inspecting current selection or state, exploring the live board, or applying a small interactive change.

Do not assume MCP is inherently better than Python, IPC, or the CLI. For substantial work, prefer durable scripts plus KiCad's structured interfaces. If an MCP server is mostly a wrapper around the same APIs, avoid turning one coherent operation into dozens or hundreds of opaque micro-calls.

Treat any MCP server capable of executing generated Python or modifying project files as powerful local code execution. Keep it local/trusted and respect the surrounding sandbox and approval model.

## GUI/computer control is supplemental

Use GUI automation when a visual editor interaction is genuinely required or when no reliable structured interface exists. Do not use mouse/keyboard automation for ordinary schematic or PCB mutations that can be expressed reliably through structured APIs or files.

## Manufacturing outputs

For a fabrication release, complete the relevant CAD checks and engineering review before exporting. An explicitly requested intermediate or quotation export can proceed with its revision and unresolved findings labelled; exporting does not make it fabrication-ready.

Use `kicad-cli`, a project jobset, or the project's established tooling for outputs such as:

- Gerbers or another required fabrication format;
- drill files;
- pick-and-place/position files;
- BOM data;
- STEP or other mechanical exports;
- assembly/fabrication drawings.

Generate the requested files from one saved project revision, using the existing jobset when suitable. Verify the BOM and placement references agree, including quantities, DNP exclusions, board side, origin, units, and rotations. Inspect plotted layers and drills for layer selection, outline, cutouts, and plated/nonplated holes. Check that assembly drawings and any supplier-specific files describe this same revision. Keep superseded exports separate so they cannot be mistaken for the current package.

## Handoff

Report the scope actually checked and KiCad version. Where applicable, include ERC/DRC findings and exclusions, unrouted count, and schematic/PCB parity; do not imply checks were run for an export-only task. For an independent pin audit requested by the engineering workflow, export connectivity and compare reference/pin/net tuples with the separately reviewed expected connections; include repeated pad numbers, exposed pads, and intentional no-connects.

Link the relevant schematic and PCB views and requested exports. Leave scripts, environment notes, and rule settings reproducible. Keep engineering assumptions and pending prototype measurements distinct from CAD results.

Consult the [KiCad manuals](https://docs.kicad.org/) for the installed version's operations and rule-checking behaviour.
