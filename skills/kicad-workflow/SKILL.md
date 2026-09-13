---
name: kicad-workflow
description: "Edits, checks, renders, and exports KiCad schematics and PCBs. Use when creating, editing, routing, validating, rendering, or exporting KiCad files. Circuit and layout engineering also use electronics-design when available."
---

# KiCad workflow

Preserve `.kicad_pro`, `.kicad_sch`, and `.kicad_pcb` as project source, including custom libraries, rules, placements, and unrelated user work. Use structured operations and real KiCad validation. CAD checks do not prove electrical performance or safety.

## Environment and scope

Reuse the project's verified installation and environment. Confirm its executable version and required subcommand capabilities with `--help`; do not infer them from filenames. Respect a user-selected version. If no installation is recorded, check project setup and PATH first. Read [installation discovery](references/installation.md) when these fail, capabilities are missing, or the user requests the newest local version. Record a working path and version once for reuse.

Inspect the files, library tables, design rules, net classes, stack-up, and existing scripts relevant to the operation. Prefer project jobsets for repeatable exports when they match the request.

Use `electronics-design` when available for component selection, circuit changes, placement/routing strategy, or fabrication engineering review. An export, render, or file conversion does not require a new engineering review. If the companion is unavailable, establish necessary engineering inputs from requirements and authoritative component documentation before changing the design.

## Read only the needed procedure

| Operation | Reference |
| --- | --- |
| Schematic creation, connectivity changes, or ERC | [Schematic](references/schematic.md) |
| PCB synchronisation, constraints, placement/routing operations, or DRC | [PCB](references/pcb.md) |
| Rendering, visual inspection, or manufacturing outputs | [Exports and inspection](references/exports-and-inspection.md) |

Prefer structured schematic editing, supported official PCB IPC operations, and the real CLI for checks and exports. Keep substantial transformations in durable scripts. Reuse existing automation when migration is outside scope. Use MCP for useful live-session operations and GUI control when a reliable structured operation is unavailable. Respect the environment's code-execution and file permissions.

## Verification and completion

Verify symbol pins, footprint pad numbers, orientation, pitch, and exposed pads against reviewed requirements before encoding a new part. Preserve the supporting evidence. Run relevant ERC after schematic changes; after PCB changes refill/save affected copper, run DRC, and check schematic parity where supported. Inspect reports, warnings, exclusions, and ignored checks, not only exit status. Do not suppress a real problem to obtain a clean report.

Actually inspect relevant schematic sheets and board views. Fix visible connectivity, mechanical, or layout problems within scope and rerun affected checks. For an independent pin audit, compare exported reference/pin/net tuples against separately reviewed intended connections, including repeated pads, exposed pads, and intentional no-connects.

Generate requested outputs from one saved revision and verify file contents and settings relevant to their purpose. A quotation or intermediate export may retain labelled findings; a fabrication release needs the relevant CAD and engineering review. Exporting alone does not establish readiness to fabricate.

Continue through authorized operations and corrections. Report the version, scope checked, findings/exclusions, useful views and exports, and any unverified behaviour. Do not imply ERC, DRC, or engineering checks ran for an export-only task.
