---
name: screeps-world-ai
description: "Develops, diagnoses, optimises, and operates Screeps World bots, including CPU scheduling, movement, economy, room planning, expansion, and combat. Use for persistent-world Screeps AI work on official or private servers; Arena requires its own API and match rules."
---

# Screeps World AI

## Work within the bot's design

Establish the server, shard, runtime, deployment target, and requested outcome. Inspect the project's architecture, persistent state, build process, diagnostics, and tests before choosing an implementation. Adapt the guidance to role-based bots, task systems, schedulers, compiled code, and other architectures; do not introduce a particular framework just to follow this skill.

For a new bot, establish a working tick loop and a recoverable local economy before adding dependent systems. For an existing bot, trace the affected behaviour through its actual decision and execution paths. Reviews report findings without changing the colony unless changes are requested. Offline development can finish with local evidence and clearly stated live checks still outstanding.

Derive thresholds, force sizes, body designs, and economic policy from the actual environment and requested strategy. Keep room names, player relationships, shard choices, and manual orders in configuration or operation data. General behaviour should follow capabilities and state. Respect intentional manual controls and existing deployment authorization.

Consult the [official API](https://docs.screeps.com/api/) and the target server's engine or mods when mechanics are uncertain. For strategy research, inspect public bot implementations and observed player behaviour; distinguish an observed technique from an inferred policy or an untested idea. Account for differences in CPU, maturity, geography, and opponents before adopting it.

Read only the references relevant to the work:

| Work | Reference |
| --- | --- |
| Idle creeps, pathfinding, scheduling, initialization, or cache cost | [CPU and movement](references/cpu-and-movement.md) |
| Energy flow, spawning, recovery, upgrading, or remote mining | [Economy and remotes](references/economy-and-remotes.md) |
| Construction, base layouts, relocation, room selection, or growth gates | [Planning and expansion](references/planning-and-expansion.md) |
| Attack alerts, defence, offensive operations, or territory acquisition | [Combat](references/combat.md) |

## Diagnose from fresh evidence

For live work, record the running build and tick alongside the relevant room objects, decisions, and telemetry. Prefer existing API or console tooling for structured inspection; inspect room views when geometry, congestion, or formation behaviour matters. Do not infer live state solely from source code or stored summaries.

Check the age of the underlying measurement, not just its enclosing report. A refreshed dashboard can contain stale CPU samples, obsolete targets, or historical errors. Distinguish current visibility from remembered intelligence and unknown state from an observed empty room.

Trace the failure through selection, assignment, scheduling, intent, and resulting world state. A desired creep count, queued request, selected target, or successful API return does not establish useful work. Screeps resolves actions across ticks and has conflicts between intents; verify the resulting position, energy transfer, progress, damage, or ownership. See [game loop](https://docs.screeps.com/game-loop.html) and [simultaneous actions](https://docs.screeps.com/simultaneous-actions.html).

Tie each change to an observed failure or a measurable hypothesis. Choose acceptance evidence before changing the policy: for example, restored delivery with bounded CPU, a controller kept safe during bootstrap, or a combat objective completed within its budget. Include affected dependencies so a local improvement cannot conceal starvation elsewhere.

## Verify code and behaviour

Reproduce the relevant state with the project's existing tests or scenarios. Test transitions over ticks when the behaviour depends on deferred actions, replacement, movement, or persistence. Ensure regression tests are actually registered and run. Mocks must reproduce the API semantics involved in the failure; use an engine scenario or focused live probe when mocks cannot establish them.

Run checks appropriate to the change, including the project's required build and verification. For economic or scheduling changes, compare equivalent scenarios and time windows, including room-level losses that an empire total could hide. Preserve meaningful acceptance limits; report a tradeoff rather than weakening a failing check to fit the result.

When deployment is within scope, use the project's release process and identify the exact uploaded artifact. Compare the full expected module set with the selected live branch, including missing or obsolete modules, then confirm the intended build actually executes on the target shard. For compiled bots, compare build output rather than source files. A push or version marker alone is insufficient.

Observe affected behaviour after deployment. Separate initialization and cache warm-up from recurring performance, and leave enough unchanged ticks to assess the mechanism. Correct or revert attributable regressions within the authorized scope. Recheck live parity if another writer or importer changes the deployed code. Do not overwrite unexplained live changes with a stale local build.

## Monitor toward an outcome

Match observation cadence to the event: movement needs consecutive ticks; deliveries need complete trips; replacement economics need a representative lifecycle. Convert ticks to wall time using observed server timing when an ETA is needed.

When asked to monitor and improve, investigate anomalies and make justified corrections rather than leaving a snapshot collector as the finished result. A collector is useful when its output feeds an actual review or requested record. Healthy evidence can justify no further change. Avoid repeated deployments that prevent a stable observation window.

Use the requested duration, completion conditions, and scheduling mechanism. Do not create indefinite automation from a bounded monitoring request. Clean up temporary probes and collectors when their purpose ends, preserving useful results in the project's existing notes.

Report the implemented behaviour, tests and observations, deployed build when applicable, and remaining uncertainty. Keep code correctness, live execution, and sustained strategic or economic improvement as separate claims. Do not declare a room safe without current coverage or a remote profitable before the relevant costs have been measured.
