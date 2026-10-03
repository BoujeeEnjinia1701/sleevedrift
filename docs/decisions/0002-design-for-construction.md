---
doc_id: SVD-DDR-002
title: SleeveDrift design for construction
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
  change: Constructability review and the changes that make the design buildable, decided under Amish's pre-approvals of 2026-10-03
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** accepted

## Context

STANDARDS section 18 requires a constructable design at TRL 3: every part made by a stated process, and every part fitting and fastened to its neighbours. The concept (SVD-PRC-001 v0.2) showed a one-piece hooded sleeve, a return pulley "fixed to the ring", an endless loop with sledges, a hand capstan and an air duct, without saying how any of them is made, carried into a pipe or fixed. The constructability review went component by component, then checked the build123d model for overlaps between every pair of components and for parts that touch nothing (`python cad/src/model.py --check`: no overlaps and nothing floating). Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible". The changes below were decided under his pre-approvals of 2026-10-03 ("I pre-approve the batch runs along with any recommendations you come up with." and "Proceed with the remaining 15 scaffolds").

> **Safety:** Changes 1, 2, 4, 7 and 8 carry loads that protect people in the pipe; each is load tested before use (SVD-BLD-001, section 6).

## Options considered

For each part: make it as the concept drew it, or change it to the simplest physically sound form that keeps what it does. Changes that would alter what SleeveDrift does, its pitch or its safety case were not in scope.

## Decision

*Table 1. Changes made for construction.*

| # | Component | The concept had | The constructable design has | Why |
| --- | --- | --- | --- | --- |
| 1 | Hooded cutting ring | One short sleeve | Four rolled 5 mm S355 segments (crown 120 degrees with the hood, two sides of 90 degrees, bottom of 60 degrees), bolted through 50 x 10 mm flanges inside with four M12 bolts per joint | A one-piece ring is about 85 kg and cannot be carried along a pipe; the heaviest segment is 31 kg. No joint lies on the floor lane |
| 2 | Ring fixing | Not defined | Ring rests on the pipe invert; four M20 jacking screws in weld nuts (15 degrees either side of the top and 80 degrees) press swivel pads on the pipe wall | No drilling, welding or power at the face; the hood load goes into the pipe through contact, without free play |
| 3 | Hood | A hood over the top third | The crown runs 250 mm beyond the ring front; its flanges run the full 700 mm as hood ribs; a 60 x 10 mm lip inside the front edge; cutting bands with a 30 degree bevel on the other segments | Stiffness and an edge that can meet debris |
| 4 | Return pulley | Fixed to the ring | A bought 240 mm sheave lying flat on a 25 mm pin, on a 10 mm base plate with two saddles cut to the shell, welded to the bottom segment; spacer, keeper and R-clip; a 4 mm chequer-plate cover on four posts | The sheave needs a flat, square seat inside a curved shell; the cover guards it and is a kneeling plate |
| 5 | Rope legs | Along the floor | Train lane on the centre line; return leg on the floor 230 mm to the +Y side; both rise to the sheave plane, 185 mm up, over the last 1.2 m, so the train stops 1.2 m short of the mouth | Keeps the ropes clear of the ring rear and the jacking screws |
| 6 | Sledges | Low curved trays | Folded 1.5 mm galvanised trays, 160 mm base flaring to 300 mm, 130 mm deep, 1 m long (29.9 L), on two UHMW-PE runners that sit on the pipe curve; 8 mm end lugs | A form any sheet metal shop can fold; the runners set the friction |
| 7 | Loop | Endless rope with clip-on sledges | A shuttle train of four sledges joined by connecting links, with a 2.5 kN breakaway swivel at each end between the train and the ropes | See SVD-DDR-001, items 3 and 5 |
| 8 | Portal haul station | A hand capstan | Two bought two-speed self-tailing winches on two welded 40 x 40 x 3 mm trestles (34.8 kg each) tied by four bolted cross ties; anchor eyes level with the rope; round slings to a structural anchor; station 5.5 m behind the mouth so the rope rises 6.6 degrees to the drums | Each trestle is one carry; the sling at rope height leaves no overturning moment; the lead suits a self-tailer |
| 9 | Air outlet | A duct outlet behind the hood | A 194 mm steel spigot in two saddles welded inside the crown at 40 degrees toward +Y; duct hung 265 mm off the pipe axis on magnet hangers every 2.5 m; crown jacking screws placed at 15 degrees to clear it | The layflat needs a rigid end, and the duct must leave a crawl space (554 mm clear circle) |
| 10 | Signal and light | Signal line and lamps | Cable on magnet hangers near the crown; magnetic lamp inside the hood | Nothing drilled into the pipe |
| 11 | Casualty sledge | Full-length sledge | Bought roll-up stretcher with a made 450 mm spreader bar and rope bridle; the swivels clip to its eye | See SVD-DDR-001, item 9 |
| 12 | Set-up | Not defined | Bottom segment first, taken in on a sledge by a crew member with both ropes paying out; the other three segments together on one shuttle trip | The sheave must be at the face before the shuttle can work; about 1.6 h in all |

## Consequences

- `cad/src/model.py` carries these changes; STEP and STL, drawings SVD-DWG-001 and 002 (Rev P2), the concept media and the build plan pictures are generated from it.
- The calculations in SVD-CAL-001 are on this design.
- `design_state: constructable` in `project.yaml`.
- Items that can only be settled with real parts (winch base pattern and power ratios, sheave bore and rating, swivel release load, pad friction) are listed under "To confirm when parts are bought" in SVD-DEC-001.
