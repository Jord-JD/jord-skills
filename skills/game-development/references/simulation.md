# Build the loop properly

Use these checks when creating or changing real-time simulation. Preserve an existing engine loop that already meets the requirements.

* Simulate on a fixed timestep, usually 50 or 60 Hz, and render as often as the display allows. Use an accumulator and cap the number of physics steps per frame (five is a common limit) so a slow frame doesn't spiral. Interpolate rendered positions between physics steps if movement looks juddery.
* Scale every movement, timer, and tween by delta time, except inside the fixed step where the step itself is the delta. A game that runs faster on a faster monitor has this bug.
* Use the engine's physics body and movement functions instead of adding to position yourself. If `is_on_floor()` or its equivalent is always false, the cause is usually a missing collision shape, the wrong up direction, or a layer and mask mismatch, not the engine.
* Keep fast, small bodies from tunnelling. Speed divided by physics rate must be smaller than the thinnest wall, or enable continuous collision detection.
* Map raw keys, buttons, and touches to named actions such as `jump` and `interact`, and have gameplay read actions only. Support the input methods required by the brief. Use a radial deadzone of about 0.2 for sticks, rescaled from the edge of the deadzone, not a per-axis clamp.
* Use one seeded random number generator for everything that affects gameplay. Store the seed in the save. Never call the global unseeded random in a gameplay path. This makes bugs reproducible and makes automated tests possible.
* Keep game state as plain data. Saves, level definitions, wave tables, dialogue, and item stats are data that the engine objects are built from, not the objects themselves.
* Emit events from gameplay (`hit`, `landed`, `picked_up`, `died`) and have the HUD, audio, particles, and camera subscribe. Do not poll health every frame from the UI and do not put a sound call in the middle of collision code.
* Handle pause, focus loss, tab visibility, resize, and orientation change. A browser game that keeps simulating in a hidden tab and then applies ten seconds of delta on return is broken. Audio in browsers needs a user gesture before it can start, so start it from the first click or key press.
* Use the existing entity and screen architecture. For a new game, choose the simplest state representation that supports the requested behaviour.
