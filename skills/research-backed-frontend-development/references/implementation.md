# Build complete interaction slices

Implement one working user task at a time, including the interface states, underlying behaviour within scope, and relevant verification. If the assignment is UI-only, use the existing contracts and do not rewrite the system behind them.

Build the chosen art direction into the first slice. Do not leave the interface visually generic and promise to add its identity in a final polish pass.

While building:

- derive visual values from the agreed system rather than scattering one-off colours, dimensions, and timing values;
- use suitable platform primitives, such as semantic HTML, native controls, game-engine UI components, or the existing embedded drawing library;
- support the intended input method, including visible keyboard or controller focus, touch targets, button mappings, encoder steps, and a reliable way back;
- render correctly at the target sizes, orientations, safe areas, pixel densities, colour depths, and physical viewing distance;
- keep action and state names consistent from control to result;
- make startup, loading, empty, validation, warning, permission, error, disconnected, success, and destructive states deliberate when they can occur;
- replace placeholder icons, imagery, textures, and effects with assets that fit the direction when the task and available tools permit it;
- tune typography, spacing, alignment, surfaces, focus treatments, transitions, and responsive or state changes as one system rather than isolated decorations;
- avoid controls that do nothing and placeholder data that survives into a real path;
- watch CSS specificity for web work, anchors and draw order in game engines, native layout constraints in apps, and buffers, repaints, flash, and RAM use on embedded displays;
- keep performance within the target's limits, including images, fonts, animation, list size, draw calls, device polling, network requests, and display refresh;
- preserve relevant accessibility and safety behaviour. Use redundant cues when colour, sound, or a single indicator is not enough.

Prototype shortcuts are fine when the user asked for a prototype. Name them as shortcuts and keep the boundary clear.

### Write interface copy as part of the design

Apply `natural-writing` to interface copy, documentation, research notes, and the final handoff when that skill is available.

Use the terms real users and comparable products use, but write original copy for this product. Prefer plain verbs and specific nouns. A control says what it will do. The same action keeps the same name through confirmation and error states. Errors say what happened and what the user can do next. Empty states point to a relevant first action. Remove filler, slogans, and claims the product cannot prove.
