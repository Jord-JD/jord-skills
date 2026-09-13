---
name: polite-browser-use
description: "Keeps browser and Electron operation silent and unobtrusive, and cleans up task-owned tabs and processes. Use when launching or controlling a browser, Electron app, or live preview; apply before the first operation."
---

Browser testing is good. However, if your human is using the computer you're testing on, your testing may disturb them if you don't take precautions.

# Apply before browser operation

Apply before launching or controlling a browser, Electron app, or live preview, including navigation, interaction, snapshots, and recordings. Hidden or internal previews still count. Search APIs, HTTP document retrieval, and reading saved screenshots do not operate a browser and do not trigger this workflow.

# Keep browser testing silent

Sound can be especially annoying or confusing when it starts playing out of nowhere. You must not let your browser testing produce sound through your human's speakers.

* Mute the browser tab, process, or application before loading a page that may play audio or interacting with the application. Do not click Start, Play, or a similar control until silence is verified.
* If the browser cannot be muted reliably and the task authorizes editing this application, add a focused test-only mute mode before continuing. Otherwise use an available silent environment or stop the audio-producing interaction and report the limitation. This does not authorize modifying a third-party or read-only application.
* Prefer the application's existing mute setting or audio manager. Otherwise, add a focused automation setting using something like an environment variable, launch argument, configuration value, or query parameter.
* Enable the mute before the application sets up its audio. Make sure it covers music, sound effects, HTML media, Web Audio, and any new windows or views the application creates.
* Inspect the actual mute or audio-enabled state when the tools expose it. Do not infer silence from headless, background, hidden, or internal-preview operation.

Keep normal user launches unchanged. Headless or background mode does not necessarily mean muted.

If you need to test the actual audio output, send it to a silent recording or virtual output instead of the speakers. Ask your human before doing any test that they might hear.

# Don't pop up unexpected windows

Windows popping up can take focus away from whatever your human is doing. Internal browser previews are usually fine, but external browsers such as Chrome, Firefox, Brave, or Edge should run headlessly unless your human expects to see them.

# Clean up after yourself

Close the browsers and tabs you opened as soon as you're finished with them. Keep one open only when your human asked for it or the task needs it to remain available.

Hidden, backgrounded, detached, automation-unavailable, and closed are different states. A false `visible` or `available` value does not by itself prove that the user-visible tab is gone. Use a tab-management control that explicitly closes the tab, then verify the user-visible tab no longer exists.

If the available tools cannot close the user-visible tab, say so plainly before finishing. Never report a tab as closed based only on automation detachment, `window.close()`, navigation, or hiding the preview.

Stop test-only servers and browser processes you started unless the human asked you to leave them running.
