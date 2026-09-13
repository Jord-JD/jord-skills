# Keep procedural worlds consistent

Apply these rules when terrain, water, or other generated environments affect gameplay; a small fixed level does not need a streaming system.

* Derive visible surfaces, collision, and hazards from the same seeded data and simulation time. For moving water, the surface and buoyancy should agree. For terrain, validate that rendered ground and contact geometry describe the same location and generation.
* Treat readiness as a contract. A traversable patch is ready only when its visuals, collision, and relevant hazards are ready together. Keep coarse terrain or the previous tile visible until its replacement is ready; do not remove coverage merely because generation has started.
* Test transitions as well as steady states, including delayed generation and rapid changes of direction. Check for holes, falling through visible ground, stale collision, and abrupt changes between levels of detail. Choose streaming and refinement machinery only when the world's scale requires it.
