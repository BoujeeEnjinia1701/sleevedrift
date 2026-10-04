---
doc_id: SVD-BLD-001
title: SleeveDrift prototype build plan
project: SleeveDrift
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First build plan; design made constructable (SVD-DDR-002)
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Amish's decisions of 2026-10-03 (SVD-DDR-003): a drill drive and drum guard on each winch (new making sketch SVD-DWG-112, joint 9, steps 2, 3 and 15), rope inspection every shift with a spare set"
---

# SleeveDrift prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept SleeveDrift kit, component by component, and set it up in a length of rescue pipe. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register (`docs/06-design-decisions.md`), not here.

> **Safety:** SleeveDrift is used by people working inside a pipe under collapse debris, with ropes under tension and a winch haul driven by electric drills at the portal. It is an open engineering reference, not certified rescue, mining or confined-space equipment. Build and trial it in a test pipe on open ground first, never in a live rescue. Nobody enters the pipe without a gas monitor, a standby at the portal and a way to be pulled out; nobody stands on a rope line or near the face sheave while the train moves. The safety stops in section 6 apply to every trial.

## 1. What you are building

![Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. The made components (1 to 12) and the main bought ones, pulled apart and numbered in build order. Ropes, duct, blower, signal line, lamps, gas monitors and tools are not shown.*

The kit has three working groups. At the face, a steel ring 760 mm across is built from four curved segments bolted together inside the mouth of the pipe; the top segment runs on as a hood over the digger, and a flat sheave on the bottom segment turns the haul rope. Along the pipe, a train of four folded steel sledges on plastic runners shuttles between a pull rope and a tail rope, with a breakaway swivel at each end. At the portal, two bought self-tailing sailing winches stand on two welded trestles. Each winch is turned by a cordless right-angle drill fitted with a winch bit in place of the handle, behind a sheet guard round the back of the drum; the handles are kept for winding by hand if the drills cannot be used. A blower pushes fresh air down a layflat duct to a spigot under the hood. Left and right are as seen from the portal looking into the pipe: the train runs along the middle of the pipe floor, the return rope lies on the floor to its left, and the air duct hangs on the upper left wall. Twelve parts are made, by rolling and welding plate, folding sheet, welding square tube and rolling perforated sheet; the rest are bought and fitted. The parts cost about USD 10,800 from the BOM.

## 2. What changed to make it buildable

*Table 1. Changes from the concept (SVD-DDR-002).*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Ring | One short sleeve | Four rolled segments bolted through flanges inside | A one-piece ring is about 85 kg; the heaviest segment is 31 kg and rides in on a sledge |
| Ring fixing | Not shown | Ring rests on the pipe floor; four screws press pads on the pipe wall | Nothing is drilled or welded to the pipe and nothing needs power |
| Hood | A hood over the top third | Crown runs 250 mm past the ring, with ribs along its edges and a lip at the front | Stiffness and a leading edge |
| Return pulley | Fixed to the ring | A flat sheave on a pin and base plate welded to the bottom segment, under a kneeling cover | The sheave needs a flat, square seat inside a curved shell, and a guard |
| Loop and sledges | Endless loop with clip-on sledges | A train of four sledges shuttling between a pull rope and a tail rope | Two lanes of sledges do not fit beside a crew in the pipe |
| Haul station | A hand capstan | Two self-tailing winches on two welded trestles | A winding drum for 60 m of rope would be 1.4 m long |
| Haul drive | A hand capstan | A cordless right-angle drill on each winch, with a guard round the drum; handles kept as the fallback | Amish's decision 24B (2026-10-03): it roughly doubles the spoil hauled and adds nothing inside the pipe |
| Overload | Not shown | A breakaway swivel at each end of the train, 2.5 kN | A person heaving on a winch handle could put over 13 kN on the rope |
| Air outlet | Behind the hood | A steel spigot in two saddles inside the crown; duct on magnet hangers | The duct needs a rigid end and must leave room to crawl |

![The face end with the pipe cut away](../media/cutaway.png)

*Figure 2. The buildable face end, cut through the pipe axis: hood, a crown screw, the sheave under its cover and the duct spigot.*

## 3. Making the components

### 3.1 Bottom segment with sheave bracket

![Making sketch](../cad/drawings/SVD-DWG-101.png)

**What it is and what it is made from.** The lowest sixth of the ring, with the sheave seat welded inside it. 5 mm S355 plate, 50 x 10 mm and 60 x 10 mm flat bar, 10 mm plate, 25 mm and 20 mm round bar.

**How to make it.**

1. Cut a strip of 5 mm plate 450 mm by about 400 mm and have it rolled to 760 mm outside diameter; check it against a 760 mm template cut from plywood.
2. Trim the long edges so the arc is exactly 60 degrees (398 mm round the outside).
3. Weld a 50 x 10 mm flat bar inside each long edge, its face flush with the edge face, standing toward the ring centre.
4. Roll a 60 x 10 mm flat bar to fit inside the front edge and weld it on; grind the front of plate and bar to a 30 degree bevel.
5. Cut two 10 mm saddle plates to the curve of the shell, 195 mm long across the segment, so their tops sit 125 mm above the inside of the shell at its lowest point; weld them 325 mm apart on centres.
6. Weld the 345 x 195 x 10 mm base plate on top of the saddles. Its left-hand edge (the side the return rope runs) stops 10 mm short of the joint flange.
7. Weld a 25 mm bright bar pin square to the plate, 35 mm in from its left-hand edge and 170 mm from its rear edge, standing 60 mm high; drill a 6 mm cross hole 57 mm above the plate for the R-clip.
8. Weld four 20 mm bar posts, 80 mm high, at the plate corners (321 mm and 171 mm apart on centres); drill and tap M8 in their tops.
9. Leave the flange bolt holes until step 1 of section 3.2.

**How it fits the parts next to it.** The sheave drops onto the pin over a spacer and is held by a keeper washer and R-clip; the cover screws onto the posts.

![Close-up of the joint](05-build-plan/joint-03.png)

*Figure 3. Joint 3: plate, spacer, sheave, keeper and cover, cut through the pin.*

**Check before moving on.** The shell sits on the template with no gap over 2 mm; the pin is square to the plate within half a degree; a 260 mm disc turns on the pin without touching the shell.

### 3.2 Side segments (two)

![Making sketch](../cad/drawings/SVD-DWG-102.png)

**What it is and what it is made from.** The two sides of the ring, mirror images of each other. 5 mm S355 plate, flat bar as for the bottom segment, an M20 weld nut each.

**How to make it.**

1. Roll two strips 450 mm wide to 760 mm outside diameter and trim each to 90 degrees of arc (597 mm round the outside).
2. Weld the 50 x 10 mm flanges inside both long edges and the 60 x 10 mm cutting band inside the front edge; bevel the front as before.
3. Clamp each side segment to the bottom segment, flange to flange, on the template. Drill four 13 mm holes through both flanges together, 25 mm in from the shell, at 120 mm pitch starting 30 mm from the rear edge.
4. On each side segment, 20 degrees round from its joint with the crown (10 degrees above the horizontal) and 25 mm from the rear edge, drill a 22 mm hole through the shell and weld an M20 nut inside over it.

**How it fits the parts next to it.** The flanges bolt face to face with the bottom segment and the crown, four M12 bolts per joint, heads inside the ring.

![Close-up of the joint](05-build-plan/joint-01.png)

*Figure 4. Joint 1: crown flange to side flange with M12 bolts (the bottom joints are the same).*

**Check before moving on.** With the bottom and both sides bolted on the template, the open top spans the 120 degrees the crown needs, within 3 mm.

### 3.3 Crown segment with hood

![Making sketch](../cad/drawings/SVD-DWG-103.png)

**What it is and what it is made from.** The top third of the ring, running on 250 mm as the hood. 5 mm S355 plate, flat bar, 25 mm plate, two M20 weld nuts.

**How to make it.**

1. Roll a strip 700 mm wide to 760 mm outside diameter and trim to 120 degrees of arc (796 mm round the outside).
2. Weld the 50 x 10 mm flanges inside both long edges for the full 700 mm; they are the hood's ribs.
3. Roll a 60 x 10 mm lip and weld it inside the front edge of the hood.
4. Drill the flanges to match the side segments (clamped on the template).
5. Drill two 22 mm holes 15 degrees either side of the top, 25 mm from the rear edge, and weld M20 nuts inside.
6. Cut two saddles from 25 mm plate to cradle the 194 mm spigot, 60 mm long, and weld them inside the shell 40 degrees from the top toward the left-hand side, starting 50 mm and 170 mm from the rear edge.

**How it fits the parts next to it.** It bolts to both side segments; the spigot sits in its saddles under two band clamps.

![Close-up of the joint](05-build-plan/joint-06.png)

*Figure 5. Joint 6: duct over the spigot, the spigot in its saddles inside the crown.*

**Check before moving on.** Laid hood-down on the floor, the lip touches along its length; the four segments bolt into a ring that fits the 760 mm template all round.

### 3.4 Jacking screws with swivel pads (four)

![Making sketch](../cad/drawings/SVD-DWG-104.png)

**What it is and what it is made from.** Four bought M20 x 90 class 8.8 set screws, each with a turned mild steel pad 50 mm across and 7 mm thick.

**How to make it.**

1. Turn four pads with a 10 mm deep ball seat in the back.
2. Round each screw tip to a 12 mm radius so the pad can tilt about 5 degrees.
3. Fit a locknut to each screw.

**How it fits the parts next to it.** Each screw runs out through its weld nut and the shell and pushes its pad onto the pipe wall. The crown screws press the ring down onto the pipe floor; the side screws centre it.

![Close-up of the joint](05-build-plan/joint-02.png)

*Figure 6. Joint 2: a crown screw through its weld nut, the pad on the pipe wall, cut through the screw.*

**Check before moving on.** The pad swivels freely on the tip; the screw runs through the nut by hand.

### 3.5 Sheave spacer and keeper

![Making sketch](../cad/drawings/SVD-DWG-105.png)

**What it is and what it is made from.** A spacer 40 mm across and 20 mm long, and a keeper washer 44 mm across and 5 mm thick, both bored 25.5 mm.

**How to make it.** Cut and face the spacer from 40 x 7.5 mm tube; cut the washer from 5 mm plate and bore it.

**How it fits the parts next to it.** Spacer under the sheave, washer over it, R-clip through the pin (Figure 3).

**Check before moving on.** The sheave turns freely between them with about 1 mm of end play.

### 3.6 Sheave cover and kneeling plate

![Making sketch](../cad/drawings/SVD-DWG-106.png)

**What it is and what it is made from.** 4 mm chequer plate, 345 x 300 mm.

**How to make it.**

1. Cut the plate and break all edges.
2. Drill four 9 mm holes on the post centres, 321 mm and 171 mm apart; the plate overhangs the posts by 105 mm on the return-rope side.
3. Paint the edge that faces the portal yellow.

**How it fits the parts next to it.** Four M8 screws into the post tops; the rope enters under it from the portal side (Figure 3).

**Check before moving on.** The screws enter without forcing; the cover clears the keeper washer and pin by at least 20 mm.

### 3.7 Duct outlet spigot

![Making sketch](../cad/drawings/SVD-DWG-107.png)

**What it is and what it is made from.** 194 x 2 mm steel tube, 410 mm long.

**How to make it.** Cut to length, roll a 3 mm bead 20 mm from the rear end, deburr both ends.

**How it fits the parts next to it.** It lies in the crown saddles under two band clamps; the duct slides over its rear end and is clamped behind the bead (Figure 5).

**Check before moving on.** The duct end slides on by hand and cannot pull off past the bead once clamped.

### 3.8 Spoil sledges (four)

![Making sketch](../cad/drawings/SVD-DWG-108.png)

**What it is and what it is made from.** Folded trays of 1.5 mm galvanised sheet, 1,000 mm long, on two UHMW-PE runners 40 x 10 mm.

**How to make it.**

1. Cut the blank and fold it: a 160 mm base and two sides that flare to 300 mm apart at 130 mm high; fold a 10 mm lip along each top edge.
2. Fit and rivet or weld the two end plates; cut a 100 x 40 mm hand hole in each.
3. Weld an 8 mm plate lug 50 x 40 mm on the centre of each end plate, its 16 mm hole 30 mm out from the plate and 50 mm above the tray floor.
4. Screw two 1,000 mm runners under the base, 110 mm apart on centres, with countersunk M6 screws whose heads sit at least 4 mm below the running face.

**How it fits the parts next to it.** Sledges join end to end with connecting links through the lugs; the end sledges carry the breakaway swivels.

![Close-up of the joint](05-build-plan/joint-04.png)

*Figure 7. Joint 4: the connecting link between two sledges.*

**Check before moving on.** Each holds about 30 L of water level full; on a short length of the real pipe it rocks less than 3 mm.

### 3.9 Winch trestles (two)

![Making sketch](../cad/drawings/SVD-DWG-109.png)

**What it is and what it is made from.** Welded frames of 40 x 40 x 3 mm square tube with a 10 mm top plate and a 10 mm anchor eye; 34.8 kg each.

**How to make it.**

1. Cut the long rails 700 mm, the short rails 420 mm and four posts 480 mm.
2. Tack the base rectangle (700 x 500 mm outside) and the top rectangle on a flat table; check the diagonals within 3 mm.
3. Stand the posts on the corners of the base and weld the top rectangle on, 560 mm high overall.
4. Weld the 300 x 500 x 10 mm top plate across the top rails, centred 300 mm back from the front; drill it to the base pattern of the winch bought.
5. Weld the anchor eye plate to the centre of the rear top rail so its 22 mm hole is 640 mm above the ground, level with the rope at the drum.
6. Drill two 11 mm holes in the inner long rail, top and bottom, for the cross ties.

**How it fits the parts next to it.** The winch bolts to the top plate; a bow shackle and round sling run from the eye to a structural anchor behind.

![Close-up of the joint](05-build-plan/joint-07.png)

*Figure 8. Joint 7: the winch bolted to the trestle's top plate.*

![Close-up of the joint](05-build-plan/joint-08.png)

*Figure 9. Joint 8: the sling on the anchor eye, level at rope height.*

**Check before moving on.** It stands without rocking; the eye hole is within 10 mm of the rope height at the drum.

### 3.10 Trestle cross ties (four)

![Making sketch](../cad/drawings/SVD-DWG-110.png)

**What it is and what it is made from.** 40 x 40 x 3 mm square tube, 140 mm long, with 6 mm end plates.

**How to make it.** Cut the tubes, weld an end plate 80 x 40 mm to each end, drill two 11 mm holes 60 mm apart in each plate.

**How it fits the parts next to it.** M10 bolts through the end plates and the inner long rails of both trestles, two ties at the top and two at the bottom.

**Check before moving on.** Bolted up, the two trestles stand 140 mm apart and square to each other.

### 3.11 Stretcher towing spreader bar

![Making sketch](../cad/drawings/SVD-DWG-111.png)

**What it is and what it is made from.** 26.9 x 2.6 mm tube, 450 mm long, with a 10 mm plate towing eye.

**How to make it.** Cut the tube, drill a 10 mm hole 20 mm from each end, weld the eye at the centre and drill it 16 mm. Splice two 10 mm rope bridle legs to the stretcher's head grommets and through the bar's end holes.

**How it fits the parts next to it.** The bridle legs run from the stretcher's head grommets to the bar ends; the breakaway swivels clip to the eye in place of the train.

**Check before moving on.** Pulled by the eye, the bar sits square.

### 3.12 Winch drum guards (two)

![Making sketch](../cad/drawings/SVD-DWG-112.png)

**What it is and what it is made from.** A curved guard of 2 mm perforated steel sheet round the back of each winch drum, on two flat bar legs. About 0.5 kg each.

**How to make it.**

1. Cut a strip of perforated sheet 175 mm high and about 275 mm long and roll it to 260 mm outside diameter, so it wraps a third of the way round the winch.
2. Cut two 30 x 5 mm flat bar legs 65 mm long and weld them inside the curve, 10 degrees in from each end, so they stand 45 mm below its lower edge.
3. Drill each leg foot for an M8 bolt, and drill and tap the trestle top plate to match.
4. Deburr every edge.

**How it fits the parts next to it.** The legs bolt to the top plate behind the winch, on the side away from the pipe; the open side faces the pipe so the rope reaches the drum. The drill sits above it on the winch socket.

![Close-up of the joint](05-build-plan/joint-09.png)

*Figure 10. Joint 9: the drill on its winch bit in the winch socket, with the drum guard round the back of the drum.*

**Check before moving on.** The guard is at least 10 mm clear of the drum and of the rope on the drum all the way round, and there is no edge that could catch a sleeve.

### 3.13 Bought components

- **Face sheave.** 260 mm across, grooved for 10 mm rope, bronze bush for a 25 mm pin, rated at least 1,000 kg. Check the bore fits the pin.
- **Joint bolts.** Twenty M12 x 40 class 8.8 with nuts and washers (sixteen used).
- **Runner strip.** UHMW-PE 40 x 10 mm, cut to 1,000 mm and drilled for the sledges.
- **Connecting links and shackles.** For 8 mm lugs with 14 mm pins and split pins.
- **Breakaway swivels.** Three cable-pulling breakaway swivels with shear pins set to 2.5 kN, and a pack of spare pins. Fit the pins and record their rating.

![Close-up of the joint](05-build-plan/joint-05.png)

*Figure 11. Joint 5: a breakaway swivel between the pull rope and the train.*

- **Ropes.** 10 mm polyester double braid of at least 18 kN: a 75 m pull rope and a 140 m tail rope, each with an eye splice at the train end. A spare set of the same two ropes goes in the kit, with a 9 mm slot wear gauge cut from scrap sheet.
- **Winches.** Two two-speed self-tailing winches for 8 to 12 mm rope, rated at least 10 kN, with locking handles.
- **Drill drive.** Two heavy-duty cordless right-angle drills (18 V class, at least 60 N m) with an adjustable slip clutch, a trigger that cannot be locked on and a side handle; two winch bits that fit the winch socket; six 5 Ah batteries in all and two chargers.
- **Rope bins, slings and shackles.** Two 80 L tubs; two 1 t round slings with bow shackles.
- **Air line.** A 200 mm confined-space blower giving at least 0.27 m³/s at 500 Pa, nine 7.6 m lengths of layflat duct with couplings, and sixty magnet hangers.
- **Light, signal and gas.** Two magnetic LED work lamps and four cap lamps; two sound-powered telephones and 80 m of cable with a pull-cord bell; two four-gas monitors.
- **Stretcher and tools.** A roll-up confined-space stretcher; short-handled spade and pick (cut the handles to 450 mm), hammer, chisels, bolt cutter, hacksaw, scoop pans, with wrist lanyards.

## 4. Putting it together

Steps 1 to 3 are at the portal, steps 4 to 11 at the face, and steps 12 to 15 bring the haul into use. For a first trial, use a test pipe on open ground.

### Step 1: set the trestles and bolt the cross ties

![Step 1](05-build-plan/step-01.png)

Set the two trestles on level ground 5.5 m behind the pipe mouth, in line with the pipe, and bolt the four cross ties with M10 bolts.

### Step 2: bolt the winches and drum guards to the top plates

![Step 2](05-build-plan/step-02.png)

Winch A, for the pull rope, goes on the right-hand trestle (looking from the station toward the pipe); winch B, for the tail rope, on the left-hand one. Use the winch maker's bolts and washers under the plate. Bolt a drum guard behind each winch, on the side away from the pipe.

### Step 3: slings to the structural anchor; rope bins out

![Step 3](05-build-plan/step-03.png)

Run each round sling from its anchor eye, level, to a structural anchor behind the station: a rock bolt, a steel rib or a platform anchor rated for at least 5 kN. Never use the pipe-pushing machine. Put a rope bin beside each trestle, under the self-tailer's outlet. **Hold point:** the slings are tight and level before any rope goes on a winch.

### Step 4: set the bottom segment in the pipe mouth

![Step 4](05-build-plan/step-04.png)

Carry the bottom segment in on a sledge, bevel first. Set it on the pipe floor with 200 mm inside the pipe and 250 mm beyond the mouth.

### Step 5: bolt the side segments to the bottom

![Step 5](05-build-plan/step-05.png)

Lift each side segment into place against the bottom segment's flanges and fit four M12 bolts per joint, heads inside the ring, finger tight.

### Step 6: crown segment on top; tighten all joints

![Step 6](05-build-plan/step-06.png)

Lift the crown in with the hood forward and bolt it to both sides. Tighten all sixteen bolts to about 80 N m.

### Step 7: run the jacking screws out to the pipe wall

![Step 7](05-build-plan/step-07.png)

Run the two crown screws out first until their pads press the ring down onto the pipe floor, then the two side screws. Tighten each to about 60 N m and lock the nuts. **Hold point:** recheck these screws at every shift change.

### Step 8: drop the sheave onto its pin

![Step 8](05-build-plan/step-08.png)

Spacer, sheave, keeper washer, R-clip. Spin the sheave by hand.

### Step 9: cover over the sheave

![Step 9](05-build-plan/step-09.png)

Four M8 screws into the posts, with the open side toward the portal so the ropes run in under it.

### Step 10: duct spigot into its saddles, duct over it

![Step 10](05-build-plan/step-10.png)

Lay the spigot in the crown saddles with its bead toward the portal and close two band clamps round it. Slide the duct end over it past the bead and clamp it. Hang the duct along the upper wall on magnet hangers every 2.5 m back to the portal and couple it to the blower.

### Step 11: lamp inside the hood; signal line to the face

![Step 11](05-build-plan/step-11.png)

Set the magnetic lamp inside the hood, aimed at the face. Run the telephone cable on the hangers near the top of the pipe and hang the face telephone inside the rear of the ring. Run the bell cord beside it.

### Step 12: make up the train

![Step 12](05-build-plan/step-12.png)

Join the four sledges with three connecting links and fit a breakaway swivel to each end lug. Check every split pin.

### Step 13: reeve the tail rope round the face sheave

![Step 13](05-build-plan/step-13.png)

Shackle the tail rope's eye to the train's face-end swivel, take it round the face sheave and back along the left-hand side of the pipe floor to winch B, three turns on the drum and into the self-tailer. Shackle the pull rope to the portal-end swivel and lead it to winch A in the same way.

### Step 14: casualty stretcher ready at the portal

![Step 14](05-build-plan/step-14.png)

Splice the bridle to the stretcher's head grommets and the spreader bar. Keep it rolled at the portal; to use it, unclip the train from the swivels and clip the swivels to the spreader bar's eye and to the stretcher's foot. The casualty is hauled hand over hand, not with the drills.

### Step 15: drills on the winch sockets for hauling

![Step 15](05-build-plan/step-15.png)

Set each drill's clutch to about 35 N m, fit the winch bit in its chuck and push the bit into the winch socket with the drill body pointing outward, away from the rope lane. Run the winches in high gear only, at about 120 rpm. The operator holds the drill by both handles; it stops as soon as the trigger is let go. Stow the winch handles where they can be reached, for winding by hand if a drill fails or the batteries run out. **Hold point:** with the train empty, check that each drill's clutch slips before the winch drum stalls.

## 5. First checks

*Table 2. First checks (listed here; a TRL 4 test report records them).*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Every piece passes a 776 mm ring gauge and the test pipe | R1 | Pull each piece through 3 m of the pipe | No piece snags; the ring assembles in the mouth |
| Hood load | R2 | 5 kN spread on the hood on CalRig, head form 100 mm below | No contact with the head form; no permanent set |
| Ring hold | R2, R11 | Pull 5 kN backward on the sheave pin with the ring jacked in the test pipe | The ring does not move |
| Breakaway release | R11 | Pull each swivel to release on a calibrated gauge | Releases between 2.2 and 2.8 kN |
| Handle force | R4 | Spring balance on the handle with a loaded train | Under 200 N in high gear |
| Drill clutch | R11 | Set the clutch, then pull the rope against a load cell in high gear | The clutch slips at about 1.5 kN, below the swivel release |
| Drill haul rate | R3 | Time loaded and empty runs over the test pipe | About 14.5 m/min |
| Air at the face | R5 | Anemometer across the spigot | At least 1 m³/min |
| Gas monitors | R12 | Bump test before each shift | Both alarm |
| Casualty drill | R6 | 100 kg manikin, 60 m, three people hauling | Under 5 min |
| Set-up drill | R7 | Timed from arrival at the portal | Hauling within 2 h |

## 6. Safety stops

Work stops at each point below until what is listed is true.

1. **Before anyone enters the pipe:** gas monitors bump tested and worn; blower running with its intake in clean air; standby person at the portal; the incident commander (or trial lead) has agreed the signal code.
2. **Before the first haul:** slings tight and level at rope height to a rated anchor; both winches bolted down; swivel pins checked to 2.5 kN; jacking screws tightened and locked.
3. **Before every haul:** a clear signal from the face that nobody is on the rope lines or near the sheave; the cover is on the sheave; the easing winch is tended; both drum guards are in place and the drill is in high gear.
4. **Before loading the hood or the sheave in a test:** the load is applied by the rig, never by people standing on or under the hood.
5. **If a swivel releases:** stop hauling, find and clear the jam, fit a new pin of the same rating. Never fit a bolt or a stronger pin.
6. **At every shift change:** recheck the jacking screws; inspect both ropes along their length against the 9 mm wear gauge and swap in the spare set if any part is worn through the cover or passes the gauge; check both swivels for damage, both drill clutch settings and both guards; rotate the crews.
8. **Drills:** never wedge or tape a drill trigger, never use a drill in low gear, never haul the stretcher with a drill, and keep loose clothing and gloves away from the drum. Charge batteries in the open at the portal, away from fuel and the blower intake.
7. **On any gas alarm or loss of air:** everyone out of the pipe, haul stopped, until the cause is found and the air is clear.

## 7. Tools, skills and workspace

- **Workshop:** plate rolling (or a fabricator who rolls), MIG or stick welding, a pillar drill, a lathe for the pads and spacer, a sheet metal brake for the sledges, a 760 mm plywood template and a flat table.
- **Skills:** structural welding, rigging and rope splicing (or bought spliced eyes), and a person trained in confined-space entry for any trial inside a pipe.
- **Trial site:** open ground with a test pipe of the same bore, at least a few metres long, chocked so it cannot roll; a rated anchor point behind the station; power for the blower and the battery chargers.
- **Hand tools at set-up:** 19 mm and 30 mm spanners, torque wrench to 80 N m, 13 mm spanner for M8, rope knife and tape, spring balance, anemometer.

## 8. Where the numbers come from

- Parametric model: `cad/src/model.py` (STEP and STL in `cad/step` and `cad/stl`).
- General arrangements: `cad/drawings/SVD-DWG-001` (ring and sheave) and `SVD-DWG-002` (portal station); making sketches `SVD-DWG-101` to `112`.
- Calculations: `docs/04-calcs/01-sizing.md` (SVD-CAL-001) and `docs/04-calcs/sizing.py`.
- Bill of materials: `bom/bom.csv`.
- Pictures: `cad/src/build_plan_media.py`.
