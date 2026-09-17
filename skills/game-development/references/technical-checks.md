# Technical checks

Read only the sections relevant to the change. Preserve working engine conventions; these checks do not require a new architecture or test harness.

## Simulation and input

Use the engine's established loop. Keep physics updates stable and movement, timers, and effects independent of rendering frame rate. Bound catch-up after slow frames; handle pause, focus loss, and resuming without a large simulation jump. Use seeded randomness when reproducibility matters.

Map inputs to actions and preserve required input methods. Check physics bodies, collision shapes, layers, and masks before working around failed collision. Use swept collision or continuous collision detection for fast objects that can cross thin obstacles between steps.

## Movement and feedback

For ballistic jumps, height h and time to apex t imply gravity 2h/t² and initial upward speed 2h/t. Adjust to the game's actual physics and coordinate system. Consider jump buffering, coyote time, and variable jump height when they suit the genre; playtest their boundaries rather than applying fixed timing defaults.

Keep camera following frame-rate independent. Apply camera shake to its offset, not the player body. Drive hit-stop recovery with unscaled time so it can finish while simulation is paused. Preserve useful buffered inputs. Check that flashes, shake, scaling, and audio envelopes return to rest; support reduced effects where needed.

## Procedural worlds

Derive visuals, collision, and hazards from consistent world data and time. Keep existing terrain until its replacement is ready. Test delayed generation, rapid direction changes, and boundaries for visible holes or stale collision. Add streaming only when the world's scale needs it.

## Persistence

Use the platform's storage mechanism and save serializable data. Preserve existing saves, version formats when needed, and verify migration and interrupted-write recovery. Use safe replacement and backups where the storage API supports them. Keep settings, long-term progress, and disposable run state separate when their lifetimes differ.

## Performance

Profile the affected scene before optimising. Compare equivalent scenes, inputs, seeds, settings, and measurement windows. Separate warm-up from steady behaviour. Identify whether CPU, GPU, memory, or loading is the bottleneck; avoid speculative pooling or spatial structures.

Record the target and renderer. Software-rendered headless timings cannot establish a player's GPU frame rate. Verify appearance and controls after optimisation, as well as measured performance.
