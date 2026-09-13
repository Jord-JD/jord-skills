# Apply design constraints and synchronise the PCB

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
