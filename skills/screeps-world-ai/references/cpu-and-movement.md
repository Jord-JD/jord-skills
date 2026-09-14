# CPU and movement

## Trace apparent inactivity

Before changing movement logic, inspect the creep across several ticks:

- Whether it is spawning, already in working range, intentionally waiting, or fatigued.
- Its assigned job, target validity, carried resources, active body parts, and remaining life.
- When its decision code last ran and whether a budget or priority rule skipped it.
- Which intents were issued, their return codes, and whether later code replaced them.
- Actual position changes, path reuse, blockers, and room transitions.

A stationary miner can be productive; an unfatigued traveller with stale execution timestamps may never have issued a move. Clear obsolete stuck state when arriving or changing jobs. Do not report newly spawning creeps as stalled travellers.

## Spend CPU on useful work

Measure total tick cost and the relevant phases. Include initialization, cache population, scheduling, role execution, diagnostics, and memory handling where applicable. The first caller of a shared cache may be charged for work used by many creeps; profile the underlying operation before blaming the role.

Distinguish sustainable CPU allocation from the current tick ceiling and bucket reserve. Observe bucket trend over comparable warm windows. A full bucket cannot grow, so zero growth there does not establish lack of headroom. Read the target's actual limits rather than assuming an account subscription or allocation. See [CPU limits](https://docs.screeps.com/cpu-limit.html).

When scheduling is involved:

- Keep priority and budget policy understandable in one place where practical. Avoid accumulating independent gates that disagree about whether work can run.
- Protect essential actions and their prerequisites: defence needs supply; spawning needs energy collection; upgrading needs controller feeding.
- Bound waiting time and track last execution, not merely desired cadence. Stale high cost estimates must not exclude a task forever.
- Split expensive searches into resumable steps. Persist enough state to make progress after interruption, and invalidate it when its inputs change.
- Stagger periodic work and bound emergency bypasses. Promoting every task to critical recreates CPU exhaustion.

Compare useful output as well as CPU. A cheaper loop that suppresses harvesting or delays short-lived CLAIM creeps until they expire is a regression. Selectively cache or defer planning before reducing productive intents without measurement.

## Keep caches valid and recovery affordable

Separate tick-local object caches, resettable runtime caches, and durable serialized state. Store IDs and compact data for later ticks, reacquire current objects, and handle missing objects or lost visibility. Reconstruct positions using supported API types when methods require them; test the actual overload rather than assuming a plain object behaves identically.

Cache keys and invalidation should reflect the dependencies that matter, such as topology, target, ownership, danger, or plan version. Bound cache and diagnostic history growth. Schema migrations should preserve active work and tolerate partially completed transitions. The [caching overview](https://docs.screeps.com/contributed/caching-overview.html) describes the different persistence and cost characteristics.

Profile reset initialization separately from warm execution. If eager loading or cache rebuilding exhausts startup CPU, keep the entry path small and defer or batch expensive setup where the runtime permits. Recovery must remain possible with a low bucket; repeated reset or load retries should not consume all available CPU without making progress. Attribute console-expression errors separately from errors in deployed modules.

## Handle routes, borders, and traffic

Separate inter-room routing from movement to a working position. Validate connectivity and the intended corridor; map proximity does not prove a usable route. Inspect incomplete pathfinder results and search limits before labelling a target unreachable. Increase search work only within a measured budget.

For border oscillation, check the requested next room, chosen exit, cached path, and entry recovery together. After a forced inward step or job handover, invalidate movement state that would send the creep back out. Restrict searches to the destination room when the job should stay there, while allowing legitimate routes that must leave and re-enter because of terrain.

Use bounded recovery for failed crossings rather than trying neighbouring exit tiles indefinitely. Preserve legitimate edge destinations, retreat paths, and combat positioning. Regression cases should include both directions of a crossing and a destination inside the room.

Give stationary workers and idle guards positions that preserve source access, controller approaches, spawn exits, and hauling lanes. Coordinate traffic ownership and recovery so two units do not repeatedly swap goals or block each other. Do not trigger expensive repathing every tick for ordinary congestion.

Keep route geometry separate from trip duration. Remove loops from routes considered for paving, but retain delay and backtracking in measured transport performance until the underlying cause is fixed. Verify movement through actual subsequent positions; an accepted move intent can still lose a collision.
