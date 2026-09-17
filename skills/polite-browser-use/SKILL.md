---
name: polite-browser-use
description: "MANDATORY: read and apply before any browser, Electron, or live-preview operation, including hidden previews, navigation, interaction, screenshots, and recordings. Keep audio silent, avoid disruptive windows, and clean up task-owned tabs and processes."
---

# Polite browser use

Keep browser work silent and out of the user's way. Apply these rules before the first operation, including hidden previews. Search APIs, HTTP retrieval, and reading saved screenshots do not trigger this skill.

**Mute before audio can start.** Mute the tab, process, or application before navigation or interaction that could play sound. Cover HTML media, Web Audio, music, effects, and new windows. Inspect the mute state when available; headless, hidden, or background operation does not prove silence. Do not press Play or Start without reliable muting.

Prefer existing mute controls. If those are insufficient and editing the application is authorized, use a focused test-only mute mode enabled before audio initializes; keep normal launches unchanged. Never modify third-party or read-only applications to silence them. Otherwise use a silent environment or skip the audio-producing interaction and report the limitation. Test actual audio through silent recording or virtual output; get permission before testing through speakers.

**Avoid disruptive windows.** Use headless external browsers and hidden internal previews unless the user expects a visible window. Avoid stealing focus or changing the user's browser settings.

**Clean up what you opened.** Close task-owned tabs and stop task-only browsers and servers when finished, unless they need to remain available for the task or the user asked to keep them. Never close the user's tabs or kill a shared browser to clean up your own work.

Use an explicit tab-close control and verify removal when possible. Hidden, detached, and unavailable do not mean closed. Do not claim closure from hiding, navigation, or `window.close()` alone. If the tools cannot close a tab or verify closure, report that briefly and accurately.
