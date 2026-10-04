---
doc_id: SVD-DEC-001
title: SleeveDrift design decisions register
project: SleeveDrift
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; design decisions made under Amish's pre-approvals of 2026-10-03; three requirement decisions proposed for Amish
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Round 2. Amish decided R3 (1B), R9 (2A) and the R1 stretch (3C) as recommended (SVD-DDR-003); two new questions raised while carrying them out, proposed, awaiting Amish
---

# SleeveDrift design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several decisions below set SleeveDrift's safety case for people working inside a rescue pipe (overload limit, gas monitoring, air, ring fixing, casualty evacuation). Each took the conservative option; the evidence that would relax it is in SVD-DDR-001, Table 1.

## Open decisions

The three round 1 requirement decisions (R3, R9, R1 stretch) were decided by Amish on 2026-10-03 and are listed under Decisions made (SVD-DDR-003). The questions below were raised while carrying them out (full statement in `docs/REVIEW.md`, session 2026-10-03, round 2). Each is **Proposed, awaiting Amish**.

| # | To decide | Options (effect on the requirement, cost, mass) | Recommendation | What it affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 4 | Drill gear and clutch rule (R11 with the drill drive): a clutch set between about 28 and 45 N m slips before the 2.5 kN swivel releases in high gear only; in low gear the release is reached at 18 N m | A. Drill in high gear only, clutch set at about 35 N m, the rule written on each trestle: R3 stays 0.42 m³/h; no cost. B. Clutch set at about 15 N m so it slips first in either gear: the drill cannot start the loaded train in high gear (23 N m) and hauls in low gear at about a third of the speed. C. No rule; the swivel stays the only limit, as for hand cranking | **A**: the swivel is the designed limit in both gears; the rule keeps the clutch as a second, earlier limit in the gear the drill is used in | A label on each trestle; the build plan already says high gear | SVD-CAL-001, D6; REVIEW round 2 |
| 5 | R9 wording: option 2A meets R9 "in practice if a swap counts as maintenance", but R9 reads "72 hours of continuous operation without failure of rope, pulleys or sledges" | A. Restate R9 as "72 hours of continuous operation without failure of rope, pulleys or sledges, with ropes inspected at every shift change and a worn rope swapped as planned maintenance": R9 met in practice on paper, shown in the endurance trial. B. Keep the wording: R9 at risk until the endurance trial | **A**: it states what Amish chose in 2A, and the endurance trial still tests it | None | SVD-CAL-001, H; REVIEW round 2 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Pipe bore, wall and internal weld beads of the pipe used for trials | The ring is 760 mm OD with 20 mm clearance; a bead or a smaller bore changes the fit | SVD-CAL-001, A; R1 |
| 2 | Winch power ratios, base bolt pattern and line rating | Handle forces assume ratios of about 13 and 40; the trestle top plates are drilled to the base | SVD-CAL-001, C; BOM line 17 |
| 3 | Release load of the breakaway swivel pins bought | Sets the 2.5 kN limit that every part is sized on | SVD-CAL-001, C; R11 |
| 4 | Sheave bore, bush and rating | The pin is 25 mm; the sheave must be rated at least 1,000 kg | BOM line 6 |
| 5 | Friction of the jacking pads on the actual pipe surface | The ring's hold against the sheave pull assumes 0.20 | SVD-CAL-001, C8 |
| 6 | Rope breaking strength and splice efficiency | The factor of 6.5 assumes 18 kN and 90 % at the splice | SVD-CAL-001, C6 |
| 7 | Blower curve at 525 Pa | The air figures assume 0.27 m³/s at the blower | SVD-CAL-001, F; R5 |
| 8 | Holding force of the magnet hangers on painted or rusty pipe | They carry the duct and the cable | BOM line 22 |

## Value engineering

Value-engineering target: USD 5,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 10,804.00 (USD 5,804.00 over the target), USD 936.50 more than before the round 2 decisions for the two portal drill drives and the spare rope set (SVD-DDR-003). Main cost drivers and savings worth trying:

- The two self-tailing winches (USD 2,300) are the largest line; reconditioned winches of the same size are often about half the new price.
- The four-gas monitors (USD 1,100), the blower and duct (USD 1,515) and the telephones (USD 860) are kit that rescue services usually already hold; borrowing them for trials removes about USD 3,500 from the prototype cost without changing the design.
- The made steel (ring, trestles, sledges) is under USD 1,500; plate rolling is the main cost there.
- Savings not worth taking: the breakaway swivels, rope and slings carry the safety case and stay at rated grades.

## Decisions made

Pre-approval and decision quotes: Q3, Amish 2026-10-03: "i approve all of the 47 recommendations provided by you. Execute them." Q1, Amish 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Q2, Amish 2026-10-03: "Proceed with the remaining 15 scaffolds" (under the same pre-approval).

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | Design-case pipe 800 x 10 mm, 780 mm bore | Amish, Q1 and Q2 | SVD-DDR-001, item 1 |
| 2026-10-03 | Ring held by jacking screws with swivel pads; nothing drilled or welded to the pipe | Amish, Q1 and Q2 | SVD-DDR-001, item 2 |
| 2026-10-03 | Shuttle train between a pull rope and a tail rope, in place of a circulating loop | Amish, Q1 and Q2 | SVD-DDR-001, item 3 |
| 2026-10-03 | Two two-speed self-tailing winches at the portal; SiltHaul capstan not used | Amish, Q1 and Q2 | SVD-DDR-001, items 4, 12 |
| 2026-10-03 | Breakaway swivels at 2.5 kN at both ends of the train; requirement R11 added | Amish, Q1 and Q2 | SVD-DDR-001, item 5 |
| 2026-10-03 | Two four-gas monitors in the kit; requirement R12 added | Amish, Q1 and Q2 | SVD-DDR-001, item 6 |
| 2026-10-03 | Forcing ventilation through 200 mm layflat, about 15 m³/min at the face | Amish, Q1 and Q2 | SVD-DDR-001, item 7 |
| 2026-10-03 | Sound-powered telephones with a pull-cord bell | Amish, Q1 and Q2 | SVD-DDR-001, item 8 |
| 2026-10-03 | Bought roll-up stretcher with a made spreader bar; casualty hauled hand over hand through winch A | Amish, Q1 and Q2 | SVD-DDR-001, items 9, 10 |
| 2026-10-03 | First co-design candidate to approach: India's National Disaster Response Force with the Jhansi hand miners (not agreed) | Amish, Q1 and Q2 | SVD-DDR-001, item 11 |
| 2026-10-03 | CalRig as the first candidate rig for the hood test and proof loads; HatchSide as the first reference for air and gas rules | Amish, Q1 and Q2 | SVD-DDR-001, item 12 |
| 2026-10-03 | `budget_usd` kept at 5,000 as a value-engineering target | Amish, Q1 ("I also accept any cost overruns or variations from the assumed scope cost.") | SVD-DDR-001, item 13 |
| 2026-10-03 | Design for construction: the twelve changes of SVD-DDR-002 | Amish, Q1 and Q2 | SVD-DDR-002 |
| 2026-10-03 | Appearance model additions for renders: pipe window and platform cropped, a 1.75 m mannequin beside the pipe | Amish, Q1 and Q2 | docs/REVIEW.md, TRL 3 |
| 2026-10-03 | R3 spoil haulage (open decision 1): option B, a portal drill drive on each winch socket with hand cranking as the fallback; about 0.42 m³/h, R3 still not met | Amish, Q3 ("i approve all of the 47 recommendations provided by you. Execute them.") | SVD-DDR-003, item 1 |
| 2026-10-03 | R9 shift durability (open decision 2): option A, ropes inspected at every shift change and a spare set carried; the TRL 4 endurance trial decides whether an abrasion-resistant rope (option B) is needed | Amish, Q3 | SVD-DDR-003, item 2 |
| 2026-10-03 | R1 600 mm stretch (open decision 3): option C, kept as a stretch until the co-design partner says whether 600 mm pipes are used for rescue | Amish, Q3 | SVD-DDR-003, item 3 |

## Change log

- 2026-10-03, v0.2: open decisions 1 to 3 decided as recommended (1B, 2A, 3C) and carried into the design (SVD-DDR-003); new questions 4 and 5 opened.
