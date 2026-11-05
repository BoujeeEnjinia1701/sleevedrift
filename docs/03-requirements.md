---
doc_id: SVD-PRS-001
title: SleeveDrift product requirements and specifications
project: SleeveDrift
doc_type: Product requirements and specifications
version: "0.6"
status: Draft
date: 2026-11-02
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold (as SVD-REQ-001)
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
  change: "Status of R1, R3, R8 and R9 updated for Amish's decisions 24B, 25A and 26C of 2026-10-03 (SVD-DDR-003): portal drill drive, rope inspection and spare set, 600 mm stretch held for the co-design partner; targets unchanged"
- version: "0.5"
  date: '2026-10-04'
  author: Amish Chadha
  change: "R3 restated by Amish's round-3 decision 4A (SVD-DDR-004): moves loose spoil faster than the face produces it, at least 0.4 m3/h; met at 0.42 m3/h"
- version: "0.6"
  date: '2026-11-02'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: renamed SVD-PRS-001 (was SVD-REQ-001); the twelve requirements R1 to R12 migrated to PR-001 to PR-012 with the old number in the Was column, each traced to a user requirement in SVD-URS-001; PR-013 (cost), PR-014 (workshop build) and PR-015 (signals) added from the user needs; no target changed; status of PR-013 recorded as over target"
---

# SleeveDrift product requirements and specifications

What the kit must do, each requirement traced to a user need in SVD-URS-001 (links in SVD-RTM-001). The requirements describe option A, the rope shuttle of sledges, which is the current design and is **proposed, awaiting Amish** as the choice among the three concept options (SVD-OPT-001). Of the fifteen, thirteen are met on paper or by design and one is managed by inspection and spares until the endurance trial (PR-009); **PR-013 (cost) is over the value-engineering target** at USD 10,804.00 of parts against USD 5,000. Targets are unchanged from the scaffold except PR-003, which Amish restated on 2026-10-04. The figures in the status column come from the calculation note SVD-CAL-001 and are estimates on paper, not test results; every requirement is verified by test at TRL 4 or later.

Amish, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed." For SleeveDrift that decided three items as recommended (SVD-DDR-003): a portal drill drive on each winch for the haul rate (24B), rope inspection every shift with a spare set for shift durability (25A), and the 600 mm stretch of PR-001 held until the co-design partner answers (26C). On 2026-10-04 Amish decided option 4A: "For round 3, I agree with all your proposed recommendations". PR-003 is restated as "moves loose spoil faster than the face produces it; at least 0.4 m3/h" (hand-dug faces make about 0.27 m3/h) and is met at 0.42 m3/h (SVD-DDR-004).

> **Safety:** These requirements describe equipment used by people inside a rescue pipe under collapse debris. Meeting them on paper does not make the kit safe to use; it is published as an open engineering reference, not certified rescue, mining or confined-space equipment.

*Table 1. Product requirements and specifications. Status at TRL 3 from SVD-CAL-001 (python docs/04-calcs/sizing.py).*

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-007 | Physical architecture | Fits the pipe | Every part passes through and assembles inside an 800 mm nominal pipe; hood and ring variants for 600 mm are a stretch | 776 circle in a 780 bore | max | mm | Analysis, SVD-CAL-001 A (TRL 3); fit trial in pipe sections (TRL 4) | Met on paper for 800 mm: every piece passes a 776 mm circle in a 780 mm bore. 600 mm stretch open: held until the co-design partner says whether 600 mm pipes are used for rescue (decision 26C) | R1 |
| PR-002 | UR-001 | Safety | Hood protection | The hood carries a 5 kN (1,124 lbf) distributed load with no contact with a test head form | 5 | min | kN | Analysis, SVD-CAL-001 B (TRL 3); load test on CalRig (TRL 4) | Met on paper: 5.5 MPa in the crown, tip deflection under 0.1 mm | R2 |
| PR-003 | UR-002 | Performance | Spoil haulage | Moves loose spoil faster than the face produces it; at least 0.4 m3/h (14 ft3/h), moved 60 m (197 ft) by a two-person portal crew (restated 2026-10-04, decision 4A; hand-dug faces make about 0.27 m3/h) | 0.4 | min | m3/h | Analysis, SVD-CAL-001 D (TRL 3); timed trial in a 60 m pipe run (TRL 4) | Met as restated: about 0.42 m3/h with a right-angle drill driving each portal winch (decision 24B), a margin of 5 %; 0.22 m3/h by hand as the fallback, which is below the face rate | R3 |
| PR-004 | UR-003 | Usability | Haul force | Portal crank force under 200 N (45 lbf) with loaded sledges over 60 m | 200 | max | N | Analysis, SVD-CAL-001 C (TRL 3); force gauge during trial (TRL 4) | Met on paper: 93 N at the start in high gear, 30 N in low gear | R4 |
| PR-005 | UR-004 | Safety | Fresh air at the face | At least 1 m3/min (35 ft3/min) of fresh air delivered at the face over 60 m of duct (target, to be checked against confined-space guidance) | 1 | min | m3/min | Analysis, SVD-CAL-001 F (TRL 3); anemometer at duct outlet (TRL 4) | Met on paper: about 15 m3/min at the face | R5 |
| PR-006 | UR-006 | Performance | Casualty evacuation | A 100 kg (220 lb) manikin moved 60 m through the pipe in under 5 minutes | 5 | max | min | Analysis, SVD-CAL-001 E (TRL 3); timed drill (TRL 4) | Met on paper: about 3.5 min with three people hauling hand over hand | R6 |
| PR-007 | UR-008 | Deployment and assembly | Rapid set-up | Kit installed and hauling within 2 hours of arriving at the portal | 2 | max | h | Analysis, SVD-CAL-001 G (TRL 3); timed deployment exercise (TRL 4) | Met on paper: about 1.6 h estimated | R7 |
| PR-008 | UR-009 | Electrical | No power in the pipe | Zero electrically powered items inside the pipe except battery lamps and signal devices | 0 | max | powered items | Design review (TRL 3) | Met by design: battery lamps, gas monitors (alarm devices) and sound-powered telephones only; the drill drive stays at the portal | R8 |
| PR-009 | UR-010 | Materials | Shift durability | 72 hours of continuous operation without failure of rope, pulleys or sledges | 72 | min | h | Analysis, SVD-CAL-001 H (TRL 3); endurance trial (TRL 4) | Managed: rope abrasion over about 250 round trips at the drill rate cannot be shown on paper; both ropes are inspected against a wear gauge every shift and a spare set is carried (decision 25A). The endurance trial decides whether a tougher rope is needed | R9 |
| PR-010 | UR-011 | Packaging and transport | Transportable | Whole kit in cases no heavier than 40 kg (88 lb) each, moveable by road and by hand to the portal | 40 | max | kg | Analysis, SVD-CAL-001 I (TRL 3); weighing and handling trial (TRL 4) | Met, thin: heaviest package 37.7 kg (the sledge bundle) | R10 |
| PR-011 | UR-012 | Safety | Overload limit | Rope tension limited to 2.5 kN (562 lbf) by a release at each end of the train or stretcher; every part sized on that limit | 2.5 | max | kN | Analysis, SVD-CAL-001 C and D6 (TRL 3); release test of the swivel pins and proof load on CalRig (TRL 4) | Met by design: rope factor 6.5 on the release load; drill clutch slips at 1.55 kN in high gear | R11 |
| PR-012 | UR-005 | Safety | Air monitoring | Oxygen, carbon monoxide, hydrogen sulphide and flammable gas monitored continuously at the face and at the portal, with alarms | 4 gases, 2 places | min | gases, places | Design review (TRL 3); bump test before each shift (TRL 4) | Met by design: two four-gas monitors in the kit | R12 |
| PR-013 | UR-013 | Cost | Affordable to hold | Parts cost of the priced bill of materials within the USD 5,000 value-engineering target (a control target, not a limit; Amish kept it on 2026-10-03, SVD-DDR-001 item 13) | 5,000 | max | USD | Priced BOM, bom/bom.csv; SVD-CAL-001 J | Over target: USD 10,804.00 in parts, USD 5,804.00 over. The two winches (USD 2,300), four-gas monitors (USD 1,100), signal line (USD 860), duct (USD 765) and blower (USD 750) are the largest lines. Proposed, awaiting Amish: hold the target, or restate it for a rescue kit | none |
| PR-014 | UR-014 | Materials | Made by a general workshop | Every made part shall be cut, rolled, drilled, bent or welded from stock steel section, bar and sheet with workshop tools; bought parts limited to catalogue items (winches, sheave, ropes, drills, blower, duct, monitors, fasteners); no casting and no machining beyond drilling and facing | Pass or fail | Pass or fail | n/a | Inspection of the BOM, the model and the build plan SVD-BLD-001 (TRL 3) | Met by design: the fidelity check lists every made part (cad/fidelity.json) | none |
| PR-015 | UR-015 | Electrical | Face and portal signals | A sound-powered telephone pair with a pull-cord bell as a mechanical backup runs between the face and the portal, with no battery in the pipe | 1 pair, 1 backup | min | sets | Design review (TRL 3), SVD-DDR-001 item 8; call test (TRL 4) | Met by design: signal line, BOM line 24 | none |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- The rescue pipe is steel of 800 mm outside diameter with a 10 mm wall (780 mm bore), as at Silkyara; the fit trial confirms the bore and the weld beads.
- Experienced hand miners or trained rescue crews will be available to use the kit.
- A blower and some power are available at the portal; nothing inside the pipe uses mains power.
- The pipe is pushed forward by other means while crews dig; SleeveDrift does not push pipe.
- The pipe is horizontal or on a slight grade, so the train does not run away when a winch is eased.
- Targets are proposals for review with a co-design partner (SVD-PRB-001). PR-013 to PR-015 are new at the kit 1.9.1 upgrade and are proposed, awaiting Amish, with the rest.
