---
doc_id: SVD-MKT-001
title: SleeveDrift market and viability
project: SleeveDrift
doc_type: Market and viability
version: "0.1"
status: Draft
date: 2026-11-02
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-02
    author: Amish Chadha
    change: First issue at the kit 1.9.1 upgrade; prices cited with the date checked, unknowns marked to assess
---

# SleeveDrift market and viability

The users are disaster-response forces and tunnel contractors that may have to dig by hand in a rescue pipe when a machine stops; they buy few kits, rarely, and spend on readiness rather than on volume, so a kit that costs about USD 10,800 in parts is a standby item, not a consumer product. Open design matters because no public design for this kit exists (SVD-PRB-001, Prior work), so forces and workshops in countries with tunnelling and collapse risk can build from the files.

> **Safety:** SleeveDrift is published as an open engineering reference, not certified rescue equipment. A force that holds a built kit trains with it and decides when to use it (SVD-REG-001).

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| National and state disaster-response forces | NDRF and state forces, India first (SVD-DDR-001 item 11); other forces in tunnelling countries | Nothing sold for pipe hand-mining. A vertical confined-space tripod with winch and 3-way SRL, the Frontline Megapod, lists at USD 4,245.35 (De Gemmill, checked 2026-11-02); it is a different function (top entry), not a substitute | 10,804 in parts for option A (bom/bom.csv); labour, transport, import and training to assess | A documented hood, haul and air kit that can be staged and built locally from stock parts |
| Tunnel contractors | Road, rail and hydropower tunnel projects in India, Europe and elsewhere | The cost of a stopped machine and a standby rescue plan is the real comparator; the price of an auger-boring rescue spread to assess | As above | Equipment held on site as part of emergency planning; the design is theirs to adapt |
| Mine rescue and technical-rescue teams | Mine rescue stations, fire-service technical rescue | Four-gas monitors cost GBP 776.52 excluding VAT for the Honeywell BW GasAlertMicroClip XL (Hazchem Safety, checked 2026-11-02); the kit's monitor line (BOM 25) is USD 550 each | Gas monitors 1,100 of the 10,804 | Parts that fit a rescue kit they already know (monitors, winches, rope) |
| Fabrication workshops and universities | Steel workshops near tunnel projects; engineering departments | Design files for rescue kits: none found for this function (to assess in a second search) | Made parts USD 1,637 of the 10,804, from the BOM (the lines marked make: 1 to 3, 5, 7 to 10, 15, 16, 27, 33) | Make the kit or teach from it; the build plan and drawings are open |

## Open route

Who would build it: a general steel workshop with plate rolls, near a tunnel programme or a rescue force's store (PR-014). How it spreads: through the co-design partner's own trials and training, through engineering departments that adopt it for teaching, and through rescue-equipment networks. What keeps it open: CERN-OHL-S-2.0 for the hardware, MIT for the scripts, and the safety notes in every document, so a copy carries the warnings with it.

## Viability

- **Demand:** one real incident (Silkyara, 2023) shows the need; the number of forces that would buy a kit is unknown (to assess with the partner).
- **Cost:** option A is about twice the value-engineering target (PR-013). The largest lines are the winches (USD 2,300), monitors (USD 1,100), signal line (USD 860), duct (USD 765) and blower (USD 750). No price has been checked against a second supplier; every unit cost in the BOM is a first-pass estimate to confirm when parts are bought.
- **Competition:** none found for the function; adjacent products are vertical retrieval systems and gas monitors.
- **Revenue:** the project does not sell kits. Any revenue (training, build services) is for builders and partners and is outside this repo.

## Sources

- De Gemmill, "Frontline Megapod Confined Space 7 ft Aluminum Tripod with 60 ft Winch and 3-Way SRL", https://degemmill.com/products/frontline-megapod-confined-space-7-ft-aluminum-tripod-with-60-ft-winch-and-3-way-srl, USD 4,245.35, accessed 2026-11-02.
- Hazchem Safety, "BW Gas Alert Micro Clip XL 4 Gas Detector (O2, LEL, CO, H2S)", https://www.hazchemsafety.com/product/bw-gas-alert-micro-clip-xl-4-gas-detector-o2-lel-co-h2s/, GBP 776.52 excluding VAT, accessed 2026-11-02.
- Silkyara reports and prior work: see SVD-PRB-001.
