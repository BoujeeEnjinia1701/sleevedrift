# Review note: SleeveDrift

## 2026-10-03: Amish's requirement decisions carried out

Amish Chadha (owner), 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed." For SleeveDrift that decided items 24B, 25A and 26C as recommended; record SVD-DDR-003 (`docs/decisions/0003-requirement-decisions-2026-10-03.md`). Nothing was committed or pushed.

**Changes and new results.**

- **R3, decision 24B: portal drill drive.** A cordless right-angle drill on a winch bit in each winch socket, motor body outboard, with a perforated-sheet drum guard round the rear of each winch; winch handles stowed as the fallback; nothing extra inside the pipe (R8 still met). `cad/src/model.py` (drills, bits, guards and four new checks; checks OK), STEP and STL regenerated; BOM lines 30 to 33 (USD 700). New result (SVD-CAL-001 v0.2, D4): 14.5 m/min, a 17.3 min cycle, **0.42 m³/h against the 1 m³/h target, still not met**; 0.22 m³/h by hand. Drill safety kept: the clutch at 35 N m slips at 1.55 kN of rope pull in high gear, below the 2.5 kN swivel release; in low gear it would allow 4.8 kN, so the drill is used in high gear only (D6); the trigger has no lock-on; the swivels stay the limit. About 111 Wh an hour of hauling: six 5 Ah batteries and two chargers on portal power (D7). R6 unchanged (3.5 min by hand; 5.1 min with the drill, so hand hauling stays the method). R7: 93 min, about 1.6 h (met on paper).
- **R9, decision 25A: inspection and a spare set.** BOM line 34 (spare ropes and a 9 mm slot wear gauge, USD 236.50, 15 kg); the shift-change safety stop now inspects both ropes against the gauge and swaps in the spare set if worn. New result (H1 to H3): at the drill rate 72 h is about 250 round trips; R9 is managed by inspection and spares, and the TRL 4 endurance trial decides whether a tougher rope is needed.
- **R1, decision 26C.** The 600 mm variant waits for the co-design partner; no design change. R1 met for 800 mm; the stretch is open (A5).
- **Requirements:** `docs/03-requirements.md` v0.4 (status of R1, R3, R8 and R9; targets unchanged, none restated). **Calculations:** `docs/04-calcs/01-sizing.md` v0.2, `sizing.py`, `results.csv`.
- **Mass and cost:** kit about 328 kg in 13 packages (was 304 kg in 12), heaviest 34.8 kg (R10 met); drill drive package 9.5 kg, ropes and spare set 29.9 kg. Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 10,804.00 (USD 5,804.00 over the target).
- **Pictures:** SVD-DWG-002 Rev P3 (station GA with drills and guards); new making sketch SVD-DWG-112 (drum guard); build plan overview, joint 7 (handle stowed), new joint 9 (drill on the winch socket), steps 2 and 3 (guards), new step 15 (drills fitted); concept hero and blueprint (key figure on the drill drive), `flow.png` (now battery to spoil, D8) and `model.glb`. `docs/05-build-plan.md` v0.2 (section 3.12 drum guards, drill drive in bought parts, step 15, first checks for the clutch and haul rate, safety stops 6 and 8).
- **Register:** `docs/06-design-decisions.md` v0.2: the three items moved to Decisions made; one new open question (below).
- **Appearance model:** `cad/src/product_model.py` now shows the drills and drum guards in the station detail view; scenes exported to `/home/claude/renders/sleevedrift`. Photoreal renders, captions and cards need redoing on Amish's Mac.

### New question for Amish

**R3 target.** **Proposed, awaiting Amish.**

- *State:* with the decided drill drive the haul moves about 0.42 m³/h against R3's 1 m³/h (SVD-CAL-001, D4). Cause: once the haul is powered, loading and tipping take almost half the 17.3 min cycle; the hand-dug face at Silkyara produced about 0.27 m³/h (D3), so the haul now keeps ahead of the face.
- *Options:*
  - **A. Restate R3** as "moves loose spoil 60 m faster than the face it serves produces it; at least 0.4 m³/h with a two-person portal crew". R3: met at 0.42 m³/h on paper. Cost: none. Mass: none.
  - **B. Keep 1 m³/h** and record R3 as not met until the TRL 4 timed trial. Cost: none. Mass: none.
  - **C. Add the longer train and faster handling** (six sledges, two people tipping, spoil pre-bagged). R3: about 0.71 m³/h, still not met. Cost: about USD 240 more. Mass: about 15 kg more.
- *Recommendation:* **A.** The 1 m³/h figure came from the scaffold, not from a face rate; a haul that keeps ahead of hand digging is what the crew needs, and the timed trial confirms the margin. If a powered digging face is ever used, it needs its own haul study.

### Cross-repo actions

None.

### Safety concerns

- The drills are powered machinery at the portal: drum guards in place, high gear only, triggers never wedged, stretcher never hauled with a drill, batteries charged in the open away from fuel and the blower intake. The clutch slip setting is a first check at TRL 4.
- A worn rope is the main 72-hour risk; the shift inspection and spare set manage it but do not prove it.

### Recommended next step

Amish decides the R3 target question. The design is then ready for TRL 4 when the phase allows, as recommended below.

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

## 2026-10-04: Amish's requirement decisions carried out (round 3)

Amish on 2026-10-04: "For round 3, I agree with all your proposed recommendations". For SleeveDrift this decides open decision 1 of SVD-DEC-001 as recommended (4A). Recorded in `docs/decisions/0004-r3-restated.md` (SVD-DDR-004). Wording and records only; no geometry. Not committed or pushed.

### Changes

- `docs/03-requirements.md` v0.5: R3 restated as "moves loose spoil faster than the face produces it; at least 0.4 m3/h"; Amish quoted; count of requirements met updated.
- `docs/04-calcs/01-sizing.md`: summary, section D and the results table now say R3 is met as restated.
- `docs/06-design-decisions.md` v0.3: open decision 1 moved to Decisions made; Open decisions now "None."
- No model, BOM, drawing or media change was needed.

### New results

- R3: met as restated, 0.42 m3/h against at least 0.4 m3/h (hand-dug faces about 0.27 m3/h; hand fallback 0.22 m3/h).
- Other requirements, cost and mass unchanged.

### For Amish

Nothing new.

## 2026-10-04: photoreal renders redone after the round-2 and round-3 decisions

Views: hero, exploded, detail; cards regenerated; image_qc passes and `render.py --check` has no FAIL.
