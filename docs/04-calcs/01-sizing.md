---
doc_id: SVD-CAL-001
title: SleeveDrift sizing calculations
project: SleeveDrift
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First issue for TRL 3 on the constructable design (SVD-DDR-002); fit, hood, haul forces, overload limit, output, casualty, air, set-up, durability, packages, cost
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Amish's decisions 24B, 25A and 26C of 2026-10-03 (SVD-DDR-003): portal drill drive (output, torque, clutch, energy), rope inspection and spare set (durability), 600 mm stretch held for the co-design partner; set-up, packages and cost recomputed"
---

# SleeveDrift sizing calculations

On paper SleeveDrift does what it was drawn for, with output as restated for R3 on 2026-10-04. Every piece passes along a 780 mm pipe bore, the heaviest weighs 31 kg, the hood carries 5 kN at 5.5 MPa with under 0.1 mm of deflection, the portal crew turns the winch with 92 N at most when cranking by hand, the rope keeps a factor of 6.5 on the 2.5 kN breakaway load, the blower delivers about 15 m³/min at the face, a casualty comes out in about 3.5 minutes, and the kit is set up in about 1.6 hours. Amish decided on 2026-10-03 (decision 24B) to drive each winch with a right-angle electric drill at the portal: the train then moves at 14.5 m/min, a round trip takes 17.3 minutes and the haul carries about 0.42 m³ an hour, nearly twice the hand rate of 0.22 m³ and faster than the hand-dug face at Silkyara (about 0.27 m³ an hour), which meets R3 as restated by Amish on 2026-10-04 (decision 4A, SVD-DDR-004: at least 0.4 m³ an hour and faster than the face produces it); the original 1 m³ target was a scaffold figure, not a face rate. Once the haul is powered, loading and tipping take most of the cycle. Rope wear over a 72-hour shift (R9) cannot be settled on paper; it is managed by inspecting both ropes every shift and carrying a spare set (decision 25A). Every number below is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C3], is the line of the script's output that carries it.

> **Safety:** SleeveDrift is rescue equipment for people working inside a pipe under collapse debris, with ropes under tension and a hand-wound haul. These are first-principles estimates for a paper proof of concept; they do not show that any part is safe. The hood, sheave bracket, ring fixing and anchors must be load tested before use (SVD-BLD-001, section 6), the breakaway swivels must never be bypassed, and nobody is on a rope line or near the sheave while the train moves. See SVD-PRC-001, Safety.

## Scope and method

The note checks every requirement in SVD-REQ-001 v0.4 against the design in SVD-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and `masses()`, so the ring, sledges and trestles used here are the ones in the STEP files and drawings SVD-DWG-001 and 002. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes `docs/04-calcs/results.csv`.

The design case is a 60 m rescue pipe of 800 mm outside diameter and 10 mm wall, horizontal, with the portal haul station 5.5 m behind the pipe mouth and the train working at the face.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Pipe | 800 x 10 mm steel, 780 mm bore, 60 m, horizontal | Silkyara escape pipe; confirm at the fit trial |
| Spoil | Loose density 1.7 kg/L (range 1.5 to 1.9); bulking 1.3 | Handbook ranges for broken rock, soil and rubble |
| Sliding | UHMW-PE runners on a gritty steel floor: friction 0.30 sliding, 0.40 starting; rope on the floor 0.50 | Conservative for dry grit; confirm in trial |
| Winches | Two-speed self-tailing, power ratios 13 and 40 with a 250 mm handle, efficiency 0.85 | Typical size 40 class; confirm with the winch bought |
| People | One person cranking sustains 60 W; handle at 60 rpm light; hand-over-hand hauling 0.4 m/s | Ergonomics ranges for shift work |
| Drill drive | 120 rpm at the winch socket in high gear; 0.60 from battery to socket; slip clutch set to 35 N m; 18 V, 5 Ah (90 Wh) batteries | Heavy-duty right-angle drill class; confirm with the drill bought |
| Crew times | Tipping a sledge 1.0 min (two people); loading 30 L/min; signals 1.0 min a cycle | Estimates; measure at TRL 4 |
| Return tension | 50 N held on the easing winch | Enough to keep the return leg from snagging |
| Steel | S355, E = 205 GPa | |
| Fixing | Crown screw preload 15 kN, side screw 10 kN, friction 0.20 at the pads and invert | M20 class 8.8 at about 60 N m; rusty or painted pipe |
| Air | 200 mm layflat, Darcy factor 0.030, minor losses 2.1 velocity heads, 6.5 % leakage over 65 m | Ventilation duct practice |

## A. Fit in the pipe (R1)

The ring rests on the pipe invert, so the 20 mm diametral clearance is all at the crown [A1]. With the jacking pads screwed back against the shell, every segment fits a 776 mm circle; the sledge is 300 mm wide and 158 mm high; the rolled stretcher is about 480 mm. The largest single piece is the crown segment: chord 658 mm, rise 190 mm, 31.0 kg [A2]. It rides in on a sledge.

With the duct on the upper +Y wall and the return rope on the floor, the largest clear circle left for a crawling person is 554 mm, against 780 mm in the empty pipe [A3]. Inside the ring the clear height is 750 mm [A4]. The 600 mm stretch of R1 has not been designed; the sizes are parameters in the model, but the crawl space in a 600 mm pipe needs its own layout. Amish decided on 2026-10-03 (decision 26C) to keep it as a stretch until the co-design partner says whether 600 mm pipes are used for rescue [A5]. R1 is met for the 800 mm pipe; the 600 mm stretch is open until then.

## B. Hood (R2)

The crown section (120 degrees of 5 mm shell plus the two 50 x 10 mm flanges that run the full length as hood ribs) has an area of 4,953 mm² and a second moment of area of 27.9 x 10⁶ mm⁴ about its own centroid [B1]. Taking all 5 kN on the crown alone, spread over the 500 mm that stands beyond the pipe mouth, as a cantilever from the mouth: M = 1,250 N m, stress 5.5 MPa against 355 MPa yield, tip deflection 0.01 mm [B2]. Across the hood the curved plate acts as an arch: 15.2 kPa gives a hoop force of 5.7 N/mm and 1.1 MPa [B3]. With the head form set 100 mm below the hood, the deflection uses a negligible part of the gap; R2 is met on paper [B4]. A concentrated rock impact is not covered by this check; the CalRig load test settles it.

The moment goes into the pipe through the bottom of the ring at the mouth and the two crown pads 175 mm inside: 3.7 kN on each crown screw, well inside the 15 kN preload [B5].

## C. Haul forces and the overload limit (R4, R11)

A train of four 29.9 L sledges carries 120 L, 203 kg of spoil, with 33 kg of sledges and links [C1]. 120 m of rope lies in the pipe at any time (the pull leg plus the tail and return legs), dragging 38 N; the back tension on the easing winch adds 53 N through the sheave [C2]. The pull is 786 N loaded, 1,018 N to start and 188 N empty [C3].

*Table 2. Handle force at winch A [C4].*

| Case | High gear (ratio 13) | Low gear (ratio 40) |
| --- | --- | --- |
| Loaded, moving | 71 N | 23 N |
| Loaded, starting | 92 N | 30 N |

R4 is met in either gear. Without a limit, one person heaving 400 N in low gear would put 13.6 kN on the rope, so a breakaway swivel at each end of the train releases at 2.5 kN (R11) [C5]. The rope (18 kN, 90 % at the splice) then has a factor of 6.5 on the release load and 21 on the working pull [C6].

At the limit the face sheave pin carries 5.0 kN, 35 mm above the base plate: 114 MPa of bending, a factor of 3.1 on S355 yield [C7]. The ring is held against that pull by friction at the pads and the invert: about 79 kN of normal force gives 15.8 kN at a friction of 0.20, a factor of 3.2 [C8].

At the portal, the rope rises 634 mm over 5.5 m to the winch drums: 6.6 degrees, inside the 5 to 10 degrees a self-tailer wants [C9]. The trestle's sling eye is 640 mm up, level with the rope, so the overturning moment at the limit is 25 N m against 119 N m from the trestle's own weight [C10].

## D. Output (R3)

By hand the loaded train moves at 3.9 m/min (60 W at the handle) and the empty train at 7.2 m/min (handle at 60 rpm) [D1]. A cycle is 15.4 min out, 4.0 min unloading, 8.3 min back in, 4.0 min loading and 1.0 min of signals: 32.7 min for 120 L, or 0.22 m³/h [D2]. Hand cranking is now the fallback.

For comparison, the Silkyara hand miners advanced about 10 m in under 24 hours through a 0.8 m bore; bulked, that is about 0.27 m³/h of loose spoil [D3]. The hand haul is slower than that face.

**Portal drill drive (decision 24B).** A heavy-duty right-angle drill on a winch bit in each winch socket turns the winch at 120 rpm in high gear: 14.5 m/min, 190 W at the rope with the train loaded. The cycle becomes 4.1 min out, 4.0 min unloading, 4.1 min back in, 4.0 min loading and 1.0 min of signals: 17.3 min for 120 L, or **0.42 m³/h** [D4]. That is nearly twice the hand rate and faster than the hand-dug face, so the face rather than the haul sets the pace; R3's 1 m³/h is still not met. Nothing is added inside the pipe, so R8 is unchanged.

The drill needs 17.8 N m at the socket to keep the loaded train moving and 23.0 N m to start it. Its slip clutch is set to 35 N m, which slips at 1.55 kN of rope pull in high gear, below the 2.5 kN release of the breakaway swivels. In low gear the same clutch would allow 4.8 kN, so the drill is used in high gear only and the swivels remain the limit [D6]. The trigger has no lock-on: the drill stops when it is let go. A guard round the rear of each winch drum keeps hands and clothing off the turning drum.

A round trip takes 58.4 kJ at the rope and about 115 kJ (32 Wh) from the battery at an assumed 0.60 drill efficiency: about 111 Wh an hour, or one 90 Wh battery every 0.8 h of hauling. Six batteries and two chargers on portal power keep the haul going [D7].

*Table 3. Output (estimates).*

| Case | What changes | Cycle | Output |
| --- | --- | --- | --- |
| Hand cranking (fallback) | Hand cranking only | 32.7 min | 0.22 m³/h [D2] |
| **As designed: portal drill drive** | A right-angle drill with a winch bit on each winch, 120 rpm at the socket: 14.5 m/min, 190 W at the rope | 17.3 min | **0.42 m³/h** [D4] |
| Not adopted (option C) | The drill drive plus six sledges, two people tipping, spoil pre-bagged at the face; pull 1,135 N | 15.3 min | 0.71 m³/h [D5] |

None of these reaches the original 1 m³/h on paper. Loading and unloading take almost half the powered cycle. Amish restated R3 on 2026-10-04 (4A) as "moves loose spoil faster than the face produces it; at least 0.4 m3/h", which the drill drive as designed meets at 0.42 m³/h.

## E. Casualty evacuation (R6)

A 100 kg manikin on a 9 kg stretcher needs 412 N to move and 519 N to start [E1]. Three people hauling hand over hand on the pull rope through winch A (the drum turns freely in the hauling direction and holds when let go) pull 173 N each at the start, at 24 m/min: 3.5 min for 60 m including a minute to clip on [E2]. Cranked in high gear at 60 rpm it would take 8.3 min, and with the drill drive 5.1 min including clipping on, so hand hauling is the method [E3]. R6 is met on paper.

## F. Air at the face (R5)

65 m of 200 mm layflat at 0.27 m³/s runs at 8.6 m/s and loses 525 Pa; the blower needs about 284 W of shaft power [F1]. After 6.5 % leakage, about 15.1 m³/min reaches the face, 5.0 m³/min a person; R5 is met with a wide margin [F2]. The pipe holds 28.7 m³ of air, changed every 1.9 min, and the return air moves back along the pipe at 0.57 m/s [F3]. The body heat of three people at 300 W warms it by 3.0 K [F4]. Gas monitoring is still required (R12); fresh air does not remove gas that seeps in through the debris.

## G. Set-up time (R7)

*Table 4. Set-up sequence on the critical path [G1].*

| Step | Minutes |
| --- | --- |
| Trestles, winches, guards, slings and bins at the portal; drills fitted and clutches set | 25 |
| Blower and first duct lengths at the portal | 10 |
| Bottom segment taken in on a sledge by a crew member, both ropes paying out | 15 |
| Bottom segment set in the mouth; tail rope reeved round the sheave | 10 |
| Crown and side segments sent in on one shuttle trip (drill) | 4 |
| Segments bolted, jacking screws tightened | 20 |
| Train made up and clipped in; first empty run in (drill) | 4 |
| Signal check and gas check before digging | 5 |

The total is 93 min, about 1.6 h, with the duct and cable hung in parallel by a second pair in about 40 min [G2]. R7 is met on paper; a timed drill verifies it.

## H. Durability (R9)

At the drill rate, 72 hours is about 250 round trips, and each metre of rope in the pipe drags about 60 km over the floor [H1]. The sledge runners slide about 30 km and lose about 3.0 mm of their 10 mm at an assumed 0.1 mm/km [H2]. Rope abrasion on gritty steel over that distance cannot be predicted on paper. Amish decided on 2026-10-03 (decision 25A) to manage it as maintenance: both ropes are inspected against a 9 mm wear gauge at every shift change, a spare set of 215 m is carried, and a worn rope is swapped in about 20 min; the drills, clutch settings and guards are checked at the same time [H3]. The sheave, pins and sledges are lightly loaded. The TRL 4 endurance trial shows whether an abrasion-resistant rope is needed.

## I. Packages (R10)

*Table 5. Packages, kg [I1].*

| Package | Mass |
| --- | --- |
| Crown segment | 31.0 |
| Side segments (2) | 33.2 |
| Bottom segment, sheave, spacer and cover | 32.1 |
| Winch trestle (each of two) | 34.8 |
| Winches (2), handles, ties | 22.0 |
| Sledges (4, nested), links, swivels | 34.8 |
| Ropes (215 m) and spare set (215 m) | 29.9 |
| Drill drive: two drills, two bits, two spare batteries, charger, two drum guards | 9.5 |
| Blower | 20.0 |
| Duct (65 m) | 26.0 |
| Stretcher, spreader, monitors, phones, lamps | 29.1 |
| Tools, spigot, jacks, bolts, hangers | 26.0 |

The kit is about 328 kg in 13 packages; the heaviest are a trestle and the sledge bundle at 34.8 kg, so R10 is met [I2].

## J. Cost

Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 10,804.00 (USD 5,804.00 over the target) [J1]. The drill drive adds USD 700 (two drill kits USD 500, two winch bits USD 90, two spare batteries USD 80, two drum guards USD 30) and the spare rope set USD 236.50. The largest lines are the two self-tailing winches (USD 2,300), the four-gas monitors (USD 1,100), the signal line (USD 860), the duct (USD 765) and the blower (USD 750) [J2].

## Results

*Table 6. Results against the requirements (`docs/04-calcs/results.csv`).*

| ID | Result | Status |
| --- | --- | --- |
| R1 | Every piece passes a 776 mm circle in a 780 mm bore; 600 mm variant waits for the co-design partner | Met for 800 mm; 600 mm stretch open (decision 26C) |
| R2 | 5.5 MPa, 0.01 mm at 5 kN | Met on paper |
| R3 | 0.42 m³/h with the portal drill drive (0.22 m³/h by hand) | Met as restated (at least 0.4 m³/h) |
| R4 | 92 N starting in high gear | Met on paper |
| R5 | 15.1 m³/min at the face | Met on paper |
| R6 | 3.5 min by hand hauling | Met on paper |
| R7 | 1.6 h estimated | Met on paper (estimate) |
| R8 | Battery lamps, gas monitors and sound-powered telephones only | Met by design |
| R9 | About 250 round trips; ropes inspected every shift, spare set carried | Managed by inspection and spares (decision 25A); endurance trial at TRL 4 |
| R10 | Heaviest package 34.8 kg | Met |
| R11 | Release at 2.5 kN; rope factor 6.5 | Met by design |
| R12 | Two four-gas monitors in the kit | Met by design |
