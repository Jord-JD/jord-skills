# Export and visually inspect the design

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
