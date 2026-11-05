---
doc_id: SVD-FEA-001
title: SleeveDrift feasibility assessment
project: SleeveDrift
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: 2026-11-02
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-02
    author: Amish Chadha
    change: First issue at the kit 1.9.1 upgrade, for option A
---

# SleeveDrift feasibility assessment

Option A is feasible on paper and buildable by a general steel workshop; what stays uncertain is whether it holds up in a real collapse pipe (grit, rope wear, ring friction), which only trials at TRL 4 can show, and it costs about twice the value-engineering target. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Ten STEM claims are within known science, eleven are plausible and one (S17, the casualty rope factor of 6.5 against 15) fails with a fix proposed to Amish; every requirement is met on paper except cost (PR-013), with PR-009 managed by inspection | High | The margins that are thin: the haul rate (0.42 against 0.4 m3/h), the heaviest package (37.7 against 40 kg), the set-up time (1.6 against 2 h) | SVD-STM-001, SVD-CAL-001 |
| Materials | S355 plate and section, galvanised sheet, UHMW-PE runners, polyester rope, layflat duct; all stock materials | High | Pipe wall and weld beads at a real site may differ from the 780 mm bore assumed | SVD-CAL-001 A, BOM |
| Manufacturing and assembly | Rolled shell segments, flat-bar flanges, bent sheet sledges and welded SHS trestles; 153 made and bought parts in the detailed model; four segments go in one at a time on a sledge | Medium | Rolling 5 mm plate to a 760 mm ring and keeping the four segments to a 20 mm joint tolerance needs a workshop with plate rolls | SVD-BLD-001, cad/fidelity.json |
| Power and controls | Nothing powered in the pipe; battery drills and a 230 V blower at the portal; two sound-powered telephones | High | Portal power may be a generator; clutches are set at the portal | PR-008, SVD-CAL-001 D, F |
| Supply of parts | Winches, drills, sheave, monitors, blower and duct are catalogue items; the one long-lead item is the bought roll-up stretcher | Medium | Prices are first-pass estimates from Amish's earlier sessions; two lines (the signal line at USD 860, the winches at USD 2,300) are the least tested | BOM |
| Cost | USD 10,804.00 of parts against the USD 5,000 target (PR-013) | Low | A kit for rescue is not a consumer product; the target is a control figure (SVD-DDR-001 item 13). Proposed, awaiting Amish: hold it or restate it | BOM, SVD-CAL-001 J |
| Safety case | Overload limit, hood, gas monitoring and guards are designed in | Medium | Hazards that remain: face collapse, rope whip, drill torque on the winch, entrapment (SVD-RSK-001); none is closed by tests yet | SVD-RSK-001, SVD-CAL-001 |
| Regulatory | Published as a reference, so none to meet; operators meet confined-space rules | Medium | Rope marking (NFPA 1983 practice) and flammable-atmosphere use to assess | SVD-REG-001 |
| Concept options | A scored 175 of 195, B 164 and C 148; A and B are within 10 % | Medium | Both go to Amish; the choice is open | SVD-OPT-001 |

Ratings: High, Medium, Low.
