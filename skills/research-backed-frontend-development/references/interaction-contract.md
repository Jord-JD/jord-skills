# Define the UI/system contract

Map each important journey as an interaction slice:

```text
human input
  -> immediate visual, audible, or physical feedback
  -> UI state transition
  -> application, engine, firmware, device, or service operation
  -> validation, permission, or safety check
  -> data, network, sensor, or hardware result
  -> visible state and recovery path
```

Omit stages that do not exist. A static page may have no operation. A local game menu may have no server. An embedded controller may have no conventional backend.

Define what the task needs:

- UI states, transitions, modes, invariants, and impossible combinations;
- input events, long presses, repeats, shortcuts, focus rules, and debounce behaviour;
- the data model and application, engine, firmware, device, or service interfaces that drive the UI;
- inputs, outputs, errors, timing, and ownership at each boundary;
- validation, permissions, safety interlocks, and destructive-action confirmation;
- loading, retry, cancellation, disconnection, offline use, restart, and power-loss recovery;
- persistence, synchronisation, defaults, and migration of saved settings;
- latency, frame time, memory, draw-call, bandwidth, refresh, and power budgets where they matter;
- logs, telemetry, analytics, and audit events when the product requires them;
- fixtures, simulated sensors, fake services, or emulator states needed to exercise realistic conditions.

The backend is optional. The contract is between the interface and whatever drives it.

Use the smallest architecture that satisfies the interaction. Do not add services, abstractions, or hardware assumptions because a reference product might use them. Observable behaviour can suggest a requirement. It cannot reveal another product's implementation.
