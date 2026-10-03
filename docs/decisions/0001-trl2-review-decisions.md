---
doc_id: SVD-DDR-001
title: SleeveDrift TRL 2 review decisions
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
  change: TRL 2 review items decided under Amish's pre-approvals of 2026-10-03
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** accepted

## Context

The TRL 2 review (`docs/REVIEW.md`, TRL 2 section) raised the items below. On 2026-10-03 Amish wrote: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." and then: "Proceed with the remaining 15 scaffolds", under the same pre-approval. Every recommendation is therefore decided as recommended. Choices that touch safety take the conservative option, with the evidence that would relax them stated. Partners and regions are the first candidates to approach, not agreements.

> **Safety:** Several items below set SleeveDrift's safety case for people working inside a rescue pipe (overload limit, gas monitoring, air, casualty evacuation, the fixing of the ring). Each took the conservative option.

## Options considered

Table 1 lists the options for each item and the one chosen.

## Decision

*Table 1. Items decided on 2026-10-03 under Amish's pre-approvals.*

| # | Item | Options | Decision | What would relax a safety choice |
| --- | --- | --- | --- | --- |
| 1 | Pipe for the design case | (a) 800 mm nominal of unknown wall; (b) 800 x 10 mm steel, 780 mm bore, as at Silkyara | (b), with the bore and weld beads confirmed at the fit trial | Not a safety choice |
| 2 | Fixing the ring in the pipe | (a) bolts through holes drilled in the pipe; (b) welding; (c) jacking screws with swivel pads | (c), conservative: no drilling, welding or power at the face, and the ring can be taken out | Pull-out tests on representative pipe showing a friction above 0.20 would allow lower preloads |
| 3 | Haul layout | (a) circulating loop with sledges going out on one leg and back on the other; (b) a shuttle train between a pull rope and a tail rope | (b): two lanes of sledges do not fit with a crew in a 780 mm bore | Not a safety choice |
| 4 | Portal drive | (a) the SiltHaul hand capstan; (b) one long winding drum; (c) two two-speed self-tailing winches, one per rope | (c): each holds its own load on its pawls, takes any rope length, and lets the crew hand-haul through the drum | Not relaxed |
| 5 | Overload | (a) size everything on what a person can heave on a winch handle (over 13 kN); (b) breakaway swivels at both ends of the train, 2.5 kN | (b), conservative: R11 added; every part sized on 2.5 kN | Release tests on a batch of pins with a tight scatter could raise the working pull, never the limit |
| 6 | Gas monitoring | (a) left to the rescue service; (b) two four-gas monitors in the kit, worn at the face and the portal | (b), conservative: R12 added | None proposed |
| 7 | Air | (a) exhaust from the face; (b) forcing fresh air to the face through 200 mm layflat, sized well above R5 | (b): about 15 m³/min at the face against R5's 1 m³/min; blower intake in clean air | Confined-space guidance accepted by the partner could set a lower flow; never below R5 |
| 8 | Signals | (a) radios; (b) wired intercom; (c) sound-powered telephones with a pull-cord bell as backup | (c): no batteries in the pipe (R8) and a second, mechanical channel | Not relaxed |
| 9 | Casualty stretcher | (a) a made full-length sledge; (b) a bought roll-up confined-space stretcher with a made towing spreader bar | (b), conservative: a recognised rescue item with straps | None proposed |
| 10 | Casualty haul | (a) crank winch A; (b) three people hauling hand over hand through winch A, which holds when let go | (b): about 3.5 min for 60 m against 8.3 min cranked | Not a safety choice |
| 11 | Co-design partner | National force, state force, tunnelling contractor | First candidate to approach: India's National Disaster Response Force with the Jhansi hand miners who worked at Silkyara (not agreed) | |
| 12 | Shared blocks | SiltHaul capstan; CalRig; HatchSide air practice | SiltHaul's capstan is not used (item 4); CalRig is the first candidate rig for the hood test and proof loads; HatchSide is the first reference for air and gas rules. Sibling repos are not edited here | |
| 13 | Budget | Keep `budget_usd` at 5,000 | Kept; it is a value-engineering target, not a limit | |

## Consequences

- R11 (overload limit) and R12 (air monitoring) are added to SVD-REQ-001.
- The design for construction (SVD-DDR-002) works from these choices.
- R3, R9 and the 600 mm stretch of R1 are not met or at risk on paper; they are not decided here but put to Amish as decisions with options in `docs/REVIEW.md` and SVD-DEC-001.
