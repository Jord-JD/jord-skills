---
name: polite-browser-use
description: Use the browser in a way that doesn't disturb your human. Read this skill before doing any browser-based testing, including website/game previews, external browsers, and Electron apps.
---

Browser testing is good. However, if your human is using the computer you're testing on, your testing may disturb them if you don't take precautions.

# Keep browser testing silent

Sound can be especially annoying or confusing when it starts playing out of nowhere. You must not let your browser testing produce sound through your human's speakers.

* If you can mute the browser tab or process, do that before loading or interacting with the application. Confirm that it is muted if your tools let you check.
* If the browser cannot be muted reliably, modify the application to add a test-only mute mode before continuing. You are allowed to make this small change even when it isn't part of the main task.
* Prefer the application's existing mute setting or audio manager. Otherwise, add a focused automation setting using something like an environment variable, launch argument, configuration value, or query parameter.
* Enable the mute before the application sets up its audio. Make sure it covers music, sound effects, HTML media, Web Audio, and any new windows or views the application creates.
* Check that the mute is active before clicking or typing anything that could start playback.

Keep normal user launches unchanged. Headless or background mode does not necessarily mean muted.

If you need to test the actual audio output, send it to a silent recording or virtual output instead of the speakers. Ask your human before doing any test that they might hear.

# Don't pop up unexpected windows

Windows popping up can take focus away from whatever your human is doing. Internal browser previews are usually fine, but external browsers such as Chrome, Firefox, Brave, or Edge should run headlessly unless your human expects to see them.

# Clean up after yourself

Close the browsers and tabs you opened as soon as you're finished with them. Keep one open only when your human asked for it or the task needs it to remain available.
