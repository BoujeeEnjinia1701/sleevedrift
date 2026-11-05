---
doc_id: SVD-DDR-005
title: SleeveDrift concept selection
project: SleeveDrift
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-11-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-02'
  author: Amish Chadha
  change: Concept selection proposed at the kit 1.9.1 upgrade; A and B within 10 %, so both go to Amish
---

# 0005: Concept selection

- **Date:** 2026-11-02
- **Status:** proposed. **Proposed, awaiting Amish.** Nothing here is decided.

## Context

Before the kit 1.8 pipeline SleeveDrift had one design, the rope shuttle of sledges, which Amish's earlier decisions (SVD-DDR-001 items 2 to 4 and SVD-DDR-003) shaped. The pipeline asks for at least two options with different working principles, scored against the user requirements (SVD-URS-001). The two added options were screened by the STEM check (SVD-STM-001, rows O1 to O5) and modelled at D3 beside A (SVD-OPT-001). The current design is option A; it was not redesigned.

## Options considered

Scores out of 195 (SVD-OPT-001, Table 2):

- **A, rope shuttle of sledges:** 175. Sledges slide between a pull rope and a tail rope; two portal winches turned by drills. Strongest on fitting the pipe, set-up time and the casualty route; weakest on cost (USD 10,804.00 against 5,000) and rope wear.
- **B, rail tramway:** 164. Wheeled wagons on aluminium rails, same ropes and winches. Pull 162 N against 790 N, but 60 m of rail to lay in the pipe, long pieces to carry and a cost that is to assess.
- **C, pneumatic extraction:** 148. A 150 mm hose, cyclone and drum, with a 7.5 kW blower and a 12 mm lump limit after the STEM fix (SVD-DEC-001 D1). Cannot bring a casualty out; needs a generator; cost to assess.

A leads B by 6.3 %, inside the 10 % band, so both A and B are put to Amish. C is 15.4 % behind A.

Alternatives declined or set aside in earlier sessions were checked and not re-proposed: a circulating loop, the SiltHaul capstan, one long winding drum, bolting or welding to the pipe, radios and wired intercom, and the six-sledge variant of `docs/REVIEW.md` (a variant of A).

## Decision

**Proposed, awaiting Amish:** keep A as the baseline and decide between A and B. No pick is recommended between them because the scores are within 10 % and the scores are the author's judgments, not a co-design partner's. C is not recommended.

## Consequences

If Amish keeps A: nothing changes; PR-001 to PR-015 stand as written. If Amish picks B: PR-003, PR-004 and PR-007 change, the build plan, BOM and calculation note are redone for rails and wagons (a new TRL 3 pass), and the model already holds B at D3. If Amish picks C: the casualty route needs its own rope and winch and the portal needs generator power; not recommended. `CHOSEN` in `cad/src/model.py` stays "A", and `concept_chosen` in `project.yaml` reads "A (proposed)" until Amish decides.
