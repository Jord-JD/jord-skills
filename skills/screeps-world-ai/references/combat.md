# Combat

## Establish what is threatened

Attribute an attack alert to the creep or structure, location, time, and activity. Scout losses in an opponent's defended room need a different response from attacks on owned rooms or operating remotes. Tune expected-loss notifications without suppressing economically or strategically important alerts.

Use fresh visible state when available, with timestamps on remembered intelligence. Distinguish harmless visitors from bodies capable of damaging creeps, structures, or controllers. A WORK or CLAIM threat can matter to a structure or controller without justifying the same flight behaviour as melee or ranged damage to a creep. Reconcile diplomacy and ownership consistently across intelligence, selection, targeting, and retreat.

Project combat from active parts, boosts, range, healing, tower supply, cover, and relevant effects. Include hostile Power Creeps when supported by the environment. Check the [API](https://docs.screeps.com/api/) and [defence mechanics](https://docs.screeps.com/defense.html) for the exact interactions rather than relying on nominal body counts.

## Coordinate defence and movement

Focus damage where it can overcome healing and cover. Avoid unnecessary target switching that repeatedly abandons nearly defeated targets, while allowing armed threats to interrupt lower-value work. Coordinate distinct working or firing positions so support units do not block attackers.

Distinguish own and hostile ramparts, and own and hostile safe mode. Consider tower refilling and repair supply when estimating sustained defence. A planned perimeter is ineffective until its structures are built, maintained, and reachable by defenders and repair crews.

Pursuit should reflect the target's threat and the squad's movement capability. Stopping at firing range may let a retreating target escape; advancing into melee may lose a ranged unit. Coordinate healing, retreat, border crossing, and regrouping so specialists do not arrive unsupported.

Count combat-capable forces rather than merely living creeps with a matching role. Damaged survivors without useful offensive parts should not prevent needed replacements. Ensure cleanup of remote or economic assignments cannot cancel valid home defence or military missions.

## Define operations by objective

Give operations explicit objectives, stages, sponsors, commitments, and completion conditions. Useful distinctions include income raids, core destruction, reservation denial, siege, holding territory, and acquisition for mining or settlement. These objectives need different bodies and evidence of success.

Derive force composition from current opposition, safe transit, travel time, specialist lifetime, reinforcement delay, and counterattack risk. Keep target-room opposition separate from transit danger: the intended enemy should not accidentally make its own supply corridor appear hostile twice.

Allow affordable objectives that fit the strategy. A distant mining raid may be feasible even when reservation breakers cannot arrive with useful life remaining. Conversely, clearing creeps does not finish an order that also requires removing reservation or holding the room.

Budget spent energy and pending commitments across all stages and simultaneous operations. Reserve shared sponsor and spawn capacity when a force is committed so two planners cannot each spend the same allowance. Respect explicit limits and manual overrides; generalize their mechanism rather than embedding historical rooms, player names, or campaign sizes in policy.

When launch conditions fail, report the actual reason and arrange actionable follow-up such as priority scouting or a later capacity review. Keep retries bounded and respond to changed evidence. A terminal operation should not immediately recreate itself from stale target data.

## Verify transitions and outcomes

Test selection, staging, engagement, reinforcement, retreat, completion, and cleanup where affected. Include NPC and player cases relevant to the implementation rather than assuming one target filter works for every mission type. Preserve active troop assignments and defensive coverage during operation-schema migrations.

Observe the ordered result: structure destroyed, reservation removed, hostile production disrupted, territory held, or economic handover completed. Record what remains contested. End or reassess operations according to their objective and budget rather than leaving automatic reinforcement active forever.
