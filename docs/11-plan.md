---
doc_id: SVD-PLN-001
title: SleeveDrift project plan
project: SleeveDrift
doc_type: Project plan
version: "0.1"
status: Draft
date: 2026-11-02
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-02
    author: Amish Chadha
    change: First issue at the kit 1.9.1 upgrade; stage P3 reached, P4 to P6 on hold under the stage cap
---

# SleeveDrift project plan

SleeveDrift is at stage P3 (TRL 3, a constructable design with a detailed model of every concept option). The next gate is Amish's choice between options A and B (SVD-OPT-001, within 10 % on score) and his answer on the cost target (PR-013); after that the work is hands-on and waits for the portfolio's TRL cap to lift. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem and users | Project lead | SVD-PRB-001, SVD-URS-001 | Done at P3 |
| STEM check and calculations | Design lead | SVD-STM-001, SVD-CAL-001 (sizing.py, stem_check.py) | Done; independent review recorded |
| Concept options and selection | Design lead | SVD-OPT-001, SVD-DDR-005 | Done; decision awaiting Amish |
| Requirements and traceability | Design lead | SVD-PRS-001, SVD-RTM-001 (generated) | Done |
| Detailed CAD of every option | CAD lead | cad/src/model.py, cad/fidelity.json, STEP, drawings | Done at D3 |
| Build plan | Design lead | SVD-BLD-001 and its pictures | Done (paper) |
| Regulatory, feasibility, risk, market | Project lead | SVD-REG-001, SVD-FEA-001, SVD-RSK-001, SVD-MKT-001 | First issue |
| Co-design partner | Project lead | An agreed partner and review of the user requirements | Not started; NDRF first (not agreed) |
| Hardware build and trials | Test lead | Prototype, fit trial, load tests, timed trials | On hold (P4 to P6 under the stage cap) |

## Resources needed

Table 2. Resources.

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Co-design partner time | Review of URS and PRS; site pipe data | A few days | to assess |
| Steel workshop with plate rolls | Prototype ring, sledges, trestles (made parts) | About 3 weeks | 1,637 in parts for the made lines; labour to assess |
| Bought items | Winches, drills, monitors, blower, duct, ropes | One order | 9,167 (the rest of the BOM), first-pass prices |
| CalRig or equivalent | Hood and ring proof loads | Days | to assess |
| Pipe test section, 800 x 10 mm | Fit, ring friction and haul trials | 12 m or more | to assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 to P2 | Problem, concept, first calculations | Done (TRL 2, 2026-10-03) |
| P3 | Constructable design, detailed model of every option, STEM check, options, requirements traced, build plan | Reached; awaiting Amish on the concept choice |
| P4 | Prototype built; fit trial, ring friction, hood load, haul and set-up timed | On hold (stage cap) |
| P5 | Endurance and field trial with a partner | On hold |
| P6 | Release candidate; certification routes assessed | On hold |

## Next steps and decision requested

1. **Decision for Amish:** the concept (SVD-DDR-005). Option A scores 175 of 195, B 164 and C 148; A and B are within 10 %, so both are put to Amish without a pick. A is the current design and the baseline.
2. **Decision for Amish:** hold or restate the USD 5,000 cost target (PR-013); the parts cost is USD 10,804.00 (SVD-DEC-001 open decision 2).
3. **Decision for Amish:** the jacking screw length, M20 x 60 as modelled or the 90 mm in the BOM (SVD-DEC-001 open decision 3).
4. Approach the first co-design partner (SVD-PRB-001, Co-design) once the choice is made.
5. When the cap lifts: TRL 4 starts with the pull-out test of the ring, the swivel release batch, the sled test and the 12 m fit trial (the highest RPNs in SVD-RSK-001).

## References

- OSHA, "Permit Required Confined Spaces", 59 FR 60735, https://www.osha.gov/node/16671, accessed 2026-11-02.
- FireRescue1, "NFPA 1983: Where did it come from and what does it mean?", https://www.firerescue1.com/fire-products/technical-rescue/nfpa-1983-where-did-it-come-from-and-what-does-it-mean, accessed 2026-11-02.
- European Agency for Safety and Health at Work, "Regulation (EU) 2023/1230 on machinery", https://osha.europa.eu/en/legislation/directive/regulation-20231230eu-machinery, accessed 2026-11-02.
- De Gemmill, "Frontline Megapod ...", https://degemmill.com/products/frontline-megapod-confined-space-7-ft-aluminum-tripod-with-60-ft-winch-and-3-way-srl, accessed 2026-11-02.
- Hazchem Safety, "BW Gas Alert Micro Clip XL 4 Gas Detector", https://www.hazchemsafety.com/product/bw-gas-alert-micro-clip-xl-4-gas-detector-o2-lel-co-h2s/, accessed 2026-11-02.
- Silkyara sources: see SVD-PRB-001.
