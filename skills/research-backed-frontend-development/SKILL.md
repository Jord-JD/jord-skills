---
name: research-backed-frontend-development
description: "Designs and reviews interfaces using comparable products and visual verification. Use when creating or changing a UI or reviewing its appearance or interactions, across web, native, game, and embedded displays. Small fixes reuse established design evidence."
---

# Interface development

Build an original interface suited to its users, display, controls, and system constraints. Aim for excellent visual execution: coherent type, spacing, composition, imagery, and state feedback. Preserve the existing visual language for narrow changes. Clarity, accessibility, and safe operation take precedence over decoration.

## Route by the requested change

Inspect the existing interface, relevant project files, target display and controls, and accepted requirements first. Preserve the stack and unrelated user work. Resolve routine choices yourself; ask only about ambiguity that would materially change the requested result.

- **New product, screen, or substantial redesign:** Read [research](references/research.md), then [design](references/design.md). Use inspected comparisons to establish the direction, reuse applicable project evidence, and record the decisions it supports.
- **Existing interface change:** Inspect affected states and reuse the design system. Read [research](references/research.md) only if an unresolved design decision needs comparisons. A typo, spacing correction, or behaviour-preserving fix does not need a new product direction.
- **Review only:** Inspect the requested states and compare against the brief, established design, and relevant evidence. Report findings and limitations without modifying the project.
- **Design only:** Deliver the requested design and interaction specification. Do not start implementation unless asked.

Read [interaction contracts](references/interaction-contract.md) when changing flows, state transitions, or system integration. Read [implementation](references/implementation.md) for a new interface or substantial implementation. Load only the references that apply. The UI contract does not authorize unrelated backend, engine, or firmware changes.

## Verify the affected experience

Exercise the relevant journeys with the intended inputs in the closest available target environment. Check console, engine, application, or device diagnostics as applicable. Run the project's affected checks and expand testing only when failures or shared-system changes justify it.

Capture and actually inspect important states at target sizes and resolutions. Check hierarchy, spacing, clipping, legibility, contrast, focus, control feedback, and consistency. Include loading, empty, error, offline, and recovery states when affected. Tiny displays need inspection at their actual scale as well as enlarged detail.

For a new visual direction, compare captures against the declared ambition and strongest research evidence. Identify visible weaknesses, fix them within the brief, and recapture affected states. Use `visual-inspection-improvement` when available. Contact sheets can locate views; use individual images for detailed judgments.

Before operating browsers or previews, use `polite-browser-use` when available. Keep audio silent, avoid unexpected windows, and clean up task-owned tabs and processes. For other interfaces, use the relevant emulator, renderer, application, or authorized hardware. State what remains unverified when the real target is unavailable.

## Completion and handoff

Continue through authorized implementation and fixes until required interactions work, affected checks pass or their failures are explained, and inspected presentation meets the brief without unresolved visible defects within scope. A review finishes with supported findings; it does not require fixing them.

Report the result, important verification evidence, and material limitations. Include research sources and design decisions when they informed the work. A small fix needs a small handoff. Do not call the interface polished or production-ready as a substitute for evidence.
