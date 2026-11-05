---
doc_id: SVD-DEC-001
title: SleeveDrift design decisions register
project: SleeveDrift
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-11-02'
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
  change: "Amish decided the three open items as recommended (24B, 25A, 26C; SVD-DDR-003); one new question on restating R3 proposed"
- version: "0.3"
  date: '2026-10-04'
  author: Amish Chadha
  change: "Open decision 1 (R3 target) decided by Amish (round-3 decision 4A, SVD-DDR-004) and moved to Decisions made; no open decisions"
- version: "0.4"
  date: '2026-11-02'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: five open decisions proposed (concept A or B, cost target, jacking screw length, casualty rope load, PR-005 target); D1 (option C blower) recorded as made under the standing instruction of 2026-10-23; D2 lists the CAD detailing choices for review"
---

# SleeveDrift design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several decisions below set SleeveDrift's safety case for people working inside a rescue pipe (overload limit, gas monitoring, air, ring fixing, casualty evacuation). Each took the conservative option; the evidence that would relax it is in SVD-DDR-001, Table 1.

## Open decisions

*Proposed, awaiting Amish. Nothing below is decided.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Which concept to carry forward | A: rope shuttle of sledges (current design, score 175 of 195). B: rail tramway (164). C: pneumatic extraction (148) | Both A and B go to Amish with no pick, because they are within 10 % (6.3 %); A stays the baseline until decided. C is not recommended | Everything if B is chosen: PR-003, PR-004 and PR-007 change, and the model, BOM and build plan go to a new TRL 3 pass | SVD-OPT-001, SVD-DDR-005 |
| 2 | Cost target for PR-013 (USD 5,000 value-engineering target; parts cost USD 10,804.00, USD 5,804.00 over) | A: hold the target and value-engineer. B: restate the target for a rescue kit. C: treat the winches, monitors, telephones, duct and blower as borrowed kit for trials | Option A for the repo (the target is a control target and the registered cost is the priced BOM), with the savings under Value engineering; `budget_usd` is not raised. Note from the independent review: the BOM carries USD 550 for each four-gas monitor, while the quote found for a comparable unit is GBP 776.52 (about USD 1,000) each, so the BOM is probably low; it is not repriced here | PR-013 status; `project.yaml` `budget_usd` stays 5,000 | SVD-PRS-001 PR-013, section Value engineering below |
| 3 | Jacking screw length and swivel pad size: the BOM (line 5) says M20 x 90 and a 50 x 7 mm pad; the kit 1.9 model draws M20 x 60 and a 50 x 8 mm pad | A: keep the BOM and lengthen the model screw at the next CAD pass. B: shorten the BOM to match the model | Option A: the BOM is the purchase specification and the build plan says M20 x 90; the model is the part to correct. No requirement or mass figure changes | BOM line 5, `cad/src/model.py` face end | docs/REVIEW.md, session 2026-10-24 |
| 4 | Casualty rope load: the pull rope has a factor of 6.5 on the 2.5 kN release, not the 15:1 of life-safety rope practice (STM S17, found by the independent review) | A: keep the 2.5 kN release for the stretcher and state the factor of 6.5. B: fit a stretcher-only breakaway at 1.0 kN, a factor of 16 on the rope (the starting pull is 519 N). C: a dedicated 42 kN rescue rope | Option B: lowest cost, and 1.0 kN is 1.9 times the starting pull; it changes the overload limit Amish decided (SVD-DDR-001 item 5), so it is not implemented | PR-011; swivel pin for the stretcher; BLD safety stops | SVD-STM-001 S17 |
| 5 | PR-005 target (at least 1 m3/min at the face): three people digging need about 1.0 to 1.4 m3/min just to hold CO2 below 5,000 ppm, so the target as written leaves no margin (STM S13) | A: keep 1 m3/min. B: restate per person, for example at least 3 m3/min a person (the design delivers 15 m3/min, about 5 a person) | Option B; no design change | PR-005 wording only | SVD-STM-001 S13, independent review |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Pipe bore, wall and internal weld beads of the pipe used for trials | The ring is 760 mm OD with 20 mm clearance; a bead or a smaller bore changes the fit | SVD-CAL-001, A; R1 |
| 2 | Winch power ratios, base bolt pattern and line rating | Handle forces assume ratios of about 13 and 40; the trestle top plates are drilled to the base | SVD-CAL-001, C; BOM line 17 |
| 3 | Release load of the breakaway swivel pins bought | Sets the 2.5 kN limit that every part is sized on | SVD-CAL-001, C; R11 |
| 4 | Sheave bore, bush and rating | The pin is 25 mm; the sheave must be rated at least 1,000 kg | BOM line 6 |
| 5 | Friction of the jacking pads on the actual pipe surface | The ring's hold against the sheave pull assumes 0.20 | SVD-CAL-001, C8 |
| 6 | Rope breaking strength and splice efficiency | The factor of 6.5 assumes 18 kN and 90 % at the splice | SVD-CAL-001, C6 |
| 9 | Drill torque, clutch range and no-load speed in high gear; winch bit to fit the socket | The drive assumes 120 rpm at the socket and a clutch that can be set to about 35 N m | SVD-CAL-001, D4 and D6; BOM lines 30 and 31 |
| 7 | Blower curve at 525 Pa | The air figures assume 0.27 m³/s at the blower | SVD-CAL-001, F; R5 |
| 8 | Holding force of the magnet hangers on painted or rusty pipe | They carry the duct and the cable | BOM line 22 |

## Value engineering

Value-engineering target: USD 5,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 10,804.00 (USD 5,804.00 over the target), including the drill drive (USD 700) and the spare rope set (USD 236.50) decided on 2026-10-03. Main cost drivers and savings worth trying:

- The two self-tailing winches (USD 2,300) are the largest line; reconditioned winches of the same size are often about half the new price.
- The four-gas monitors (USD 1,100), the blower and duct (USD 1,515) and the telephones (USD 860) are kit that rescue services usually already hold; borrowing them for trials removes about USD 3,500 from the prototype cost without changing the design.
- The made steel (ring, trestles, sledges) is under USD 1,500; plate rolling is the main cost there.
- The drill kits (USD 500) can be bought in the battery platform a rescue service already uses, so its batteries and chargers are shared.
- Savings not worth taking: the breakaway swivels, rope and slings carry the safety case and stay at rated grades.

## Decisions made

Pre-approval quotes: Q1, Amish 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Q2, Amish 2026-10-03: "Proceed with the remaining 15 scaffolds" (under the same pre-approval). Q3, Amish 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed."

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
| 2026-10-03 | R3: a right-angle electric drill drive on each portal winch (about 0.42 m³/h, about USD 700); nothing extra inside the pipe; drill safety kept: guarding, dead-man trigger, breakaway swivels (item 24, option B) | Amish, Q3 | SVD-DDR-003 |
| 2026-10-03 | R9: inspect both ropes each shift and carry a spare set (item 25, option A) | Amish, Q3 | SVD-DDR-003 |
| 2026-10-03 | R1: the 600 mm variant waits for the co-design partner (item 26, option C) | Amish, Q3 | SVD-DDR-003 |
| 2026-10-04 | R3 (4A): restated as "moves loose spoil faster than the face produces it; at least 0.4 m3/h" (hand-dug faces about 0.27 m3/h); met at 0.42 m3/h | Amish: "For round 3, I agree with all your proposed recommendations" | SVD-DDR-004 |
| 2026-11-02 | D1. Option C blower: the 2.2 kW fan of the first draft cannot carry 50 mm rubble (it needs about 2.4 kW for 6 mm fines and 17 kW for 50 mm lumps at 1.5 times the terminal velocity); fixed with a 7.5 kW three-phase high-pressure blower on a portal generator and a 12 mm limit on the lumps the crew feeds to the nozzle (the first fix, a 7.5 kW side-channel blower for 50 mm rubble, was refuted by the independent review: it needs about 1,700 m3/h at 7.8 kPa). Keeps the working principle, so it does not go to Amish; option C itself stays proposed, not chosen | Decided under Amish's standing instruction of 2026-10-23 (fix rule) | SVD-STM-001 Table 2, SVD-OPT-001 |
| 2026-11-02 | D2. CAD detailing choices for the D3 models, none changing a dimension, mass or cost figure: tie collars welded top and bottom only so the bolts and washers stay clear; winch sling pin and eye plate aligned to the hole centre; drill battery hung below the body; option B wagons with an M16 axle and a 19 mm spacer tube; option B rails bolted with M6 into tapped sleepers; option C hose clamps as split bands with a tangent bolt; the contacts of the duct cuffs, the blower spigot and the cyclone inlet box listed in `ALLOWED_CONTACTS` | Implementation detail within the upgrade brief ("keep the design and the numbers"); not a decision under the standing instruction, which covers failed STEM rows; listed for Amish's review | docs/REVIEW.md, session 2026-10-24 |
