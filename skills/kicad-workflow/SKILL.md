---
name: kicad-workflow
description: Best-practice workflow for using KiCad. Use this skill whenever you create, edit, inspect, validate, lay out, route, render, export, or otherwise automate KiCad schematics and PCBs. Prefer structured schematic editing, the official KiCad IPC API for supported live PCB operations, and kicad-cli for ERC, DRC, rendering, and manufacturing outputs; use MCP or GUI control as optional live-session tools rather than the primary design interface.
---

# KiCad workflow

## Default approach

Treat the KiCad project files as the source of truth and prefer structured, reproducible operations over GUI automation.

For substantial work, prefer this order:

1. Inspect the existing project, KiCad version, libraries, design rules, and relevant source documentation.
2. Create or modify schematics through a structured schematic API such as `kicad-sch-api` when it is compatible with the project.
3. Use the official `kicad-python` IPC bindings for supported live PCB Editor operations.
4. Use `kicad-cli` for ERC, DRC, schematic exports, PCB renders, fabrication outputs, and other headless checks.
5. Inspect both machine-readable reports and visual outputs.
6. Iterate until the electrical, physical, and visual checks pass.
7. Use MCP when a live KiCad session is genuinely useful.
8. Use GUI/computer-control tools only for work that is awkward or unavailable through structured interfaces.

Do not turn a coherent schematic or PCB operation into a long sequence of opaque mouse clicks or granular MCP mutations when it can be represented in durable scripts or project files. The `.kicad_pro`, `.kicad_sch`, and `.kicad_pcb` files remain legitimate project artefacts; do not rebuild an existing project from scratch just to make it script-generated.

## Detect the installed KiCad before choosing an API

Start by checking the actual environment rather than assuming a KiCad release:

```bash
kicad-cli --version
kicad-cli --help
```

Use subcommand-specific `--help` before relying on syntax that may differ between KiCad versions.

For new PCB automation, prefer KiCad's official IPC API through the `kicad-python` package, imported as `kipy`. Do not start new work on the deprecated SWIG `pcbnew` Python bindings unless an existing project already depends on them and migrating is outside the task.

Be aware of the IPC execution model. KiCad 9 and 10 require a running GUI instance for IPC. KiCad 11 added headless IPC support through `kicad-cli`. Future releases may expand this further, so detect capabilities instead of hard-coding assumptions.

If a useful Python package is missing, first look for the project's documented environment, lockfile, requirements, or setup scripts. Add dependencies to a project environment only when appropriate, and make the dependency reproducible rather than relying on an unexplained global install.

## Understand the project before changing it

For an existing project, inspect at least the relevant:

- `.kicad_pro`, `.kicad_sch`, and `.kicad_pcb` files;
- `sym-lib-table` and `fp-lib-table` files when present;
- project-local symbol, footprint, and 3D-model libraries;
- custom design rules, net classes, stack-up, keepouts, and board constraints;
- existing scripts, jobsets, fabrication outputs, and documented workflows.

Preserve unrelated user-authored content. Do not silently replace custom symbols, footprints, design rules, board outlines, placement, routing, or manufacturing settings with generic defaults.

For new hardware or meaningful circuit changes, verify important component facts from authoritative sources before encoding them into the design. Check pin numbering, absolute maximums, recommended operating conditions, required decoupling, pull-ups or pull-downs, programming/debug connections, power sequencing, thermal requirements, connector pinouts, and layout guidance where relevant. Verify that the selected footprint matches the exact package, pitch, pad numbering, orientation, and exposed-pad requirements of the intended part.

For high-voltage, mains, high-current, RF, high-speed digital, precision analogue, power-conversion, USB, Ethernet, memory buses, antennas, or other layout-sensitive circuits, treat manufacturer layout guidance and the applicable electrical constraints as design inputs rather than guessing from appearance.

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

## Move from schematic to PCB deliberately

Do not treat PCB layout as an automatic formatting step after schematic capture.

Before routing, establish or verify:

- board outline and mechanical dimensions;
- mounting holes and mechanical keepouts;
- connector, button, antenna, display, heatsink, and other mechanically constrained positions;
- layer count and stack-up;
- net classes, clearances, track widths, via sizes, differential-pair rules, and impedance constraints where relevant;
- copper-to-edge rules and any creepage or isolation requirements;
- component height or enclosure constraints when relevant.

Use the supported KiCad update/import path to keep PCB footprints and nets synchronised with the schematic, then verify schematic/PCB parity rather than assuming it succeeded.

## Use the official IPC API for live PCB work

For supported PCB Editor operations, prefer `kicad-python`/`kipy` over legacy `pcbnew` scripting. The IPC API provides structured access to the open board and supports transactional changes, board items, nets, footprints, geometry, and other PCB state according to the installed KiCad version.

For groups of related mutations, use KiCad transactions/commits when the API supports them so a coherent operation is applied and can be undone as a unit.

Keep substantial placement or routing logic in repository scripts where practical. Stable scripted transformations are easier to rerun, review, diff, and debug than a large number of one-off interactive calls.

For placement:

- place mechanically constrained parts first;
- place decoupling capacitors and other local support parts close to the pins they serve;
- keep critical current and signal loops short;
- group related circuitry so the board is understandable;
- consider assembly access, connector reach, probe access, airflow, heatsinking, enclosure walls, and screw clearances;
- orient references and polarity markings for readable assembly where practical.

For routing:

- honour the project's net classes and electrical constraints;
- prefer simple, intentional paths over needlessly tortuous routing;
- minimise unnecessary vias on sensitive or high-current paths;
- handle differential pairs, controlled impedance, return paths, length constraints, guard structures, and RF geometry according to the circuit's actual requirements;
- refill zones after meaningful copper changes before final DRC;
- do not assume an autorouter result is production-ready merely because it completes.

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

Inspect the report, not just the process exit status. Relevant problems include clearance violations, unconnected items, malformed board geometry, silkscreen-to-pad conflicts, courtyard collisions, track/via rule violations, copper-edge problems, and schematic/PCB mismatches.

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

A good hybrid workflow is:

```text
project requirements + verified component data
  -> structured schematic edits
  -> KiCad ERC
  -> schematic export + visual inspection
  -> PCB synchronisation
  -> IPC-based placement/routing where supported
  -> KiCad DRC + schematic parity
  -> PCB renders + visual inspection
  -> iterate
  -> manufacturing outputs

optional: MCP or GUI interaction with a live KiCad session
```

## Manufacturing outputs

Do not generate fabrication files as the first proof that a board is finished. Generate them only after the intended final schematic and PCB have passed the relevant checks.

Use `kicad-cli`, a project jobset, or the project's established tooling for outputs such as:

- Gerbers or another required fabrication format;
- drill files;
- pick-and-place/position files;
- BOM data;
- STEP or other mechanical exports;
- assembly/fabrication drawings.

Verify that the requested files were actually written and correspond to the final board revision. When practical, inspect the plotted fabrication layers or reopen them in an appropriate viewer rather than trusting file existence alone.

## Finishing checklist

Before handing KiCad work back to the human:

- confirm the correct project and KiCad version were used;
- confirm important component pinouts, packages, footprints, and layout requirements came from reliable sources;
- rerun ERC and resolve or deliberately justify remaining findings;
- confirm the PCB is synchronised with the schematic;
- refill copper zones as required;
- rerun DRC with schematic parity and resolve or deliberately justify remaining findings;
- inspect final schematic exports for readability and accidental-looking connectivity;
- inspect final PCB front/back and 3D views where relevant;
- verify board dimensions, layer stack, net classes, clearances, mechanical constraints, and unrouted connectivity;
- verify requested Gerbers, drills, BOM, position, STEP, or other delivery files exist and reflect the final board;
- leave scripts, dependencies, design assumptions, and important parameters understandable for the next person who needs to modify the project.
