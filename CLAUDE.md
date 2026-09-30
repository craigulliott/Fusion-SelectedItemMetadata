# SelectedItemMetadata — Fusion add-in

Adds metadata about the selected item to Fusion's lower-right status readout, e.g.
`1 Sketch Point | projected from sketch 'Bellows Barrel'`. The facts shown will grow
steadily more specific to what is selected and its state.

## Current status
**Version:** 0.1.0 (MVP). Unit tests pass headlessly; not yet run in Fusion.
**Next step:** verify in Fusion — a projected sketch point and line, a joint origin in the root and inside a component, an edge (Fusion's readout must be unchanged), several items selected, clearing the selection, stopping the add-in (Fusion's readout must come back).

## Architecture
```
SelectedItemMetadata/
├── SelectedItemMetadata.py   entry point: run/stop -> lib.lifecycle
└── lib/
    ├── lifecycle.py          start/stop, the selection handler
    ├── events.py             pin() handler registry (M-7)
    ├── errors.py             report() -> Fusion's TEXT COMMANDS window
    ├── status.py             owns the status line
    ├── describe.py           SUBJECTS + TRAITS tables, describe(entity)
    ├── subjects/             what the entity is — one per selection, most specific class wins
    └── traits/               what is true about it — every one whose type and condition match
tests/headless/               unit tests, no Fusion needed
```
- **Adding a fact:** write the function(s) in `subjects/` or `traits/`, add one line to a table in `describe.py`, add a test file named after it. Ask: is this *what it is* (subject) or *something true about it* that depends on state or spans types (trait)?
- Most types need **no subject**: Fusion's readout already names them (`1 Sketch Point`). A subject is for types whose readout says too little (joint origin).
- A trait that should **replace** another rather than add to it gets a condition that cannot hold at the same time as the other's. There is no override mechanism, deliberately.
- `describe()` guards every subject, condition and text call: a failure is reported and costs only that fragment. Failures Fusion produces **as answers** (see `referencedEntity` below) are handled inside the trait and not reported.

## Conventions
- **Relative imports**, unlike ConstraintLens's `sys.path` insert + `from lib import`: all add-ins share one Python interpreter, so a second top-level `lib` would resolve to whichever add-in loaded first.
- **Handlers are pinned** (M-7) and never let an exception escape: they report through `errors.report()`, which logs rather than opening a dialog because it runs on every selection change.
- **Module state is reset on stop** (`status.restore`): Fusion keeps the module loaded across stop and run.

## Testing
```sh
cd tests/headless && python3 -m unittest discover
ruff check .
```
`tests/headless/stubs/adsk/` is a hand-written stand-in for the `adsk` package with Fusion's real class chain for the types used. `fakes.py` holds attribute-only fakes. Add a fake, not a mock framework.

## Verified Fusion API facts (2705.1.25, macOS, probed in Fusion 2026-09-30)
- **Status line**: reading `ui.statusMessage` returns Fusion's own readout (`'1 Edge | Length : 30.00 mm'`), already written when `activeSelectionChanged` fires. Writing it does not mark the document modified. Fusion's readout and ours share the one line, which is why `status.py` remembers what it wrote.
- **Rejected display routes**: custom graphics mark the document modified on every redraw (though they do not add undo steps); a transparent palette swallows clicks, scroll and keys over the model and always has a title bar.
- **referencedEntity** resolves for entities projected directly from a sketch entity, B-Rep vertex/edge/face/body or construction geometry. It *raises* `RuntimeError: InternalValidationError` — never returns None — for non-reference entities, the endpoints added with a projected curve, and included, intersected and unlinked geometry.
- **Joint origins**: a proxy's `parentComponent` is the component ('Bracket') and `assemblyContext` the occurrence ('Bracket:1'). `Component.allJointOrigins` lists one proxy per occurrence. `Joint.geometryOrOriginOne/Two` return the *native* joint origin, with the occurrence in `occurrenceOne/Two`.
- **Root component** is named after the document ('(Unsaved)', then the saved name).
- **activeSelectionChanged** fires for canvas, browser and timeline selections; not while another command runs. Rename and undo clear and restore the selection, so they fire it too.
- `Sketch.project2` sometimes returns an empty list while still creating geometry.
