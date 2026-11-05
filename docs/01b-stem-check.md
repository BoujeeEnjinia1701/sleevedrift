---
doc_id: SVD-STM-001
title: SleeveDrift STEM check
project: SleeveDrift
doc_type: STEM check
version: "0.1"
status: Draft
date: 2026-11-02
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-02
    author: Amish Chadha
    change: First issue at the kit 1.9.1 upgrade; 22 claims for options A, B and C; option C blower failure fixed under the standing instruction of 2026-10-23 (SVD-DEC-001 D1); independent review recorded and its findings applied; S17 fails with a fix proposed to Amish
---

# SleeveDrift STEM check

Verdict: of 22 claims, 10 sit within known science, 11 are plausible and need a measurement or a named part (S1b, S7, S8, S9, S10, S11, S12, S15, S16, O5, O4), and 1 fails with a fix proposed to Amish (S17: the casualty rope has a factor of 6.5 on the 2.5 kN release, not 15). Two other claims failed and were fixed in the same session under the standing instruction of 2026-10-23: the first draft of option C (a 2.2 kW fan for 50 mm rubble) and, after the independent review, its first fix (a 7.5 kW side-channel blower). The method and rules are in STANDARDS section 20. The calculations are in `docs/04-calcs/stem_check.py`, which imports the sizing script behind SVD-CAL-001; results are in `docs/04-calcs/stem_results.csv`.

> **Safety:** SleeveDrift describes equipment for use inside a rescue pipe under collapse debris. A claim that sits within known science on paper does not make the kit safe; every figure here is a paper screen to be tested at TRL 4 or later.

## Claims checked

Table 1. Claims, governing science and verdicts. Rows S1 to S17 (and S1b) are the claims of option A (the rope shuttle of sledges, the current design); O1, O2, O4 and O5 screen the working principles of option B (rail tramway) and option C (pneumatic extraction) from SVD-OPT-001.

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | The hood's crown carries 5 kN spread over its 500 mm cantilever below the 355 MPa yield of S355 with a factor of 1.5 | Physics | Strength of materials | Cantilever bending, sigma = M c / I; S355 yield 355 MPa (EN 10025-2, minimum for t up to 16 mm) | 5.46 MPa <= 236.7 MPa | Within known science | SVD-CAL-001 B2 |
| S2 | The hood tip deflects less than 0.1 mm at 5 kN, so no contact with a head form | Physics | Strength of materials | Cantilever with uniform load, d = w L^4 / (8 E I); E = 205 GPa | 0.0136 mm <= 0.1 mm | Within known science | SVD-CAL-001 B2, B4 |
| S1b | The hood tip, taken as a flat strip across its 658 mm chord with no arch action, stays below yield with a factor of 1.5 | Physics | Strength of materials | Simply supported strip, sigma = (p c^2 / 8) / (t^2 / 6); conservative because the rolled crown carries part of the load as an arch | 197 MPa <= 237 MPa | Plausible, to confirm at TRL 3 | SVD-CAL-001 B3 (membrane result); shell finite-element check or load test on CalRig at TRL 4 |
| S3 | Dragging the loaded train takes about 790 N at the rope (sledge friction plus rope on the floor) | Physics | Mechanics and statics | Coulomb friction: F = mu_k m g for the sledges plus the drag of the rope on the floor and the sheave back tension | claimed 794.426 N, estimate 794 N (ratio 1.00) | Within known science | SVD-CAL-001 C3 |
| S4 | A person turning the winch handle in high gear needs less than 200 N to start the loaded train | Physics | Mechanics and statics | Winch power ratio and efficiency: handle force = rope force / (power ratio x efficiency); starting friction mu_s | 93.1 N <= 200 N | Within known science | SVD-CAL-001 C4 |
| S5 | The 18 kN rope keeps a factor of 5 or more on the 2.5 kN release load after a 90 % splice (factor 5.04 at 70 %) | Physics | Strength of materials | Rope breaking strength x splice efficiency / release load; factor 5 is working-line practice, not a cited standard (to confirm with the partner) | 6.48 factor >= 5 factor | Within known science | SVD-CAL-001 C6 |
| S6 | The drill's slip clutch (35 N m) slips below the 2.5 kN swivel release in high gear | Physics | Mechanics and statics | Rope force = clutch torque x power ratio x efficiency / drum radius; in low gear the same clutch would pass 4.8 kN, so the drill is used in high gear only | 1.55 kN <= 2.5 kN | Within known science | SVD-CAL-001 D6 |
| S7 | Friction at the jacking pads holds the ring against twice the 2.5 kN release load with a factor of 1.5 | Physics | Mechanics and statics | Coulomb friction, F = mu N; the pad-to-pipe friction coefficient of 0.2 is an assumption for rusty or painted steel | 7.5 kN <= 15.8 kN | Plausible, to confirm at TRL 3 | SVD-CAL-001 C8; friction coefficient to measure on CalRig at TRL 4; the friction coefficient 0.20 and the screw preload from a torque coefficient are assumptions (independent review) |
| S8 | A 200 mm layflat duct passes 0.27 m3/s over 65 m with less than 600 Pa of loss, a pressure a 200 mm axial or mixed-flow portal blower can give | Physics | Fluid mechanics | Darcy-Weisbach, dp = (f L / D + K) rho v^2 / 2, f = 0.030, K = 2.1 (SVD-CAL-001 F1) | 525 Pa <= 600 Pa | Plausible, to confirm at TRL 3 | SVD-CAL-001 F1, F2; blower curve to confirm with the blower bought; no named blower curve yet: a 200 mm axial unit must pass 0.27 m3/s at about 570 Pa total (independent review) |
| S9 | A right-angle drill on each portal winch moves loose spoil at least 0.4 m3/h, faster than a hand-dug face makes it | Mathematics | Rates and cycle times | Cycle arithmetic: volume per trip / (out + unload + in + load + signals); drill speed from rpm and drum diameter | 0.416 m3/h >= 0.4 m3/h | Plausible, to confirm at TRL 3 | SVD-CAL-001 D4 (restated 2026-10-04, SVD-DDR-004) |
| S10 | Three people bring a 100 kg casualty out 60 m in under 5 minutes, hand over hand | Mathematics | Rates and cycle times | Time = distance / speed (0.4 m/s hand over hand, ergonomics range) plus one minute to clip on | 3.5 min <= 5 min | Plausible, to confirm at TRL 3 | SVD-CAL-001 E2; the 0.4 m/s hand-over-hand speed is an assumption; below 0.25 m/s the 5 min target fails; timed drill at TRL 4 (independent review) |
| S11 | The kit goes up in less than 2 hours | Mathematics | Rates and cycle times | Sum of the critical-path steps in SVD-CAL-001 G1; step times are estimates to measure in a drill at TRL 4 | 1.55 h <= 2 h | Plausible, to confirm at TRL 3 | SVD-CAL-001 G1, G2 |
| S12 | The heaviest package weighs less than 40 kg | Mathematics | Units and dimensional analysis | Sum of component masses from the model (cad/src/model.py masses()) | 37.7 kg <= 40 kg | Plausible, to confirm at TRL 3 | SVD-CAL-001 I2; the case itself is not counted |
| S13 | 5 m3/min of fresh air per person is far more than needed to keep CO2 below 5,000 ppm | Biology | Human physiology | Dilution: Q = n x CO2 production / (limit - inlet); heavy work 1.5 L/min CO2 per person (physiology texts, to cite), inlet 400 ppm | 0.98 m3/min <= 15.1 m3/min | Within known science | SVD-CAL-001 F2; heat and dust, not CO2, govern the airflow (SVD-CAL-001 F4) |
| S14 | Four-gas monitors measure oxygen, carbon monoxide, hydrogen sulphide and flammable gas and alarm | Chemistry | Analytical chemistry and gas sensing | Electrochemical cells for O2, CO and H2S and a catalytic bead or infrared cell for combustible gas are standard in portable four-gas monitors (Honeywell BW GasAlertMicroClip XL, listed at GBP 776.52 excluding VAT, checked 2026-11-02) | Commercial monitors exist; fitness for a collapse atmosphere (dust, humidity, calibration) to confirm with the rescue service | Within known science | SVD-REG-001 G4 |
| S15 | Rope abrasion over 72 hours of hauling does not part the pull or tail rope | Engineering and technology | Standards practice | Polyester double braid dragged over a gritty steel floor: wear per kilometre is not predictable on paper; managed by a wear gauge each shift and a spare set (SVD-DDR-003 decision 25A) | About 250 round trips at the drill rate (SVD-CAL-001 H1); an endurance trial decides whether a tougher rope is needed | Plausible, to confirm at TRL 3 | Open until TRL 4 |
| S16 | UHMW-PE runners slide on the pipe floor with a friction coefficient of 0.30 sliding and 0.40 starting | Physics | Mechanics and statics | UHMW-PE on dry steel is low friction (about 0.1 to 0.2 clean); grit, wet clay and rust raise it, so 0.30 and 0.40 are conservative assumptions | Not measurable on paper; sled test with pipe-floor debris at TRL 4 | Plausible, to confirm at TRL 3 | Open until TRL 4 |
| S17 | The pull rope can carry a casualty with the 15:1 factor that life-safety rope practice uses (NFPA 1983, FireRescue1 summary) | Physics | Strength of materials | Breaking strength x splice efficiency against 15 x the largest load the rope can see, which is the 2.5 kN swivel release, not the starting pull; NFPA 1983 (now in NFPA 2500) is a manufacturer standard and the 15:1 factor is a cited practice, not a requirement on this kit | Factor 6.5 on the 2.5 kN release (15 x 2.5 = 37.5 kN against 16.2 kN); 16.2 kN is 2.1 times the 7.8 kN that 15 x the starting pull of 519 N would need | Fails, fix proposed | Proposed, awaiting Amish (SVD-DEC-001 open decision 4): a stretcher-only breakaway at 1.0 kN would give a factor of 16 on the rope; it changes the overload limit Amish decided, so it is not implemented |
| O1 | Option B: a 40 x 40 x 4 mm aluminium T rail on sleepers 1 m apart carries a loaded wagon wheel below 6061-T6 yield with a factor of 3 | Physics | Strength of materials | Simply supported beam, M = P L / 4; sigma = M / Z; 6061-T6 yield 240 MPa (minimum, to confirm for the extrusion bought) | 19.5 MPa <= 80 MPa | Within known science | SVD-OPT-001 Table 1; smallest section modulus and a dynamic factor of 2 at rail joints (independent review) |
| O2 | Option B: rolling the train on rails (rolling resistance 0.02) cuts the pull to less than half of the sliding train | Physics | Mechanics and statics | F = c_rr m g plus the same rope drag and back tension; c_rr = 0.02 for polymer wheels on aluminium rail (estimate, to confirm) | 162 N <= 397 N | Within known science | SVD-OPT-001 Table 1 |
| O5 | Option B: cranked by hand, the rail train keeps ahead of the Silkyara face rate | Mathematics | Rates and cycle times | Cycle arithmetic with the handle at its 60 rpm limit both ways (7.2 m/min); option A by hand makes 0.22 m3/h | 0.281 m3/h >= 0.272 m3/h | Plausible, to confirm at TRL 3 | SVD-OPT-001 Table 1 |
| O4 | Option C, after the fix: a 7.5 kW three-phase high-pressure blower on a portal generator conveys lumps of up to 12 mm through 70 m of 150 mm hose | Physics | Fluid mechanics | Conveying air at 1.5 times the terminal velocity v_t = sqrt(4 g d (rho_s - rho_a) / (3 C_d rho_a)), C_d = 1 (v_t = 18 m/s for 12 mm), solids loading doubles the air power; air power = Q dp, 60 % efficient. First draft: the 2.2 kW fan needed 2.5 kW for 6 mm fines and a lump of 50 mm needs 59 kW, so the first draft failed; the fix keeps suction extraction, limits the lump to 12 mm (the crew feeds the nozzle by hand) and sizes the blower on the pressure and flow the hose needs (SVD-DEC-001 D1) | 7 kW <= 7.5 kW | Plausible, to confirm at TRL 3 | SVD-DEC-001 D1; a named blower curve passing about 1759 m3/h at 4.3 kPa is to assess |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails**.

## Fixes made under the standing instruction

*Table 2. Failed claims and their fixes. Standing instruction of 2026-10-23: when a row fails, implement the best fix in the same session, record it as decided under that instruction, and rerun the check; a fix that changes the principle, pitch or scope goes to Amish.*

| Row | What failed | Fix | Changes the principle, pitch or scope? | Recorded in |
| --- | --- | --- | --- | --- |
| O4 | The first draft of option C: a 2.2 kW fan carrying 50 mm rubble through 70 m of 150 mm hose needs about 2.4 kW for 6 mm fines and 17 kW for 50 mm lumps | A 7.5 kW three-phase high-pressure blower on a portal generator and a 12 mm limit on the lump size; the first fix (a 7.5 kW side-channel blower for 50 mm rubble) was refuted by the independent review | No: still suction extraction in a hose; lumps above 12 mm are broken by hand at the nozzle, and the cost and portal power go up (SVD-OPT-001) | SVD-DEC-001 D1 |
| S17 | The casualty rope has a factor of 6.5 on the 2.5 kN release, against the 15:1 of life-safety rope practice | A stretcher-only breakaway at 1.0 kN would give a factor of 16 | Yes: it changes the 2.5 kN overload limit Amish decided; not implemented | SVD-DEC-001 open decision 4 (Proposed, awaiting Amish) |

Option A has one failed row (S17), and its fix goes to Amish, so the design is unchanged. The calculation script was corrected: the kit mass now counts the second trestle (370 kg), the rope travel in H1 is 30 km, and the R3 row was corrected: the R3 result row in `sizing.py` still compared the haul with the scaffold 1 m3/h and printed "not met"; it now compares with the restated 0.4 m3/h of decision 4A (SVD-DDR-004), as the requirements already did.

## Fields not relevant

- Earth science: the soil and debris around the pipe are outside the kit; the kit does not move the pipe or the ground.
- Medicine: the stretcher moves a casualty; SleeveDrift makes no clinical claim and gives no treatment.
- Electronics and software: no firmware, radio or battery in the pipe; the only electrical items in the pipe are lamps and monitors with their own alarms.
- Biology beyond human physiology: no living material (S13 covers breathing air only).

## Concept options

- **A, rope shuttle of sledges (current design):** S1 to S17 and S1b. S17 fails with a fix proposed to Amish; S1b, S7 to S12, S15 and S16 are plausible and need a measurement or a trial.
- **B, rail tramway:** O1 and O2 within known science; O5 plausible (by hand it keeps ahead of the Silkyara face rate by a thin margin, about 0.28 against 0.27 m3/h, and fails if the face makes 0.33 m3/h).
- **C, pneumatic extraction:** O4 plausible after the fix (7.5 kW blower, 12 mm lumps); the first draft failed.

No option is dropped by the STEM check.

## Independent review

A second agent (Claude Opus 5.5, run headless with no access to this session or the author's reasoning) was given only this STEM check, `stem_check.py`, the calculation note SVD-CAL-001, the product requirements SVD-PRS-001 and `sizing.py`, and was asked to try to refute every "Within known science" verdict by recomputing it. It reread the rows once. Its recomputed values agreed with the script on S3, S4, S6, S9, S11 and O2, and it refuted two verdicts and weakened ten. Every finding was dealt with as follows; the table is the first run, the Verdict column of Table 1 is after the changes.

*Table 3. Independent review: findings and what changed.*

| # | Finding (reviewer's number) | Disposition |
| --- | --- | --- |
| 1 | O4 refuted: a 7.5 kW side-channel blower cannot give the flow (about 1,700 m3/h at 7.8 kPa for 50 mm lumps at 0.7 of the terminal velocity; 17.6 kW at the terminal velocity) | Accepted. The 0.7 rule was dropped for 1.5 times the terminal velocity; the first draft's 2.2 kW fan and the side-channel fix both fail. Fix under the standing instruction (SVD-DEC-001 D1): a 7.5 kW three-phase high-pressure blower and a 12 mm limit on the lump size (about 7 kW at 27.6 m/s). O3 was merged into O4. O4 is now Plausible: a named blower curve is to assess. The model part was renamed; the 12 mm grid at the nozzle is not modelled |
| 2 | S17 refuted: the 15:1 factor applies to the largest load the rope can see (2.5 kN release), not the starting pull | Accepted. The row now reads "Fails, fix proposed": factor 6.5, not 15. The fix (a stretcher-only 1.0 kN breakaway) changes the overload limit Amish decided, so it goes to Amish (SVD-DEC-001 open decision 4) and is not implemented. The 18 kN rope is a working line, not a rescue rope |
| 3 | S1 and S2 check the wrong mode for the free tip of the hood | Partly accepted. Row S1b added: the tip as a flat strip across its chord gives 197 MPa against 237 MPa allowable (Plausible, conservative because the arch carries part of the load); S2 at the strip is about 17 mm, inside the 100 mm head gap. No stiffener was added because the strip model ignores arch action; a shell finite-element check or the CalRig load test at TRL 4 decides |
| 4 | PR-005 at 1 m3/min leaves no margin for three people's CO2 (1.0 to 1.4 m3/min) | Accepted as a finding; restating a target is Amish's decision (SVD-DEC-001 open decision 5). The design delivers 15 m3/min |
| 5 | S5 says a 70 % splice, the script uses 90 % | Accepted. The claim now says 90 % and gives 5.04 at 70 % |
| 6 | S7 and S10 rest on assumptions | Accepted. Both are now Plausible (friction coefficient and preload; hand-over-hand speed) |
| 7 | S8 states 0.25 m3/s, the script uses 0.27 | Accepted. Text corrected; S8 is Plausible until a named blower curve is found |
| 8 | Battery logistics: D7 wants six batteries and two chargers, I1 showed two spares and one charger | Partly accepted. The BOM does carry six batteries (four in the two drill kits and two spares, lines 30 and 32) and a charger in each kit; package I1 omitted the second charger, now added (10.9 kg) |
| 9 | I2 omits the second trestle: the kit is about 370 kg, not 336 kg | Accepted. `sizing.py` and SVD-CAL-001 corrected (370 kg in 13 packages; heaviest 37.7 kg unchanged) |
| 10 | H1 doubled the rope travel (30 km, not 60 km) | Accepted. `sizing.py` and SVD-CAL-001 corrected |
| 11 | The BOM monitor price (USD 550 each) is below the GBP 776.52 quote | Accepted as a finding. Not repriced here: the cost figure stays at the BOM total of USD 10,804.00 and the difference is recorded under SVD-DEC-001 open decision 2 |
| 12 | O1 used the top-fibre modulus of a modelled section | Accepted. O1 now uses the smaller modulus and a dynamic factor of 2: 19.5 MPa against 80 MPa |
| 13 | S12 has a 2.3 kg margin and the case is not counted | Accepted. S12 is Plausible |

Missing coverage the reviewer listed, and where it went: the 776 mm ring in a 780 mm bore leaves 2 mm a side, so pipe ovality and weld beads need a fit trial (PR-001, TRL 4 fit trial; SVD-RSK-001); a crawl-space check against shoulder breadth with gear, the trestle tipping moment against the portal anchor, the sheave pin, intrinsic safety of the lamps and monitors if methane is possible, and the generator exhaust in option C are not STEM rows and are listed in `docs/REVIEW.md` as checks to add at TRL 4; the weight of 60 m of aluminium rail in option B (about 170 kg for a pair before sleepers) is in SVD-OPT-001; the assumed runner wear of 0.1 mm per km stays an assumption (STM S16). Two reviewer points were already in the design: rope abrasion is managed by decision 25A (S15) and the pad friction is measured on CalRig (S7).


## Sources

- EN 10025-2: hot rolled structural steel, S355 yield strength (minimum, thickness up to 16 mm).
- Young, W. C. and Budynas, R. G., Roark's Formulas for Stress and Strain, cantilever and simply supported beams (strength of materials); edition to cite at TRL 4.
- Darcy-Weisbach pressure loss in ducts; Moody friction factors for flexible duct (fluid mechanics texts).
- Terminal velocity and pneumatic conveying: Klinzing, G. E. et al., Pneumatic Conveying of Solids (Springer), for the 0.7 of terminal velocity rule and the loading factor.
- Rope strength and the 15:1 life-safety rope factor: NFPA 1983 (now in NFPA 2500), FireRescue1 summary, accessed 2026-11-02.
- Four-gas monitors: manufacturer datasheet listed in SVD-MKT-001 (Honeywell BW MicroClip, GBP 776.52, accessed 2026-11-02).
- UHMW-PE friction on steel: manufacturer tables (typical 0.1 to 0.2 dry), conservative assumptions of 0.30 and 0.40 used.
- CO2 limits and heavy-work production: physiology and confined-space texts, to cite with page references at TRL 4 (the row needs 0.98 m3/min against 15.1 m3/min delivered).
- SVD-CAL-001 (docs/04-calcs/01-sizing.md) and `docs/04-calcs/sizing.py` for every closed-by reference.
