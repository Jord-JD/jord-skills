---
name: electronics-design
description: Design and review electronic circuits, schematics, and PCB layouts, including component selection, power budgets, sourcing, manufacturing cost, and prototype validation. Use for new hardware, circuit changes, board layout decisions, or engineering audits in any CAD tool. Pure CAD export, rendering, or file conversion belongs to the tool-specific skill.
---

# Electronics design

## Scope and working sequence

This skill owns engineering decisions and the evidence needed to support them. Use the available CAD-specific skill for implementation; for KiCad, use `kicad-workflow`. CAD commands and file operations belong there. When lithium batteries are involved, also use `lithium-battery-safety` if available.

For new boards, establish requirements, architecture, component availability, and a manufacturing baseline before detailed layout. Review critical circuit placement before general routing, then check connectivity, electrical behaviour, and manufacturing outputs before release. These are work stages, not mandatory user approval stops. For a small change, apply only the stages affected by that change and check its interfaces to the existing design.

Keep decisions and evidence in the project's existing notes where possible. Match documentation to the task; a component substitution does not need a new design dossier.

## Establish the intended behaviour

Record the consequential requirements and assumptions before committing to an architecture:

- Power sources and supported voltage/load range; whether operation, charging, and programming must work simultaneously.
- Programming and recovery method, external connections, controls, and behaviours the user should not have to manage manually.
- Mechanical envelope, connector access and orientation, mounting, and environmental conditions.
- Performance targets, quantity, assembly method, preferred suppliers, cost target, and acceptable prototype limitations.

Use reasonable stated defaults when details are missing. Ask only when an unresolved choice materially changes the design or supported behaviour. Do not add modes, switches, connectors, or required accessories without considering the user's intended workflow. Preserve accepted decisions across revisions; reopen them only when new evidence requires it, explaining the conflict.

Inspect relevant reference designs early. When adapting a proven board, identify its exact revision, circuit, and operating assumptions. Reuse the approach where suitable, then check the effects of different loads, supplies, components, and firmware. A familiar product name is not evidence that the modified circuit meets the new requirements.

## Select circuits and parts before layout

Use manufacturer datasheets, application notes, package drawings, and reference layouts for the exact ordering codes. Record links and relevant revisions or sections. Verify pin functions and numbering, recommended operating conditions, startup and enable states, support components, programming connections, and layout requirements. Absolute maximum ratings are not operating targets.

Before committing to footprints and routing, read [sourcing and manufacturing](references/sourcing-and-manufacturing.md) when selecting purchasable parts, choosing fabrication options, reducing cost, or preparing a quote. Resolve foreseeable lifecycle, stock, and package-cost problems at this stage. Exploratory circuits may retain explicitly identified provisional parts.

For substitutions, compare electrical limits, timing or protocol, package and pinout, thermal needs, and support circuitry. Update affected schematic connections, footprints, layout, firmware, BOM, and validation together. Equal labels or a supplier's automatic match do not establish equivalence.

## Establish electrical constraints

Calculate relevant limits with tolerances and worst-case operating conditions, not just typical values. For power circuits, distinguish steady load, transient demand, source capability, conversion losses, voltage drop, and thermal dissipation. Record assumptions behind current ratings and runtime estimates. Battery capacity alone does not establish discharge capability.

Check behaviour during startup, shutdown, reset, brownout, unplugging and source switchover where applicable. Include programming/recovery and missing or crashed firmware when hardware behaviour depends on software. Record required firmware sequencing, pin defaults, clock handling, or load limits beside the circuit; do not rely on unspecified future firmware to make the design work.

Choose stack-up, trace/via geometry, clearance, return paths, impedance, and thermal measures from the actual circuit and manufacturing constraints. Use current manufacturer guidance and applicable standards for layout-sensitive interfaces, RF, power conversion, precision analogue, high voltage, and isolation. Do not infer compliance from connector type or a rule-checker pass.

## Plan placement and critical routing

Resolve the mechanical arrangement and critical circuit groups before general routing. Check connector mating space, cable access, mounting hardware, antenna clearance, component height, acoustic openings, and assembly/probe access as relevant.

Compare critical groups against manufacturer reference layouts. Identify and inspect the actual high-current loops, decoupling paths, switching nodes, feedback routes, ground returns, and thermal paths. Translate qualitative guidance such as "close to the pin" into a placement and copper path that can be inspected. Route sensitive and constrained connections before filling the remaining space.

Keep signal and current return paths continuous where required. Review layer transitions, zone boundaries, routing around keepouts, and interactions between noisy and sensitive circuits. A short trace or few vias is not automatically the better electrical route. An autorouter finishing does not establish layout quality.

Keep the schematic readable, with meaningful signal flow, circuit groups, net names, and explicit intentional no-connects. Check package drawings for pitch, pad numbering, exposed pads, polarity, and top/bottom view conventions. A plausible 3D model is supplementary evidence, not footprint verification.

## Review before fabrication release

Review against the requirements and component documentation without waiting for a separate user request to audit the design. Keep these forms of evidence distinct:

- **CAD evidence:** connectivity, schematic/PCB agreement, configured electrical and geometric checks, and visual inspection. Use the CAD skill for commands and reports; identify exclusions and unchecked constraints.
- **Engineering evidence:** calculations, pinout/package review, reference-layout comparison, operating and fault-state review, and any relevant simulation. Explain the limits of models and assumptions.
- **Physical evidence:** prototype measurements of the behaviours CAD cannot establish. Do not report tests as passed before performing them.

For generated designs or substantial connection changes, compare intended reference/pin/net connections against both schematic and PCB data. Derive the expected mapping from reviewed pinouts and circuit intent, not solely from the same generator that created both files. Include repeated pads, exposed pads, and intentionally unused pins. This catches transcription errors; it does not prove the circuit architecture correct.

Inspect schematic sheets and board layers as well as assembly views. Correct visible electrical or mechanical problems even when automatic checks pass. Recheck the affected design after fixes and ensure the delivered revision is the checked one.

Leave a practical prototype test plan for unresolved behaviour: what to measure, under which supply/load or fault condition, and the acceptance limit derived from the requirements. Distinguish readiness to fabricate a prototype from readiness for production. Do not require unrelated certification work for an ordinary prototype, or claim safety/compliance from CAD results.

## Deliver the requested result

Summarise the implemented behaviour, supported operating limits, material tradeoffs, verification performed, and measurements still outstanding. For design changes, identify effects on firmware, mechanics, sourcing, and existing manufacturing files. For fabrication or quotation work, follow the revision and quotation practices in the sourcing reference. Preserve useful reusable scripts and source evidence with the project.
