---
doc_id: SVD-RSK-001
title: SleeveDrift risk register and hazard analysis
project: SleeveDrift
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: 2026-11-02
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-02
    author: Amish Chadha
    change: First issue at the kit 1.9.1 upgrade, for option A; project risks, preliminary hazard analysis and a first-pass design FMEA
---

# SleeveDrift risk register and hazard analysis

The top risks are the ones no desk study can close: the real pipe (bore, weld beads, rust) may not match the 780 mm bore the ring is cut for; rope abrasion and ring friction are assumed values; and a hand crew at a collapse face works with falling debris, bad air and moving ropes that the kit can reduce but not remove. Method: STANDARDS section 23, with the hazard method of ISO 12100 in preliminary form (SVD-REG-001 G5). Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high).

> **Safety:** This register is a design-stage analysis for a paper design. It is not a safety case and does not make the kit safe to use. Every control marked "use rule" depends on an incident commander, a standby crew and training that the kit does not supply.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| K1 | The real pipe is not 800 x 10 mm with a 780 mm bore | Pipe sizes and wall differ by site; internal weld beads | The ring and sledges do not pass or fit | 3 | 4 | Design lead | Fit trial in pipe sections; parametric ring (SVD-CAL-001 A5); confirm with the co-design partner |
| K2 | No co-design partner is found | No force or contractor answers | The kit stays a reference, never trialled | 3 | 4 | Project lead | Approach NDRF with the Jhansi hand miners first (SVD-DDR-001 item 11); keep other forces open |
| K3 | Cost stays about twice the target | Winches, monitors, signal line and blower are catalogue items | Few forces or contractors can hold a kit | 4 | 3 | Design lead | Decision for Amish: hold or restate the USD 5,000 target (PR-013); value engineering of the signal line and winches |
| K4 | Friction and wear assumptions are wrong | Pad friction 0.2, runner friction 0.3 and rope abrasion are assumed | Ring slips, haul force or rope wear exceed the paper values | 3 | 4 | Test lead | Pull-out test on CalRig, sled test and endurance trial at TRL 4 |
| K5 | The haul margin is thin | 0.42 against 0.4 m3/h; loading and unloading take half the cycle | R3 is missed in the field | 3 | 3 | Design lead | Timed trial; longer train is a known option (SVD-DDR-004) only if the face outpaces the haul |
| K6 | A builder sells an uncertified rescue kit | Open design copied without the safety notes | Harm and a reputation problem | 2 | 5 | Maintainer | Safety notes in every document; licence disclaimers; reference-not-product wording |
| K7 | The rope used is not rated for life-safety use | A cheaper unmarked rope is bought | A casualty load fails the rope | 2 | 5 | Procurement | Choose a marked rope (SVD-REG-001 G6); the 15:1 factor holds on paper |
| K8 | Key parts become unavailable | Winch or drill model discontinued | Rebuilds stall | 3 | 2 | Procurement | Specs, not brands, in the BOM; two sources per catalogue item |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Fall of debris onto the digger | Face collapses or loose material above | Crush, burial | 5 | 3 | 5 mm steel hood over the digger (PR-002); crew of three; stand-down rules | Medium; the hood protects the head and shoulders only |
| H2 | Low oxygen, CO, H2S or flammable gas | Gas seeps through the debris; exhaust; no air movement | Asphyxia, poisoning, explosion | 5 | 3 | Forced air to the face (PR-005); two four-gas monitors (PR-012); no spark source in the pipe (PR-008) | Medium; atmosphere assessment is the operator's |
| H3 | Rope under tension snaps or whips | Overload, abrasion, a knot | Strike, amputation | 5 | 2 | Breakaway swivels at 2.5 kN (PR-011); rope factor 6.5 on the release; wear gauge each shift; nobody in line with a rope | Medium; use rule |
| H4 | Drill torque or runaway on the winch | Slip clutch set too high; drill used in low gear | Rope overload, hand or clothing drawn in | 4 | 3 | Clutch 35 N m slips at 1.55 kN in high gear (STEM S6); dead-man trigger; drum guard; high gear only | Medium; use rule |
| H5 | Entrapment by the moving train | A person in the pipe while it moves | Crush, drag | 5 | 2 | Signals by telephone and pull cord (PR-015); nobody on the rope line or near the sheave while it moves | Medium; use rule |
| H6 | Heat stress, dust and fatigue | Warm air, shifts, effort | Collapse of a rescuer | 4 | 4 | Air changed every 1.9 min; shifts of three; rest rules | Medium |
| H7 | Ring slips at the face end | Friction lower than assumed; sheave load of 5 kN | Ring drops or moves under a digger | 5 | 2 | Four jacking screws at 15 and 10 kN preload, factor 3.2 on the sheave load (STEM S7); inspection | Medium until the pull-out test |
| H8 | Manual handling injury | Pieces up to 37.7 kg | Back injury | 3 | 3 | Two-person lift; ring segments ride in on a sledge | Low |
| H9 | Sharp edges and pinch points | Cut sheet, flanges, lugs | Cuts, crushed fingers | 2 | 4 | Edges broken in the model; guards on drums | Low |
| H10 | Blower or mains fault at the portal | Damp, cable damage | Shock, fire | 4 | 2 | Residual-current protection on portal power (use rule); nothing mains in the pipe | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Crown segment and hood | Carry 5 kN over the digger | Buckles or yields | Hood drops onto the digger | Overload, weld defect | 5 | 2 | 3 | 30 | Load test on CalRig; weld inspection |
| F2 | Jacking screw and swivel pad | Hold the ring in the pipe | Pad slips on rusty pipe | Ring moves under the sheave pull | Friction below 0.2 | 5 | 3 | 4 | 60 | Pull-out test; proof load; check each shift |
| F3 | Segment joint bolts (M12) | Join the four segments | Loosen or shear | Ring opens | Vibration, tightening | 4 | 2 | 3 | 24 | Torque check; locking by weld nut and washer |
| F4 | Face return sheave and pin | Turn the tail rope | Pin bends or rope jumps | Tail rope stops or snags | 5 kN load at the limit | 4 | 2 | 3 | 24 | Pin factor 3.1 on yield; keeper and R-clip |
| F5 | Breakaway swivel shear pin | Limit rope tension to 2.5 kN | Releases early or late | Train lost or rope overload | Pin scatter | 5 | 3 | 5 | 75 | Release tests on a batch; never bypass |
| F6 | Pull and tail ropes | Haul the train | Abrasion parts the rope | Train stranded; whip | Grit on the floor | 5 | 3 | 3 | 45 | Wear gauge each shift; spare set |
| F7 | Sledge tray and end plates | Carry 30 L of spoil | Tears or tears off lug | Spoil spills; train splits | Overload, fatigue | 3 | 2 | 3 | 18 | Weld inspection; lug welds sized on 2.5 kN |
| F8 | Sledge runners and screws | Slide on the floor | Runner wears through or screw backs out | Steel on steel; noise | 30 km of sliding | 2 | 3 | 3 | 18 | Replace at 3 mm wear; nuts and washers |
| F9 | Winch (bought) | Hold and haul the rope | Pawls fail to hold | Load runs back | Wear, dirt | 5 | 2 | 4 | 40 | Inspect each shift; load test |
| F10 | Drill, bit and clutch | Drive the winch | Clutch set too high or fails | Rope overload | Setting error | 5 | 3 | 3 | 45 | Clutch check each shift; high gear only; swivels remain the limit |
| F11 | Trestle and cross ties | Hold the winch to the anchors | Overturns or tears from the anchor | Winch moves under load | Anchor not as assumed | 5 | 2 | 4 | 40 | Moment margin 4.6 times; anchor check at set-up |
| F12 | Layflat duct and magnet hangers | Carry air to the face | Duct falls or kinks | Air stops | Hanger fails on rust or debris | 4 | 3 | 3 | 36 | Air flow check at the face; monitors alarm |
| F13 | Blower | Deliver 15 m3/min | Stops or loses pressure | No air | Power, blockage | 4 | 3 | 2 | 24 | Spare blower recommended; monitors alarm |
| F14 | Gas monitor | Alarm on bad air | Sensor drifts or poisons | No warning | Missed bump test | 5 | 3 | 3 | 45 | Bump test each shift; two monitors |
| F15 | Telephone and cable | Signal between face and portal | Cable cut or mic fails | No signal | Snag, damp | 4 | 3 | 2 | 24 | Pull-cord bell backup |
| F16 | Stretcher and spreader bar | Carry the casualty | Strap or bar fails | Casualty drops | Overload at 2.5 kN | 5 | 2 | 3 | 30 | Bought rescue-rated stretcher; limit by swivel |
| F17 | Pull rope under a casualty | Bring a casualty out on the rope | Rope load above what life-safety practice allows | Casualty dropped or rope parts | The rope has a factor of 6.5 on the 2.5 kN release, not 15 (STM S17) | 5 | 2 | 4 | 40 | Proposed, awaiting Amish: a stretcher-only breakaway at 1.0 kN (SVD-DEC-001 open decision 4) |

Scoring: severity, occurrence and detection 1 to 5 (detection 5 = hard to detect). The highest RPNs (F5, F2, F6, F10, F14; F17 is new from the independent STEM review) are all items the paper design cannot close; they set the first trial list for TRL 4 in the plan (SVD-PLN-001).
