# Research comparable interfaces

Use this process when a new direction or unresolved design decision needs external evidence. For a new product or substantial flow, inspect several relevant interfaces with different strengths. Choose enough evidence to resolve the decision rather than collecting a fixed quota. Reuse current project research. For a small change that preserves the design, inspect the existing interface and affected states; no fresh competitor research is required.

Search is only discovery. Use the browser to open the actual product or the best available evidence of it. Before the first browser action, read and follow the available browser-safety instructions, such as `polite-browser-use`. Do not enter private areas, create accounts, start trials, or submit data unless the user has authorised it. Close tabs and stop test processes when the work is finished.

### Choose useful comparisons

Include whichever comparisons expose the real design problem:

- direct alternatives used for the same job and in the same medium;
- products with similar controls, display limits, or usage conditions;
- adjacent products that solve the same interaction or information problem;
- a strong reference outside the category when it offers a useful pattern the direct alternatives lack.

At least one reference should earn its place because its visual execution is exceptional, even if it sits outside the product category. Functional competitors can teach conventions, but a group of bland competitors sets a low ceiling.

Prefer live products, interactive demos, official screenshots, manuals, app-store pages, game footage, device footage, source repositories, and detailed reviews. Design galleries, award pages, templates, and search-result thumbnails show isolated frames without proving how an interface works.

A website can be researched through its live pages. A game may require game footage and screenshots of HUDs, menus, inventories, or other states. A hardware interface may require its manual, product videos, emulator, firmware repository, or close-up photos of the display and controls. If the real product is inaccessible, say which evidence you used instead.

### Inspect, capture, and record

For each reference:

1. Open the relevant product, demo, recording, manual, or image source.
2. Examine the screens, physical controls, states, and transitions that matter to the task.
3. Capture focused screenshots or video frames at useful states and sizes. Use emulator captures, render captures, or device photos when the target is not browser-based.
4. Open and inspect every capture. Taking a screenshot without looking at it is not research.
5. Record the source URL, product and state, access date, and screenshot path.
6. Write down what was observed separately from what was inferred.

Pay attention to:

- navigation, hierarchy, grouping, density, and the order in which information appears;
- the mapping between controls and results, including focus, selection, shortcuts, back behaviour, and accidental activation;
- layout behaviour across screen sizes, orientations, safe areas, resolutions, and fixed pixel grids;
- legibility at the real physical size and viewing distance;
- composition, focal point, visual rhythm, density, layering, image treatment, and the details that make the strongest frames feel finished;
- typography, colour or monochrome roles, spacing, borders, icons, imagery, animation, sound, haptics, and indicator lights;
- forms, menus, inventories, HUD elements, gauges, alerts, settings, search, filters, and destructive actions when present;
- startup, onboarding, loading, empty, success, error, warning, disconnected, offline, sleep, and recovery states;
- response time and the feedback shown while software, a network, a sensor, or a physical mechanism catches up;
- accessibility, platform conventions, redundant warnings, and safety-related behaviour;
- signs of the underlying system, such as entities, permissions, device modes, persistence, sensor states, connectivity, timing, power loss, and hardware faults.

A compact evidence table is usually enough:

| Reference | Screen, state, or control | Screenshot | Observed pattern | System implication | Keep, adapt, or avoid |
| --- | --- | --- | --- | --- | --- |

Label system implications as inferences unless the product documents them. A visible delay may imply asynchronous work. It does not reveal whether the product uses a queue, a thread, a network request, or a slow sensor.

Screenshots are research evidence, not permission to reuse another product's art, copy, logo, or distinctive composition. Learn the conventions people depend on, then make a design that belongs to this product.

If web or browser access is unavailable, use supplied screenshots, recordings, manuals, local builds, emulators, and hardware documentation. Say what could not be inspected. Never invent sources, observations, or screenshots.

## Synthesize before designing

Turn the research into decisions. A useful synthesis names:

- the conventions shared by several references and why users may expect them;
- the strongest solution to each important interaction problem;
- recurring weaknesses, clutter, hidden modes, or confusing states to avoid;
- gaps where this product can be clearer or easier to control;
- the visual benchmark the finished interface should meet, with specific reference frames and the qualities worth matching;
- the software, service, or hardware capabilities implied by the desired experience;
- which findings apply to this medium and which do not.

Then write a short product direction with one concrete audience, one primary job, the usage conditions, the main journeys, and the states each journey can enter. If the evidence contradicts the initial idea, revise the idea. Do not collect screenshots merely to justify a decision already made.
