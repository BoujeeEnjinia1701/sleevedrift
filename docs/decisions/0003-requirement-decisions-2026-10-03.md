---
doc_id: SVD-DDR-003
title: SleeveDrift requirement decisions of 2026-10-03
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
  change: "Amish's decisions 24B, 25A and 26C of 2026-10-03 on R3, R9 and the R1 stretch, and how they were carried out"
---

# 0003: Requirement decisions of 2026-10-03 (R3, R9, R1 stretch)

- **Date:** 2026-10-03
- **Status:** accepted

## Context

The TRL 3 calculations (SVD-CAL-001 v0.1) left three requirements not met or at risk: R3 (spoil haulage, 0.22 against 1 m³/h by hand), R9 (rope abrasion over 72 hours cannot be shown on paper) and the 600 mm stretch of R1 (not designed). Each was put to Amish with options and a recommendation in `docs/REVIEW.md` and the register SVD-DEC-001 (portfolio items 24, 25 and 26).

Amish Chadha (owner), 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed."

> **Safety:** Decision 24B puts powered drills on the portal winches. The drill clutch, the trigger with no lock-on, the drum guards and the breakaway swivels are kept as conditions of the decision; nothing powered goes into the pipe.

## Options considered

The options are set out in full in `docs/REVIEW.md` (TRL 3, "Decisions for Amish") and SVD-CAL-001 v0.1, sections A, D and H.

- **24 (R3):** A, hand cranking only (0.22 m³/h); **B, a right-angle drill drive on each portal winch (about 0.42 m³/h, about USD 700)**; C, B plus six sledges and faster handling (about 0.71 m³/h, about USD 940).
- **25 (R9):** **A, inspect both ropes every shift and carry a spare set (USD 237, 15 kg)**; B, an abrasion-resistant rope; C, rope rollers every 10 m.
- **26 (R1 stretch):** A, drop the 600 mm stretch; B, design a 600 mm variant now; **C, keep it as a stretch until the co-design partner answers**.

## Decision

*Table 1. Decisions and how they were carried out.*

| # | Decision | What changed | New result |
| --- | --- | --- | --- |
| 24B | A cordless right-angle drill on a winch bit in each winch socket drives the haul at the portal; hand cranking stays as the fallback; nothing extra inside the pipe; drill safety kept (guarding, dead-man trigger, breakaway swivels) | Model: drills, winch bits and drum guards on the station (`cad/src/model.py`, with new checks); BOM lines 30 to 33 (USD 700); SVD-DWG-002 Rev P3; making sketch SVD-DWG-112 (drum guard); joint 9; build plan steps 2, 3 and 15; drill rules in the safety stops | R3: 0.42 m³/h against 1 m³/h, **still not met**, but faster than the hand-dug face (about 0.27 m³/h). Clutch at 35 N m slips at 1.55 kN in high gear, below the 2.5 kN swivel release; drill used in high gear only. About 111 Wh an hour of hauling. R8 still met |
| 25A | Inspect both ropes each shift and carry a spare set | BOM line 34 (spare ropes and wear gauge, USD 236.50, 15 kg); shift-change safety stop rewritten; ropes package now 29.9 kg | R9: managed by inspection and spares; at the drill rate 72 h is about 250 round trips (60 km of drag per metre of rope); the TRL 4 endurance trial decides whether a tougher rope is needed |
| 26C | The 600 mm variant waits for the co-design partner | No design change; R1 status and SVD-CAL-001, A5 updated | R1: met for 800 mm; 600 mm stretch open until the partner answers |

Kit after the decisions: about 328 kg in 13 packages, heaviest 34.8 kg (R10 met). Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 10,804.00 (USD 5,804.00 over the target). `budget_usd` is unchanged.

## Consequences

- R3 remains below its 1 m³/h target with the decided drive. Whether to restate R3 is a new question for Amish (register, Open decisions; `docs/REVIEW.md`).
- The drills need portal power for charging and six batteries for continuous hauling; the trial site list in the build plan now includes it.
- Set-up stays about 1.6 h (93 min): fitting the drills adds 5 min, and the shuttle trips during set-up are faster with them.
- The rope swap time (about 20 min) and the drill clutch slip are TRL 4 first checks.
