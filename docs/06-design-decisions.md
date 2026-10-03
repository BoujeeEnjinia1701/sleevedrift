---
doc_id: SVD-DEC-001
title: SleeveDrift design decisions register
project: SleeveDrift
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; design decisions made under Amish's pre-approvals of 2026-10-03; three requirement decisions proposed for Amish
---

# SleeveDrift design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several decisions below set SleeveDrift's safety case for people working inside a rescue pipe (overload limit, gas monitoring, air, ring fixing, casualty evacuation). Each took the conservative option; the evidence that would relax it is in SVD-DDR-001, Table 1.

## Open decisions

Three requirements are not met or are at risk on paper. They are put to Amish with options and a recommendation (full statement in `docs/REVIEW.md`, TRL 3, "Decisions for Amish"). Each is **Proposed, awaiting Amish**.

| # | To decide | Options (effect on the requirement, cost, mass) | Recommendation | What it affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | R3 spoil haulage: 0.22 m³/h by hand | A. Keep hand cranking only: 0.22 m³/h, no cost, no mass. B. A right-angle drill with a winch bit on each winch at the portal: about 0.42 m³/h, about USD 700, about 7 kg. C. B plus six sledges, two people tipping and spoil pre-bagged at the face: about 0.71 m³/h, about USD 940, about 22 kg | **B**: it doubles the haul and moves it past the hand-dug face rate seen at Silkyara (about 0.27 m³/h), keeps hand cranking as the fallback and adds nothing inside the pipe | Portal station only: drill, winch bits, batteries | SVD-CAL-001, D; REVIEW TRL 3 |
| 2 | R9 shift durability: rope abrasion unknown | A. Inspect both ropes every shift against a wear gauge and carry a spare set: no change to R9 on paper but a 20 min swap if one wears, USD 237, 15 kg. B. Rope with an abrasion-resistant coated cover: likely longer life, about USD 300 more, about 3 kg more. C. Low rollers every 10 m to lift the ropes off the floor: least wear, about USD 500, about 25 kg, and parts in the crawl lane | **A**, with the TRL 4 endurance trial deciding whether B is needed | Ropes and the shift routine; nothing to make | SVD-CAL-001, H; REVIEW TRL 3 |
| 3 | R1 stretch: 600 mm pipe not designed | A. Remove the 600 mm stretch from this design: no cost, no mass. B. Design a 600 mm variant now (560 mm ring in three segments, 220 mm sledges, 150 mm duct): about USD 900 more for a second ring set, about 70 kg. C. Keep it as a stretch and decide when the co-design partner confirms whether 600 mm pipes are used for rescue: no cost now | **C**: the sizes are parameters in the model, and the partner's answer decides whether a second ring is worth making | Nothing in the first prototype | SVD-CAL-001, A; REVIEW TRL 3 |

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

Value-engineering target: USD 5,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 9,867.50 (USD 4,867.50 over the target). Main cost drivers and savings worth trying:

- The two self-tailing winches (USD 2,300) are the largest line; reconditioned winches of the same size are often about half the new price.
- The four-gas monitors (USD 1,100), the blower and duct (USD 1,515) and the telephones (USD 860) are kit that rescue services usually already hold; borrowing them for trials removes about USD 3,500 from the prototype cost without changing the design.
- The made steel (ring, trestles, sledges) is under USD 1,500; plate rolling is the main cost there.
- Savings not worth taking: the breakaway swivels, rope and slings carry the safety case and stay at rated grades.

## Decisions made

Pre-approval quotes: Q1, Amish 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Q2, Amish 2026-10-03: "Proceed with the remaining 15 scaffolds" (under the same pre-approval).

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
