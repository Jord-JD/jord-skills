# Build schematics through structured operations

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
