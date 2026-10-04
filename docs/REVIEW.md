# Review note: SleeveDrift

## Session 2026-10-03: round 2 requirement decisions applied

Amish, 2026-10-03: "i approve all of the 47 recommendations provided by you. Execute them." For SleeveDrift that decides the three requirement decisions of the TRL 3 session below as recommended: 1B (R3), 2A (R9, with the TRL 4 endurance trial deciding whether B is needed) and 3C (R1 stretch). They are recorded in `docs/decisions/0003-requirement-decisions-round2.md` (SVD-DDR-003) and moved to Decisions made in `docs/06-design-decisions.md` (SVD-DEC-001 v0.2). Phase cap TRL 3 kept: no test articles, test plans, firmware, build-log entries or purchasing lists. Nothing was committed or pushed.

**What changed.**

- **1B, R3: portal drill drive.** `cad/src/model.py`: new `drill_drive()` massing (winch bit, right-angle head, motor body, battery) on each winch socket as the `drills` component (BOM line 30); `winch()` takes `handle=False`, the hand handles stowed as the fallback; the station STEP and STL include the drills. BOM line 30: two sets at USD 350, USD 700.
- **2A, R9: inspection and spares.** BOM line 31: spare pull and tail rope and a go/no-go wear gauge, USD 236.50, about 15 kg; build plan safety stop 6 now has the gauge check and the swap.
- **3C, R1 stretch: kept open.** No hardware change; SVD-CAL-001 A5, the requirements and the concept precis say the stretch waits for the co-design partner.
- `docs/04-calcs/sizing.py` re-run (drill drive as the design rate, hand as fallback, new clutch torque line D6, durability at the drill rate, two new packages): `results.csv` and `docs/04-calcs/01-sizing.md` (SVD-CAL-001 v0.2).
- Regenerated with the repo's scripts: STEP and STL (`cad/src/model.py`), SVD-DWG-001 (Rev P2, unchanged geometry) and SVD-DWG-002 (Rev P3, drills added) (`cad/src/sheets.py`), concept media and `media/model.glb` at linear deflection 1.0 and angular 0.35 (`cad/src/concept_media.py`), the build plan overview, making sketches, joints and steps (`cad/src/build_plan_media.py`, joint 7 and step 2 now show the drill drive). `cad/src/product_model.py` has the drills in the station detail.
- Text: `docs/03-requirements.md` v0.4, `docs/02-concept.md` v0.4, `docs/05-build-plan.md` v0.2, `README.md`; `project.yaml` trl_evidence gains SVD-DDR-003.

**Requirement status, before and after.**

| ID | Before | After |
| --- | --- | --- |
| R3 | Not met, 0.22 m³/h by hand | Not met, 0.42 m³/h with the drill drive (0.22 m³/h by hand, the fallback) |
| R9 | At risk, about 132 round trips in 72 h | At risk on paper, about 250 round trips at the drill rate; met in practice if a rope swap counts as maintenance; the TRL 4 endurance trial decides on the tougher rope |
| R1 | Met for 800 mm; 600 mm stretch at risk | Met for 800 mm; 600 mm stretch open, pending the co-design partner |
| R10 | Met, 304 kg in 12 packages, heaviest 34.8 kg | Met, 326 kg in 14 packages, heaviest 34.8 kg |

R2, R4 to R8, R11 and R12 are unchanged. R4 (hand force) now applies to the fallback; R8 still holds, the drills stay at the portal.

**Cost.** Estimated cost of the constructable design USD 9,867.50 before, USD 10,804.00 after (USD 700 drill drives, USD 236.50 spare ropes), USD 5,804.00 over the USD 5,000 value-engineering target. `budget_usd` unchanged: it is the value-engineering target (SVD-DDR-001 item 13), and Amish accepted overruns on 2026-10-03.

**New questions for Amish.** Each is **Proposed, awaiting Amish**, listed in SVD-DEC-001 as items 4 and 5.

**4. Drill gear and clutch rule.**
- *State:* at the winch socket the haul needs 18 N m loaded and 23 N m to start in high gear; the 2.5 kN swivel release corresponds to 57 N m in high gear but only 18 N m in low gear (SVD-CAL-001, D6). The TRL 3 recommendation said the clutch slips before the swivel releases; that holds only in high gear.
- *Option A:* drill in high gear only, clutch set at about 35 N m, the rule written on each trestle. R3 stays 0.42 m³/h. No cost.
- *Option B:* clutch set at about 15 N m so it slips first in either gear. The drill cannot start the loaded train in high gear and hauls in low gear at about a third of the speed.
- *Option C:* no rule; the swivel stays the only limit, as it is for hand cranking.
- **Recommendation: A.** The swivel is the designed limit in both gears; the rule keeps the clutch as a second, earlier limit in the gear the drill is used in.

**5. R9 wording.**
- *State:* option 2A meets R9 "in practice if a swap counts as maintenance", while R9 reads "72 hours of continuous operation without failure of rope, pulleys or sledges".
- *Option A:* restate R9 to allow a worn rope to be swapped as planned maintenance after the shift-change inspection. R9 met in practice on paper; shown in the endurance trial.
- *Option B:* keep the wording. R9 at risk until the endurance trial.
- **Recommendation: A.** It states what was chosen in 2A, and the trial still tests it.

**Safety notes.**

- The portal drill drive puts a powered tool on the haul. Its dead-man trigger stops the haul when let go; its slip clutch is an earlier limit in high gear only; the breakaway swivels remain the overload limit in every gear and for hand cranking. Build plan safety stop 2 now includes the clutch setting and high gear.
- The faster haul (14.5 m/min, both ways) means the train reaches the face sooner: hauling still starts only on a clear signal from the face, and nobody is on a rope line or near the sheave while the train moves.
- At the drill rate the ropes drag about 60 km per metre in 72 h, nearly twice the hand figure; the shift-change inspection against the wear gauge is part of the safety case until the endurance trial gives a wear rate.
- Battery charging stays at the portal in clean air; nothing powered goes into the pipe beyond lamps, monitors and signals (R8).

**Renders.** The photoreal renders made on Amish's Mac predate this session. The hero view changes slightly (drills on the winches at the station in the background); the detail view of the portal station changes visibly (drill drives on both winch sockets, hand handles gone) and needs a re-render. The exploded ring view is unchanged.

**Recommended next step.** Amish decides items 4 and 5. The design is then ready for TRL 4 when the phase allows: build the ring and a short test pipe, load test the hood and the ring's hold on CalRig, release test the swivel pins and set the drill clutches, then a timed haul with the drill drive and by hand, the casualty drill and the 72 h endurance run that settles the rope.

## Session 2026-10-03: TRL 3 (kit 1.7.0, /to-trl3 under Amish's pre-approvals)

Amish, 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Then, for this second batch: "Proceed with the remaining 15 scaffolds", under the same pre-approval. Every design choice in this session is therefore recorded as decided, dated 2026-10-03, in `docs/06-design-decisions.md`. Requirements that are not met or at risk are not decided here: they are set out below under "Decisions for Amish" (Amish, 2026-10-03: "A simple statement doesn't add value - ensure you are identifying a state and posing it as a clear recommendation for me to decide on."). Kit 1.7.0 was installed from the kit source; `.kit/PHASE.yaml` kept as installed. Nothing was committed or pushed.

### TRL 2

**What was done.**

- `docs/01-problem.md` (SVD-PRB-001 v0.2): safety note, first co-design candidate, answers to the open questions, questions for the first trials.
- `docs/03-requirements.md` (SVD-REQ-001 v0.2): concept status for every requirement; R11 (overload limit) and R12 (air monitoring) added.
- `docs/02-concept.md` (SVD-PRC-001 v0.2): how it works, components, key design choices, first-order numbers, safety, concept media.
- `docs/decisions/0001-trl2-review-decisions.md` (SVD-DDR-001): thirteen TRL 2 review items decided.

**Results.** First-order: the hood is far stiffer than it needs to be; the rope haul needs well under 200 N at a winch handle; the blower can deliver many times the air R5 asks for; the output of a hand-cranked haul over 60 m is limited by the power of one person.

**Requirements not met.** R3 (spoil haulage) was already short at TRL 2; it is carried to TRL 3 as a decision for Amish.

**Decisions made under the pre-approval.** SVD-DDR-001, items 1 to 13: 800 x 10 mm design pipe; ring held by jacking screws; shuttle train instead of a circulating loop; two self-tailing winches (SiltHaul capstan not used); breakaway swivels at 2.5 kN (R11); four-gas monitors (R12); forcing ventilation; sound-powered telephones; bought roll-up stretcher hauled hand over hand; India's National Disaster Response Force with the Jhansi hand miners as first co-design candidate (not agreed); CalRig and HatchSide as shared references; budget kept.

**Safety concerns.** Face collapse onto the digger; asphyxiation and gas; entrapment by moving ropes and the face sheave; rope overload from a person heaving on a winch handle; heat stress.

### TRL 3

**What was done.**

- `docs/04-calcs/01-sizing.md` and `docs/04-calcs/sizing.py` (SVD-CAL-001 v0.1), `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model with constructability checks (no overlaps between any two components, nothing floating, nothing through the pipe wall); STEP and STL in `cad/step` and `cad/stl` (ring, sledge, station; assembly STEP at the 60 m design case).
- `cad/src/sheets.py`: SVD-DWG-001 (hooded cutting ring and face sheave GA) and SVD-DWG-002 (portal haul station GA), Rev P2.
- `bom/bom.csv`: 29 lines, all priced, with suppliers by type.
- `cad/src/concept_media.py`: `media/hero.png`, `exploded.png` (face end), `cutaway.png` (face end), `flow.png`, `concept-blueprint.png` and `.pdf` (SVD-DWG-010), `model.glb` (coarse tessellation) and `viewer.html`.
- `docs/decisions/0002-design-for-construction.md` (SVD-DDR-002); `design_state: constructable`.
- `cad/src/build_plan_media.py`: overview, eleven making sketches (SVD-DWG-101 to 111), eight joint close-ups and fourteen step pictures; `docs/05-build-plan.md` (SVD-BLD-001) and `docs/06-design-decisions.md` (SVD-DEC-001).
- `cad/src/product_model.py` (`product_parts()`, `TITLE`, `RENDER_VIEWS` hero, exploded, detail); scenes exported to `/home/claude/renders/sleevedrift` (three .npz and .json, `sleevedrift__jobs.json`). Photoreal renders, captions and cards are made on Amish's Mac; the README already leads with `media/render-hero.png`.
- `README.md`, `project.yaml` (trl 3, trl_target 3), `docs/01-problem.md` v0.2, `docs/02-concept.md` v0.3, `docs/03-requirements.md` v0.3.

**Results (SVD-CAL-001).** Every piece passes a 776 mm circle in the 780 mm bore; the heaviest is the crown segment at 31.0 kg; the clear crawl circle beside the duct is 554 mm. The hood takes 5 kN at 5.5 MPa with 0.01 mm of deflection; the crown screws see 3.7 kN against a 15 kN preload. The loaded train (120 L, 203 kg of spoil) needs 786 N, 1,018 N to start; 71 N and 92 N at the handle in high gear. The breakaway swivels release at 2.5 kN; the rope keeps a factor of 6.5; the sheave pin a factor of 3.1; the ring's grip on the pipe a factor of 3.2. About 15.1 m³/min of air reaches the face. A casualty comes out in about 3.5 min with three people hauling. Set-up about 1.6 h. Kit about 304 kg in 12 packages, heaviest 34.8 kg. Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 9,867.50 (USD 4,867.50 over the target).

**Requirements not met or at risk.**

- **R3, not met on paper:** 0.22 against 1 m³/h.
- **R9, at risk:** rope abrasion over about 132 round trips in 72 h cannot be shown on paper.
- **R1 (600 mm stretch), at risk:** not designed.
- R7 is met on paper only as an estimate (1.6 h) and needs the timed drill.

#### Decisions for Amish

Each item below is **Proposed, awaiting Amish**, and is listed in `docs/06-design-decisions.md` under Open decisions.

**1. R3, spoil haulage.**

- *State:* about 0.22 m³/h of loose spoil moved 60 m by hand, against the R3 target (SVD-CAL-001, D2). Cause: one person cranking at a sustainable 60 W can drag the 786 N loaded train at only 3.9 m/min, and the empty return, loading and tipping take as long again.
- *Options:*
  - **A. Keep hand cranking only.** R3: about 0.22 m³/h, below the hand-dug face rate seen at Silkyara (about 0.27 m³/h). Cost: none. Mass: none.
  - **B. Add a portal drill drive.** A heavy right-angle drill with a winch bit on each winch socket, at about 120 rpm (14.5 m/min, 190 W at the rope), with spare batteries and a charger at the portal; hand cranking stays as the fallback, and nothing is added inside the pipe (R8 unchanged). R3: about 0.42 m³/h. Cost: about USD 700. Mass: about 7 kg. Safety: the drill clutch is set to slip before the 2.5 kN swivel releases, and the trigger is a dead-man switch.
  - **C. Option B plus a longer train and faster handling.** Six sledges, two people tipping at the portal and spoil pre-bagged at the face while the train travels. R3: about 0.71 m³/h. Cost: about USD 940. Mass: about 22 kg. A 1.1 kN loaded pull and a 6.9 m train.
- *Recommendation:* **B.** It doubles the haul, moves it past the face rate that hand digging produced at Silkyara so the face rather than the haul sets the pace, adds nothing inside the pipe and keeps hand cranking as the fallback. C is worth trying at TRL 4 only if the trial shows the face producing faster than B can haul.

**2. R9, shift durability.**

- *State:* the 72-hour target cannot be shown on paper. At the hand rate the kit makes about 132 round trips, and each metre of rope drags about 32 km over a gritty steel floor (SVD-CAL-001, H1). Cause: polyester braid abrasion on grit is not predictable without a test; the sheave, pins, sledges and runners are lightly loaded.
- *Options:*
  - **A. Inspect and carry spares.** Inspect both ropes at every shift change against a wear gauge and carry a spare set; a worn rope is swapped in about 20 min. R9: met in practice if the swap is accepted as maintenance, not failure. Cost: USD 237. Mass: 15 kg.
  - **B. Abrasion-resistant rope.** A 10 mm rope with a coated or abrasion-resistant cover of the same strength. R9: likely longer life; still unproven without a test. Cost: about USD 300 more. Mass: about 3 kg more. The self-tailer's grip on the cover must be checked.
  - **C. Rope rollers on the floor.** Low rollers every 10 m to lift both ropes off the floor. R9: least wear. Cost: about USD 500. Mass: about 25 kg. They put parts in the crawl lane and must be fixed without drilling.
- *Recommendation:* **A**, with the TRL 4 endurance trial deciding whether B is needed.

**3. R1 stretch, 600 mm pipe.**

- *State:* only the 800 mm pipe is designed. Cause: in a 600 mm pipe the crawl space, the duct and the return rope do not fit the same layout; the sizes are parameters in the model, but a second layout is needed.
- *Options:*
  - **A. Drop the 600 mm stretch from this design.** R1: met for 800 mm, stretch removed. Cost: none. Mass: none.
  - **B. Design a 600 mm variant now.** A 560 mm ring in three segments, 220 mm sledges, 150 mm duct. R1 stretch: met on paper after a second TRL 3 pass. Cost: about USD 900 for a second ring set and sledges. Mass: about 70 kg more in the kit.
  - **C. Keep it as a stretch until the partner answers.** Ask the co-design candidate whether 600 mm pipes are used for rescue before designing. R1 stretch: open. Cost: none now.
- *Recommendation:* **C.** The partner's answer decides whether a second ring is worth making.

**Decisions made under the pre-approvals.** SVD-DDR-001 (thirteen TRL 2 items) and SVD-DDR-002 (twelve design-for-construction changes, listed below); the appearance model additions (below). All in `docs/06-design-decisions.md`.

**Build plan findings (design changes made for construction, SVD-DDR-002).**

1. Ring in four bolted segments (crown with hood 120 degrees, sides 90, bottom 60), flanges inside; no joint on the floor lane; heaviest 31 kg.
2. Ring rests on the pipe invert; four M20 jacking screws (15 and 80 degrees from the top) press swivel pads on the pipe wall; nothing drilled or welded.
3. Hood ribs from the crown flanges, a hood lip, and bevelled cutting bands on the other segments.
4. Face sheave on a pin and base plate welded to the bottom segment on curved saddles, with spacer, keeper and a chequer-plate kneeling cover on four posts.
5. Rope legs 240 mm apart, rising to the sheave plane over the last 1.2 m; the train stops 1.2 m short of the mouth.
6. Sledges as folded 1.5 mm galvanised trays, 29.9 L, on UHMW-PE runners that sit on the pipe curve, with end lugs.
7. Shuttle train with connecting links and a breakaway swivel at each end.
8. Portal station as two welded trestles (34.8 kg each) with cross ties, anchor eyes at rope height, 5.5 m from the mouth so the rope reaches the drums at 6.6 degrees.
9. Duct spigot in two saddles inside the crown; duct on magnet hangers 265 mm off the pipe axis; crown jacking screws placed at 15 degrees to clear it.
10. Signal cable on magnet hangers near the crown; magnetic lamp inside the hood.
11. Stretcher spreader bar and bridle.
12. Set-up sequence: bottom segment first by hand on a sledge, the other three segments on one shuttle trip.

**Appearance model.** `product_model.py` uses the `model.py` solids in the shortened picture layout. Additions not in `model.py`: the pipe window (the last 2.8 m, cut open on the camera side), a platform slab, and a 1.75 m mannequin (`mannequin()`, standing) on the platform beyond the pipe's far end, beside the product and clear of the line of sight. Decided under the pre-approvals.

**Safety concerns.**

- The hood and the ring's fixing are calculated, not tested; the first load test is on CalRig with nobody under the hood.
- The ring's hold against the sheave pull depends on pad friction on the real pipe (assumed 0.20); it is a "to confirm" item and a first check.
- Rope and sheave entrapment inside the pipe: hauling only on a clear signal from the face, the sheave always covered.
- The breakaway swivels carry the overload case; a pin replaced by a bolt removes it. The build plan's safety stop 5 says so.
- Gas and air: the kit monitors and ventilates, but it cannot make the pipe safe on its own; the incident commander's rules govern entry.
- Option B in decision 1 would add a powered drive at the portal; its clutch and dead-man trigger are part of that option.

**Recommended next step.** Amish decides the three items above. The design is then ready for TRL 4 when the phase allows: build the ring and a short test pipe, load test the hood and the ring's hold on CalRig, release test the swivel pins, then a timed haul and casualty drill in a 60 m pipe run with the first co-design candidate.

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (SVD-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (SVD-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (SVD-REQ-001 v0.1): 10 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

### Next

- Run `/populate` to bring the repo to a strong TRL 2 with concept media.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.
