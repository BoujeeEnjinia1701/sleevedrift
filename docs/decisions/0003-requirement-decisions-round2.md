---
doc_id: SVD-DDR-003
title: SleeveDrift requirement decisions, round 2
project: SleeveDrift
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Amish's decisions on R3 (1B), R9 (2A) and the R1 stretch (3C) carried into the model, calculations, BOM, drawings and build plan
---

# 0003: Requirement decisions, round 2

- **Date:** 2026-10-03
- **Status:** Decided by Amish Chadha, 2026-10-03: "i approve all of the 47 recommendations provided by you. Execute them." For SleeveDrift these are the three requirement decisions of SVD-DEC-001 (portfolio decisions 34, 35 and 36), each decided as recommended.

## Context

At TRL 3 (SVD-CAL-001 v0.1) the constructable design (SVD-DDR-002) missed R3, 1 m³ of loose spoil an hour moved 60 m by a two-person portal crew, at about 0.22 m³/h: one person cranking at a sustainable 60 W drags the 786 N loaded train at only 3.9 m/min, and the return, loading and tipping take as long again. R9, 72 hours without failure of rope, pulleys or sledges, could not be shown on paper because polyester braid abrasion on a gritty steel floor is not predictable without a test. The 600 mm stretch of R1 was not designed, because the crawl space, duct and return rope do not fit a 600 mm pipe in the same layout. The three were put to Amish with options and a recommendation in `docs/REVIEW.md` and SVD-DEC-001.

## Options considered

*Table 1. The three decisions put to Amish and the option chosen.*

| # | Requirement | Options | Chosen |
| --- | --- | --- | --- |
| 1 | R3, spoil haulage | A: hand cranking only. B: a portal drill drive on each winch socket, hand cranking as the fallback. C: B plus a six-sledge train and faster handling | **B** |
| 2 | R9, shift durability | A: inspect both ropes at every shift change and carry a spare set. B: an abrasion-resistant 10 mm rope. C: low rope rollers every 10 m on the floor | **A**, with the TRL 4 endurance trial deciding whether B is needed |
| 3 | R1 stretch, 600 mm pipe | A: drop the stretch. B: design a 600 mm variant now. C: keep it as a stretch until the co-design partner says whether 600 mm pipes are used for rescue | **C** |

## Decision

*Table 2. Each decision as carried into the design. Figures from SVD-CAL-001 v0.2 (`docs/04-calcs/sizing.py`).*

| # | Requirement | Option chosen | Effect on the design | Condition |
| --- | --- | --- | --- | --- |
| 1 | R3 | B: portal drill drive | A heavy-duty cordless right-angle drill with an adjustable slip clutch and a dead-man trigger, and a winch bit in the handle socket, on each winch (`drill_drive()` and the `drills` component in `cad/src/model.py`; the hand handles are stowed and refitted as the fallback). At 120 rpm in high gear the train moves at 14.5 m/min, 190 W at the rope loaded; a cycle is 17.3 min and the haul carries about 0.42 m³/h, 1.9 times the hand rate and 1.5 times the hand-dug face rate seen at Silkyara. Nothing is added inside the pipe (R8 unchanged). The clutch must be set between about 28 and 45 N m so it slips before the 2.5 kN swivel releases; that holds in high gear only. BOM line 30, two sets at USD 350: USD 700, about 7 kg (estimate) | R3 stays **not met** against 1 m³/h: loading and unloading dominate once the haul is powered. Hand cranking remains the fallback at 0.22 m³/h |
| 2 | R9 | A: inspect and carry spares | Both ropes are inspected along their length against a go/no-go wear gauge at every shift change (build plan safety stop 6) and a spare pull rope and tail rope are carried; a worn rope is swapped in about 20 min. BOM line 31, USD 236.50, about 15 kg in its own package. At the drill-drive rate 72 h is about 250 round trips and each metre of rope drags about 60 km over the floor | R9 stays **at risk on paper**; it is met in practice if the swap counts as maintenance, not failure. Planned TRL 4 step: the endurance trial shows the rope's wear rate and decides whether the abrasion-resistant rope of option B is needed |
| 3 | R1 stretch | C: keep it open | No change to the hardware; the ring, sledge and sheave sizes stay parameters in the model | The 600 mm stretch is **open, pending the co-design partner's answer** on whether 600 mm pipes are used for rescue. A second ring is designed only if the answer is yes |

## Consequences

- `cad/src/model.py` carries the drill drives on both winch sockets; the constructability checks report no overlaps and nothing floating.
- SVD-CAL-001 v0.2 is re-run: R3 0.42 m³/h (not met); R9 at risk on paper, met in practice with the inspection and spare set; R1 met for 800 mm, 600 mm stretch open; R10 still met, kit about 326 kg in 14 packages, heaviest 34.8 kg. A new line D6 gives the drill clutch torque window.
- Estimated cost of the constructable design: USD 10,804.00 (was USD 9,867.50), USD 5,804.00 over the USD 5,000 value-engineering target; `budget_usd` unchanged (it is the value-engineering target, SVD-DDR-001 item 13; Amish accepted overruns on 2026-10-03).
- STEP and STL, SVD-DWG-002 (Rev P3, portal station), the concept media, `media/model.glb` and the build plan pictures and making sketches are regenerated from the model. The photoreal renders made on Amish's Mac predate this change.
- New questions raised while carrying out the decisions (the drill's gear and clutch rule, and the wording of R9) are recorded in `docs/REVIEW.md` and SVD-DEC-001 as **Proposed, awaiting Amish**.
