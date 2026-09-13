# Performance checks

Use for optimisation work or a demonstrated performance problem.

* Measure performance instead of guessing. A 60 Hz game has 16.7 ms per frame. Profile a release build on the weakest target you can get, look at whether the CPU or the GPU is the bottleneck, and only then optimise. Avoid allocating inside the hot loop and pool objects that spawn often, such as bullets and particles. Batch draws with atlases and instancing. Do not add a quadtree because it seems like a game should have one.

* For performance changes, compare the same scene, seed, input sequence, quality settings, and measurement window before and after. Record warm-up conditions, sample count, average and percentile frame intervals, and relevant resource counters. Include device, browser or engine version, renderer backend, and whether rendering uses hardware or software. Software-rendered headless timings support comparisons in that environment, not claims about a player's GPU frame rate. Counters do not measure shader execution time. Check appearance and controls again after optimisation.
