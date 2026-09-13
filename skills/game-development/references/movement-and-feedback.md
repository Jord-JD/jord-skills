# Make it feel good

Feel is not polish to add at the end. It is whether the game is worth playing. The numbers below are optional starting values for responsive action games. Choose values that fit the genre, play, and tune. Preserve deliberate existing behaviour when fixing an unrelated issue.

For a platformer with a conventional ballistic jump, derive the physics from the feel you want instead of guessing gravity. Choose a jump height `h` (three to four tiles is typical) and a time to apex `t` (0.30 to 0.40 s). Then gravity is `2h / t^2` and the jump velocity is `2h / t`. On top of that:

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

When introducing these effects or controls, account for accessibility: a screen shake slider, a way to disable flashing, control remapping with conflict detection, and a rule that the player can never unbind the key they need to reach the menu.
