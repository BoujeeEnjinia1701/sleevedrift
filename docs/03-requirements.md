---
doc_id: SVD-REQ-001
title: SleeveDrift requirements
project: SleeveDrift
doc_type: Requirements
version: "0.4"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2 update; concept status for every requirement; R11 (overload limit) and R12 (gas monitoring) added under Amish's pre-approval (SVD-DDR-001)
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3 status from SVD-CAL-001 on the constructable design (SVD-DDR-002); targets unchanged
- version: "0.4"
  date: '2026-10-03'
  author: Amish Chadha
  change: Status after Amish's round 2 decisions (SVD-DDR-003, 1B, 2A, 3C) from SVD-CAL-001 v0.2; targets unchanged
---

# SleeveDrift requirements

Ten of the twelve requirements are met on paper or by design; R3 (spoil haulage) is not met, R9 (shift durability) is at risk on paper, and the 600 mm stretch of R1 is open. Amish decided the three items on 2026-10-03 (SVD-DDR-003): a portal drill drive on each winch socket, with hand cranking as the fallback, doubles the haul to about 0.42 m³/h (R3, still short of 1 m³/h); the ropes are inspected every shift and a spare set is carried, with the TRL 4 endurance trial deciding whether a tougher rope is needed (R9); the 600 mm stretch stays open until the co-design partner answers (R1). Targets are unchanged from the scaffold; R11 and R12 were added at TRL 2 (SVD-DDR-001). The figures in the status column come from the calculation note SVD-CAL-001 v0.2 and are estimates on paper, not test results; every requirement is verified by test at TRL 4 or later.

> **Safety:** These requirements describe equipment used by people inside a rescue pipe under collapse debris. Meeting them on paper does not make the kit safe to use; it is published as an open engineering reference, not certified rescue, mining or confined-space equipment.

*Table 1. Requirements, with their status at TRL 3.*

| ID | Requirement | Target | Verification (TRL 4 or later) | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | Fits the pipe | Every part passes through and assembles inside an 800 mm nominal pipe; hood and ring variants for 600 mm (stretch) | Fit trial in pipe sections | Met on paper for 800 mm: every piece passes a 776 mm circle in a 780 mm bore. 600 mm stretch open: kept as a stretch until the co-design partner says whether 600 mm pipes are used for rescue (SVD-DDR-003) |
| R2 | Hood protection | Hood carries a 5 kN (1,124 lbf) distributed load with no contact with a test head form | Load test on CalRig | Met on paper: 5.5 MPa in the crown, tip deflection under 0.1 mm |
| R3 | Spoil haulage | At least 1 m3 (35 ft3) of loose spoil per hour moved 60 m (197 ft) by a two-person portal crew | Timed trial in a 60 m pipe run | Not met: about 0.42 m³/h with the portal drill drive (SVD-DDR-003); 0.22 m³/h by hand, the fallback |
| R4 | Haul force | Portal crank force under 200 N (45 lbf) with loaded sledges over 60 m | Force gauge during trial | Met on paper: 92 N at the start in high gear, 30 N in low gear, when cranked by hand; the drill drive takes the haul in normal use |
| R5 | Fresh air at the face | At least 1 m3/min (35 ft3/min) of fresh air delivered at the face over 60 m of duct (target, to be checked against confined-space guidance) | Anemometer at duct outlet | Met on paper: about 15 m³/min at the face |
| R6 | Casualty evacuation | A 100 kg (220 lb) manikin moved 60 m through the pipe in under 5 minutes | Timed drill | Met on paper: about 3.5 min with three people hauling hand over hand |
| R7 | Rapid set-up | Kit installed and hauling within 2 hours of arriving at the portal | Timed deployment exercise | Met on paper: about 1.6 h estimated |
| R8 | No power in the pipe | Zero electrically powered items inside the pipe except battery lamps and signal devices | Design review | Met by design: battery lamps, gas monitors (alarm devices) and sound-powered telephones only; the battery drill drives stay at the portal |
| R9 | Shift durability | 72 hours of continuous operation without failure of rope, pulleys or sledges | Endurance trial | At risk on paper: rope abrasion over about 250 round trips at the drill-drive rate cannot be shown on paper. Met in practice if a rope swap counts as maintenance: ropes inspected at every shift change against a wear gauge, a spare set carried (SVD-DDR-003); the TRL 4 endurance trial decides whether an abrasion-resistant rope is needed |
| R10 | Transportable | Whole kit in cases no heavier than 40 kg (88 lb) each, moveable by road and by hand to the portal | Weighing and handling trial | Met: heaviest package 34.8 kg; kit about 326 kg in 14 packages with the spare ropes and drill drives |
| R11 | Overload limit | Rope tension limited to 2.5 kN (562 lbf) by a release at each end of the train or stretcher; every part sized on that limit | Release test of the swivel pins; proof load on CalRig | Met by design: rope factor 6.5 on the release load |
| R12 | Air monitoring | Oxygen, carbon monoxide, hydrogen sulphide and flammable gas monitored continuously at the face and at the portal, with alarms | Design review; bump test before each shift | Met by design: two four-gas monitors in the kit |

## Assumptions

- The rescue pipe is steel of 800 mm outside diameter with a 10 mm wall (780 mm bore), as at Silkyara; the fit trial confirms the bore and the weld beads.
- Experienced hand miners or trained rescue crews will be available to use the kit.
- A blower and some power are available at the portal; nothing inside the pipe uses mains power.
- The pipe is pushed forward by other means while crews dig; SleeveDrift does not push pipe.
- The pipe is horizontal or on a slight grade, so the train does not run away when a winch is eased.
