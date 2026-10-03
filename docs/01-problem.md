---
doc_id: SVD-PRB-001
title: SleeveDrift problem statement
project: SleeveDrift
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2 and 3 update; safety note, first co-design candidate, answers to the open questions and questions for the first trials
---

# SleeveDrift problem statement

Pipe-based rescue through collapse debris depends on machines. When the machine stops, the fallback is people digging by hand inside the pipe, with whatever tools are on site.

> **Safety:** Digging by hand inside a rescue pipe under collapse debris is confined-space work with risks of face collapse, falling material, asphyxiation, heat stress and entrapment by moving ropes. SleeveDrift is published as an open engineering reference, not certified rescue, mining or confined-space equipment. It is used only under an incident commander, with a standby crew at the portal, continuous gas monitoring and a way to pull each person out.

## The problem

At Silkyara, the crews inside the pipe wore helmets, masks and glasses and used shovels ([Tribune, 2023](https://www.tribuneindia.com/news/india/silkyara-tunnel-collapse-parts-of-auger-machine-removed-from-rubble-566395)), carried a blower for air ([NewsBytes, 2023](https://www.newsbytesapp.com/news/india/uttarkashi-what-is-rat-hole-mining-used-in-collapsed-silkyara-tunnel/story)) and cut through stones and girders ([Global Kashmir, 2023](https://globalkashmir.net/manual-drilling-at-silkyara-tunnel-on-uttarakhand-cm-says-pipes-inserted-up-to-52-metres/)). Three people worked inside at a time in eight-hour shifts ([The News Minute, 2023](https://www.thenewsminute.com/news/explained-the-rat-hole-mining-technique-used-to-rescue-workers-in-uttarakhand-tunnel)). The equipment was assembled on site, and there is no public design for protecting the digger at the face, moving spoil the length of the pipe or keeping the air fresh at the working end.

The standard approach, auger boring, pushes pipe with a machine and failed at Silkyara when it hit obstructions ([Wikipedia](https://en.wikipedia.org/wiki/Uttarakhand_tunnel_rescue)). Rat-hole mining supplies the skill but no equipment, and it is banned for its original purpose because of its dangers, including asphyxiation ([The News Minute, 2023](https://www.thenewsminute.com/news/explained-the-rat-hole-mining-technique-used-to-rescue-workers-in-uttarakhand-tunnel)).

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Hand-mining rescue crews | Dig at the face with head protection, clear spoil quickly and breathe fresh air | Crawling or kneeling inside an 800 mm pipe tens of metres long |
| Portal crews | Haul spoil out and send tools and supplies in without entering the pipe | At the pipe mouth inside the tunnel |
| Rescue commanders (national and state disaster response forces, project engineers) | A kit that can be staged at site and deployed in hours | Multi-agency rescue with machines and hand crews |
| Tunnel contractors | Equipment to hold on site as part of emergency planning | Road, rail and hydropower tunnel projects |

## Operating environment

- Inside steel pipe of 800 mm nominal diameter, possibly 600 mm (target range), up to about 60 m (197 ft) long, horizontal or on a slight grade.
- Face made of soil, rock fragments, steel ribs, mesh and concrete debris that can run or collapse.
- Dust, heat, humidity and limited light; air quality can fall quickly with several people inside.
- Work in continuous shifts over days.
- Power may be available at the portal, but equipment inside the pipe should work without it.

## Constraints

- Prototype budget ceiling USD 5,000 for all prototypes and test rigs.
- Every item must pass through an 800 mm pipe and be assembled inside it.
- No part inside the pipe needs electric power; the blower sits at the portal.
- Avoid proprietary steering joints and articulated shield geometry (IP screen design-around).
- Uses commodity rope, pulleys, ducting and steel section where possible.
- Open hardware under CERN-OHL-S-2.0.

## Out of scope

- Auger boring machines and pipe-pushing equipment.
- Steering or guiding the pipe.
- Vertical shafts and drilling.
- Medical care of trapped people beyond evacuation through the pipe.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Silkyara improvised hand-mining method (2023) | Three-person team inside an 800 mm pipe: one digs, one collects, one loads a trolley that is pulled out | Improvised on site; no documented face protection, haul system or air delivery design | [link](https://globalkashmir.net/manual-drilling-at-silkyara-tunnel-on-uttarakhand-cm-says-pipes-inserted-up-to-52-metres/) |
| Auger boring at Silkyara | Machine pushes steel pipe through collapse debris | Broke and jammed on obstructions after about 47 m | [link](https://en.wikipedia.org/wiki/Uttarakhand_tunnel_rescue) |
| Rat-hole mining (Meghalaya) | Manual digging of narrow tunnels just wide enough for one person | A skill, not equipment; banned in 2014 because of its dangers | [link](https://www.thenewsminute.com/news/explained-the-rat-hole-mining-technique-used-to-rescue-workers-in-uttarakhand-tunnel) |
| Oxygen, food and camera pipes at Silkyara | Separate small pipes for air, food and an endoscopic camera to the trapped workers | Serves the trapped workers, not the crew digging in the escape pipe | [link](https://en.wikipedia.org/wiki/Uttarakhand_tunnel_rescue) |

## Co-design

A national or state disaster response force or tunnelling contractor's rescue team, together with experienced hand miners, so the kit is shaped by the people who would crawl into the pipe and by those who would stage it at site. The first candidate to approach is India's National Disaster Response Force, with the Jhansi hand miners who worked at Silkyara (recorded in SVD-DDR-001; not agreed).

- [ ] Confirm the pipe sizes held for rescue (800 mm and 900 mm, wall thickness) and how the pipe end is left at the portal.
- [ ] Walk through the three-person method at the face with experienced hand miners.
- [ ] Agree the signal code and the stop rules for hauling while people are in the pipe.
- [ ] Agree where the kit is held and who trains with it.

## Open questions

The TRL 3 work answered the first three questions on paper (SVD-PRC-001 and SVD-CAL-001):

- **How should the hooded ring attach to the lead pipe?** It is four bolted segments, carried in one at a time on a sledge and assembled in the pipe mouth, held by four jacking screws that press swivel pads on the pipe wall. Nothing is drilled or welded to the pipe and nothing needs power.
- **What air flow and monitoring are needed?** A 200 mm blower at the portal delivers about 15 m³/min (530 ft³/min) at the face through 65 m of layflat duct, about 5 m³/min a person; two four-gas monitors (one at the face, one at the portal) are part of the kit.
- **Can the rope run on the pipe floor?** The train of sledges runs on the floor along the centre and the return leg lies on the floor beside it; runner wear is small, but rope abrasion over a 72-hour shift is the open risk (SVD-CAL-001, section H).

Questions for the first trials and for the co-design partner:

- Where should the kit be held (national stores, contractors, or both) so it arrives within hours?
- How can hand-mining skills be kept alive and trained legally now that rat-hole mining is banned?
- How fast does a trained crew actually load and empty the sledges, and how fast does the face produce spoil?
