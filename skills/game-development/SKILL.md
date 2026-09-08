---
name: game-development
description: Read before creating or changing any game or game feature, in any engine or framework, including Godot, Unity, Unreal, Phaser, PixiJS, Three.js, Bevy, pygame, LÖVE, Roblox, and plain canvas or WebGL. Applies to prototypes, jam games, web games, and full projects. Defaults to delivering the full requested game in the first turn with AAA-level quality as the target. Covers working out what the game is, building a proper game loop, making controls feel good, producing real art and sound, testing by actually playing, and building in an order that keeps the game playable.
---

Most games made by agents are playable in the loosest sense. The loop runs, the character moves, and nobody wants to play it twice. The tells are always the same: assets drawn in code, a jump that feels like a lift, no feedback when anything happens, tinny beeps from an oscillator, a HUD that looks like a form, and a hand-off message that says "the game is complete" when nobody, including the agent, has played it.

This skill is about avoiding that. It is engine-neutral. The engine's own documentation and any engine-specific skills you have tell you the API. This tells you what to do with it.

Rule of thumb: don't tell your human a game or feature works until you have played it and looked at it.

# Deliver the complete game in the first turn

Aim to deliver a full, complete, high-quality AAA game in the first turn, with the user's brief defining the game. Treat AAA-level craft as the target for controls, art direction, animation, sound, level design, pacing, interface, performance, and completeness. A request for a small game still calls for a finished experience. Follow an explicit request for a prototype or a narrow feature, but never assume the user wants either because the work is substantial.

The first turn includes the research, implementation, asset production, playtesting, and revisions needed to finish. Keep working through those steps before the final response. Do not hand over a vertical slice, demo, scaffold, or roadmap in place of the requested game, and do not wait for another prompt to add the remaining content or polish. Make routine creative and technical decisions yourself within the brief.

Track every requested mechanic, mode, level, and player-facing state through implementation and verification. Temporary placeholders are internal development aids and must be replaced before delivery. Integrate finished art, animation, audio, and feedback throughout development. Do not reserve them for a future polish pass.

Use the quality target to guide the work, then describe the delivered result honestly. If an actual tool, access, or execution limit blocks completion, exhaust available alternatives, complete unaffected work, and state exactly what remains blocked. Do not pre-emptively shrink the brief because it sounds ambitious or label an incomplete result AAA.

# Skills to read alongside this one

Read these when they are available. They cover parts of game work in more depth than this file does.

* `game-development-asset-generation` before making any image, texture, sprite, model, sound effect, music, or voice. It explains why code-drawn assets look bad and which services to use instead.
* `research-backed-frontend-development` for menus, HUDs, inventories, settings screens, and any other interface, and for the research step below. Its section on researching comparable interfaces applies to game screenshots and wikis as much as websites.
* `view-video` when researching gameplay footage or reviewing a recording of the game. Extract timestamped frames, actually inspect them, and read any relevant subtitles. Inspect short sequences more densely when movement, pacing, or feedback matters.
* `visual-inspection-improvement` whenever you are judging how the game looks. Take close-up screenshots of real states, look at each one, fix, and repeat.
* `polite-browser-use` before the first browser or preview action. Games play sound. Mute first.
* `natural-writing` for anything a player reads: tutorials, dialogue, item descriptions, menus, error messages, and the README.

# Start from the project, not from habit

Before writing anything, find out what is already there.

* Detect the engine and version from the project files: `project.godot`, `*.uproject`, `Assets/` with `ProjectSettings/ProjectVersion.txt`, `Cargo.toml` with a bevy dependency, `package.json` with phaser, pixi.js, or three, and so on. Read the pinned version and use that version's API. Do not silently migrate a Phaser 3 project to Phaser 4 or a Godot 3 project to Godot 4.
* Follow the project's existing structure, naming, input mapping, art style, and asset pipeline. A new feature should look like it was made by the same person as the rest of the game.
* For a new game, pick the engine that fits the target platform, the genre, and what your human already knows. If the brief leaves it open, choose one, say why, and move on. Do not pick by hype and do not default to a raw canvas because it needs no dependencies. Raw canvas is fine for a small 2D game. It is a poor choice for anything with physics, a scene tree, or a lot of UI.
* Do not converge on the same answers every time: 800x600, one big file, arcade physics, the same scene layout. Match the game in front of you.

# Know what the game is before you code it

Write down, in a few lines, what the game is. Not a design document. Just enough to stop yourself building a static scene and bolting mechanics onto it later.

* The primary verb. Jump, shoot, match, build, sneak, negotiate. Everything else supports this.
* What the player is promised and what it should feel like. "Precise and fast" and "slow and dreadful" lead to very different code.
* The objective, the pressure that makes it hard, the reward, and what happens on failure.
* The first minute. A title screen or main menu is fine and most games have one, but it should be short and lead straight into play. Do not open with a web-style landing page, a wall of instructions, or a settings screen. Once play starts, the player should be doing the primary verb within a few seconds, and the first minute should contain at least one real decision and one reward or feedback moment.
* What is out of scope. Write this down so you don't drift into it.

Then research at least three games that do the same thing. Read official pages, store listings, guides, wikis, fandom pages, reviews, and forum threads, and open the screenshots on those pages. Use `view-video` to inspect relevant gameplay footage, such as developer demonstrations and player playthroughs. Prefer footage showing ordinary play when studying mechanics and pacing; a promotional montage may omit the transitions and downtime that matter. If footage is inaccessible, use the available screenshots and written sources and state the gap.

Look at how the games teach the verb, how quickly the first threat arrives, how movement and feedback unfold, how the HUD reads during action, and how their menus work on a controller. Keep source URLs and timestamps for useful observations, and inspect a denser sequence around important moments. Do not infer exact timing or input responsiveness from sparse stills. Wikis are especially useful because they document mechanics with numbers: jump heights, invincibility frames, enemy health, wave timings, and the controls list. Every screenshot you find or capture must be opened and looked at, not just listed. Note what to keep, adapt, and avoid, then design something original for this game. Follow the research process in `research-backed-frontend-development`.

Plan the complete game before implementation, including its content, progression, ending or repeatable loop, menus, settings, and recovery from failure as appropriate to the brief. Implement and test the primary verb early, then keep building and refining the full game in the same turn. Use playtesting to improve the mechanic and its teaching while preserving the user's requested design.

# Build the loop properly

The most common technical faults in agent-made games come from the loop.

* Simulate on a fixed timestep, usually 50 or 60 Hz, and render as often as the display allows. Use an accumulator and cap the number of physics steps per frame (five is a common limit) so a slow frame doesn't spiral. Interpolate rendered positions between physics steps if movement looks juddery.
* Scale every movement, timer, and tween by delta time, except inside the fixed step where the step itself is the delta. A game that runs faster on a faster monitor has this bug.
* Use the engine's physics body and movement functions instead of adding to position yourself. If `is_on_floor()` or its equivalent is always false, the cause is usually a missing collision shape, the wrong up direction, or a layer and mask mismatch, not the engine.
* Keep fast, small bodies from tunnelling. Speed divided by physics rate must be smaller than the thinnest wall, or enable continuous collision detection.
* Map raw keys, buttons, and touches to named actions such as `jump` and `interact`, and have gameplay read actions only. Support keyboard, gamepad, and touch where the platform allows it. Use a radial deadzone of about 0.2 for sticks, rescaled from the edge of the deadzone, not a per-axis clamp.
* Use one seeded random number generator for everything that affects gameplay. Store the seed in the save. Never call the global unseeded random in a gameplay path. This makes bugs reproducible and makes automated tests possible.
* Keep game state as plain data. Saves, level definitions, wave tables, dialogue, and item stats are data that the engine objects are built from, not the objects themselves.
* Emit events from gameplay (`hit`, `landed`, `picked_up`, `died`) and have the HUD, audio, particles, and camera subscribe. Do not poll health every frame from the UI and do not put a sound call in the middle of collision code.
* Handle pause, focus loss, tab visibility, resize, and orientation change. A browser game that keeps simulating in a hidden tab and then applies ten seconds of delta on return is broken. Audio in browsers needs a user gesture before it can start, so start it from the first click or key press.
* Start with a state machine for entities and screens. Reach for an entity component system only when you have thousands of entities and profiling says you need it.

# Make it feel good

Feel is not polish to add at the end. It is whether the game is worth playing. The numbers below are starting values that real games converge on. Set them, play, and then tune.

For anything with jumping, derive the physics from the feel you want instead of guessing gravity. Choose a jump height `h` (three to four tiles is typical) and a time to apex `t` (0.30 to 0.40 s). Then gravity is `2h / t^2` and the jump velocity is `2h / t`. On top of that:

* Coyote time of 0.08 to 0.12 s, so a jump pressed just after leaving a ledge still works.
* A jump buffer of 0.10 to 0.15 s, so a jump pressed just before landing fires on landing. Consume both timers when the jump happens.
* Variable jump height by cutting upward velocity to 40 to 50% when the button is released early.
* Fall gravity 1.5 to 2 times rise gravity. This is the single biggest lever on how a jump feels.
* Reach top run speed in 0.05 to 0.1 s and stop faster than you accelerate.

For impacts, one satisfying hit is several small responses firing together within about 100 ms of the input. Pick two or three of these per event and scale them with how important the event is:

* Camera shake driven by a trauma value between 0 and 1, with the actual shake proportional to trauma squared, sampled from noise rather than a new random offset each frame, applied to the camera offset and never to the body. Roughly 0.15 for a pickup, 0.4 for a hit, 0.7 for an explosion, decaying at around 1.5 per second. Cap the offset at 8 to 16 pixels in 2D.
* Hit-stop of 40 to 90 ms at a time scale of about 0.05, on heavy hits only. Drive it with a real-time timer, because a timer that uses scaled time never finishes at scale zero. Keep the camera, HUD, and tweens on real time. Keep buffered input alive through the freeze.
* Squash on landing to around 0.9 and stretch on take-off to around 1.15, returning over about 180 ms with an ease-out-back curve.
* A brief flash, a few particles, a short field-of-view punch, a pitch-varied sound, and rumble on a pad. Vary sound pitch by about 6% so repeated hits don't sound like a sampler.

Every effect must return to rest. If the screen is still shaking three seconds later, or the character is left stretched, that is a bug.

Camera follow should be frame-rate independent. Use `t = 1 - exp(-rate * dt)` with a rate of about 5 to 12, or the engine's smooth damp. Add a dead zone so small movements don't drag the camera, look ahead in the direction of travel, and clamp the view to the level bounds. Follow in the late update or equivalent, after the target has moved.

Response to input should be visible within about 100 ms. If it isn't, find out why before adding anything else.

Add accessibility options from the start rather than retrofitting them: a screen shake slider, a way to disable flashing, control remapping with conflict detection, and a rule that the player can never unbind the key they need to reach the menu.

# Look and sound like a real game

Art, sound, and interface are where agent-made games most often fall apart, because they are the parts the agent is least equipped to do alone.

* Read `game-development-asset-generation` and use it. Textured sprites and models from an image or 3D generator, or from Blender, beat rectangles with gradients every time. Write down the art direction in a sentence first (palette, era, material, mood) so every generated asset comes from the same world, and reuse the same style prompt for all of them.
* Check that characters and threats read at the size they appear on screen, in motion, against the actual background. Distinct silhouettes matter more than detail. If the player can't tell the enemy from the scenery in a screenshot, redo it.
* When you load a spritesheet, open the file and measure the frame size, margin, and spacing. Do not assume. Wrong frame sizes are the usual cause of sprites that flicker or show slivers of the neighbouring frame.
* Build menus and the HUD with anchors and containers, never absolute pixel positions, so they survive resizing and different aspect ratios. Respect the platform's safe area. Give every screen a focused element on open so a controller can drive it, and keep the screens as a stack so back always works. Follow `research-backed-frontend-development` for the rest, and treat the HUD as an interface someone reads at speed while something is trying to kill them.
* Route audio through buses (master, music, sound effects, ambience, user interface, voice), and convert slider values to decibels instead of multiplying the volume linearly, or quiet settings will sound almost as loud as full. Duck the music slightly under important effects and dialogue. Free one-shot players when they finish, or pool them.
* Generate sound effects and music with a proper service or from real samples. A Web Audio oscillator is a placeholder. Keep the overall mix from clipping and roughly consistent in loudness between tracks.

# Play it before you say it works

The game is not done because it compiles or because the tests pass. You must play it.

* Make the game drivable from a script. For a web game, expose a function that advances the simulation by a given number of milliseconds in fixed steps, and a function that returns the current game state as compact text or JSON, including the mode, player position and velocity, entities, score, timers, and a note on the coordinate system. For engine projects, use the engine's headless mode, test runner, or an in-game debug console that accepts the same actions. This is what makes automated play reproducible instead of flaky.
* Drive real inputs through the real input path. Do not call the jump function directly and call that a test of jumping.
* Test causal chains, not single inputs. Shooting an enemy lowers its health, at zero it disappears and the score changes, collecting the key opens the door. Reset the game between scenarios. Change one thing at a time.
* Take screenshots during play at the moments that matter: the first screen, the busiest moment of combat, the pause menu, the game over screen, the moment after a big hit. Open each one and look at it. Check that the canvas is not blank or almost black, that the HUD is readable over the busiest background, and that effects have returned to rest. Do this at a desktop size and a phone size if the game targets both. Follow `visual-inspection-improvement` for the loop.
* Read the console, engine output, and logs after every session. Fix the first new error before doing anything else.
* Measure performance instead of guessing. A 60 Hz game has 16.7 ms per frame. Profile a release build on the weakest target you can get, look at whether the CPU or the GPU is the bottleneck, and only then optimise. Avoid allocating inside the hot loop and pool objects that spawn often, such as bullets and particles. Batch draws with atlases and instancing. Do not add a quadtree because it seems like a game should have one.
* Play it as a new player would. Can you do the primary verb on purpose within thirty seconds without being told? Did you want to go again after failing? If the honest answer is no, work out why, change it, and play again. Keep iterating on your own until the answer is yes, and only bring it to your human if the fix would change what they asked for. Do not describe the game as fun, polished, or satisfying unless you can point at what you played that makes it so.
* Keep debug overlays, god mode, and level skips behind a flag that is off in normal builds.

Before any browser or preview session, apply `polite-browser-use`. Mute the tab or add a test-only mute before the game starts its audio, keep external browsers headless, and close what you opened.

# Saving, settings, and shipping

* Save plain data, not engine objects: position, health, inventory, unlocked flags, seed. Include a save version integer from the first version. Write to a temporary file, flush, and rename, and keep a backup, because renames are not always atomic. Migrate old saves through an ordered chain and refuse saves from a newer version rather than corrupting them. Autosave to its own slot, on safe boundaries such as room transitions, not more than about once a minute.
* Persist settings separately from saves. Defaults should be sensible on first run without a settings file.
* Keep run state and profile state apart in games with permadeath, so dying wipes the run and not the unlocks.
* Do not publish, upload, or submit the game anywhere unless your human asks you to. This includes itch.io, Steam, app stores, and any generation service that offers hosting.

# Build in the right order

Agents build in the wrong order. A menu system, an inventory, a dialogue tree, and a crafting system, and no one has confirmed the jump feels good.

* Organise implementation around dependencies while keeping the full deliverable in view. Get input and the core loop working early, integrate production assets and feedback as systems become playable, and test throughout. Internal implementation checkpoints are not hand-off milestones.
* Complete every requested system, level, mode, and content set in the same turn. Play through progression and transitions as well as individual mechanics. Fix weak presentation, pacing, and feedback before handing over; do not offer to add them later.
* Before the final response, reconcile the implemented game against the full brief and resolve every remaining actionable gap. A working opening level or an attractive screenshot does not establish that the game is complete.

# Writing in the game

Player-facing text is part of the game, and the flowery, over-explained tutorial prompt is one of the clearest tells of an AI-made game. Apply `natural-writing`. Name the button and the result. "Hold R2 to aim, release to throw. Guards investigate the sound." is a tutorial. "Master the art of distraction!" is not. For dialogue, item text, and story, look at how games in the same genre and tone do it, then write original copy that fits this game's voice. Keep line IDs in data rather than matching on the text so translation and edits don't break references.

# Self review

Before handing over, check the work against this file. In particular:

* You completed the full requested game or feature in this turn, including its content and presentation, rather than stopping at an internal checkpoint. Any remaining gap has a concrete blocker.
* You detected the engine and version and used its conventions, and you didn't migrate anything without being asked.
* You can say in a sentence what the primary verb is and why it should be fun, and you tested it throughout the complete game.
* You researched comparable games and looked at the screenshots you took.
* The simulation runs on a fixed step, movement is delta-scaled, gameplay randomness is seeded, and input goes through named actions.
* Feedback exists for the important events, with values you tuned by playing, and everything returns to rest.
* Art, sound, and music are real assets in a consistent direction, made with the tools in `game-development-asset-generation`, not shapes and oscillators, unless the game's existing style calls for that.
* Menus and the HUD survive resizing, work with the intended controls, and are readable over the busiest scene.
* You played the game through scripted input on the real input path, opened every screenshot, checked the console, and fixed what you found.
* You have not published anything.
* Your hand-off says what you played, what you saw, what you didn't get to, and what remains unverified, without calling the game finished or fun on faith. "No controller support yet", "placeholder music in level 2", and "untested on mobile" are useful to your human. A vague "some polish remaining" is not.

If anything above is untrue, fix it before you hand over.

# Examples

## Example 1 - Adding a jump

Your human has asked for a jump in a 2D platformer built in Godot 4.

### Bad

The assistant adds `velocity.y = -400` on key press, adds gravity, runs the scene once to confirm no errors, and reports that jumping now works.

### Good

The assistant reads `project.godot`, sees Godot 4.4, and checks how the player scene already handles input actions. It sets a jump height of 3.5 tiles and a time to apex of 0.35 s and derives gravity and jump velocity from those. It adds coyote time of 0.1 s, a 0.12 s jump buffer, a release cut to 45%, and 1.8 times gravity on the way down. It adds a small squash on landing and a pitch-varied jump sound from an existing effect. Then it drives the level with scripted keyboard and pad input, jumps a gap from the very edge of the platform, presses jump just before landing, and checks from the state output and screenshots that both still fire. It reports the values it settled on, what it changed after playing, and that the highest platform in level 3 is now reachable, which might not be intended.

## Example 2 - Making a whole game

Your human has asked for "a small space shooter I can play in the browser".

### Bad

The assistant writes one HTML file with a canvas, draws the ship as a triangle and the enemies as red squares, adds oscillator beeps through Web Audio, uses `Math.random` for spawns, runs everything off `requestAnimationFrame` with no delta time, and hands over a message saying the game is complete with smooth controls and satisfying feedback. Nobody has played it. It runs twice as fast on a 120 Hz monitor.

### Good

The assistant writes down the brief: the verb is dodging and shooting, the feel is fast and arcade, the pressure is escalating waves, the reward is score and a new weapon. It reads the wiki and store pages for three space shooters, opens their screenshots, and notes how they signal incoming fire, how their HUD sits over the playfield, and what the first wave looks like. It picks Phaser, sets up a fixed step with seeded spawns, named input actions for keyboard and touch, and a state and step hook for testing. It implements the controls and combat, plays them, and fixes slow ship turning while building the full game. It generates a ship, three enemies, a tileable starfield, shot and explosion effects, and a short loop of music using the tools from `game-development-asset-generation`, all from one style prompt. It adds shake, hit-stop on the boss hit, and a pitch-varied hit sound. In the same turn, it completes escalating waves, the weapon pickup, a boss, a title screen, pause, game over with restart, and a high score that persists. It plays through the whole thing with a script with the tab muted, opens the screenshots, sees the score is unreadable over the starfield, and adds a backing panel. It checks the whole brief, replaces every temporary asset, and replays the finished game after fixes. The first-turn hand-off delivers the playable game, lists what was played and the screenshots, and notes that touch works in emulation but was not tested on a real phone.

## Example 3 - Reporting on a game feature

Your human asks whether the new boss fight is ready.

### Bad

Assistant: Yes, the boss fight is complete and fully polished. It features three distinct phases, dynamic camera shake, satisfying hit feedback, and a challenging but fair difficulty curve.

### Good

Assistant: It works, but I wouldn't call it ready. I played it six times. Phases one and two are fine. Phase three's laser sweep hits you from off-screen because the camera is still locked to the boss, so it feels unfair rather than hard. I'd widen the camera in that phase before you try it. Screenshots of all three phases are in `qa/boss/`. Not yet tested on a pad.
