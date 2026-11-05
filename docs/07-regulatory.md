---
doc_id: SVD-REG-001
title: SleeveDrift regulatory and standards register
project: SleeveDrift
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: 2026-11-02
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-02
    author: Amish Chadha
    change: First issue at the kit 1.9.1 upgrade; confined-space, rope, gas, machinery and risk standards that touch a rescue kit; not legal advice
---

# SleeveDrift regulatory and standards register

SleeveDrift is published as an open engineering reference, not as certified rescue, mining or confined-space equipment, so no certification is needed to publish the design. The register lists what a team that builds, stages or uses a kit would meet, so the design can be shaped for it. The rules on the people who enter a pipe (permits, rescue plans, training) fall on the operator, not on the design. Not legal advice; anything marked "to assess" needs a qualified reviewer, and the use of the kit in a specific country needs the local authority's view before any claim.

> **Safety:** Digging by hand in a rescue pipe is confined-space work. Meeting a row below on paper does not make the kit safe to use. Nothing here replaces an incident commander, a standby crew at the portal and continuous gas monitoring.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | 29 CFR 1910.146, Permit-required confined spaces (OSHA) | United States | Permit programme, atmospheric testing, attendants, rescue and retrieval for entry into confined spaces | The pipe under collapse debris is a confined space. The kit supplies retrieval (casualty line, stretcher), air and gas monitoring that a permit programme would require; the permit and the rescue service are the operator's | Operator and incident commander | Applies to the operator; the kit supports it (SVD-CAL-001 E, F; PR-006, PR-005, PR-012) |
| G2 | 29 CFR 1926 Subpart AA, Confined spaces in construction (OSHA) | United States | The same duties for construction sites, which include tunnel works | Tunnel contractors who hold a kit would work under it. Section numbers and the retrieval rules to read against the kit | Tunnel contractor | To assess |
| G3 | NFPA 1670, Technical rescue operations (NFPA) | International practice, US origin | Levels of rescue capability, including confined-space rescue | Sets what a rescue team should be trained for before it uses a kit in a pipe; no equipment claim | Rescue commander | To assess |
| G4 | Gas detection: portable four-gas monitors for oxygen, carbon monoxide, hydrogen sulphide and flammable gas | International practice | Atmospheric monitoring in confined spaces | The kit carries two bought monitors (BOM line 25); an example product is the Honeywell BW GasAlertMicroClip XL, GBP 776.52 excluding VAT, checked 2026-11-02 (Sources). Bump testing before each shift is a use rule | Rescue commander | Met by design (PR-012); the monitor choice, calibration and the area classification of a collapse atmosphere to assess |
| G5 | ISO 12100:2010 (EN ISO 12100:2010), Safety of machinery, General principles for design, Risk assessment and risk reduction | International; Europe | The method for hazard analysis and risk reduction on machinery | The portal winches with drill drive are machinery in the sense of the standard. SVD-RSK-001 follows its hazard method in a preliminary form | Design lead | Applies as method; not a certification |
| G6 | NFPA 1983 (consolidated into NFPA 2500 on 2021-09-15), Life safety rope and equipment for emergency services | United States | Design, test and labelling of rope and hardware for life-safety use, with a 15:1 rope factor | The pull rope also carries a casualty, so life-safety practice is the benchmark. 15 x the 519 N starting pull is 7.8 kN against 16.2 kN of rope after the splice (STEM S17). The bought 10 mm polyester rope is not marked to the standard; choosing a marked rope is a to-assess item | Procurement | To assess (rope marking); the factor is met on paper |
| G7 | Directive 2006/42/EC, Machinery, and Regulation (EU) 2023/1230, which replaces it and applies from 2027-01-20 | European Union | Essential health and safety requirements, CE marking for machinery put on the market | Applies only to someone who sells a made kit in the EU. The open design is not a product on the market. The drill-driven winch would be an assembly of machinery to assess | Manufacturer, if any | Does not apply to the design; to assess for any builder who sells |
| G8 | ATEX Directive 2014/34/EU and IEC 60079 series, Equipment for explosive atmospheres | European Union; international | Equipment in atmospheres with flammable gas or dust | Battery drills, the blower and the lamps stay at the portal or are battery devices; whether any item may go where methane or dust is present is a question for the operator's gas assessment | Operator | To assess; not claimed |
| G9 | Indian mines and disaster-response guidance for tunnel rescue (NDMA, DGMS) | India | Rescue practice, equipment holdings and mine safety in the first co-design country | The first co-design candidate is India's National Disaster Response Force (SVD-DDR-001 item 11, not agreed); which guidance governs a tunnel rescue kit to confirm with them | Co-design partner | To assess |
| G10 | CERN-OHL-S-2.0 and MIT licences | International | Terms for the open hardware and the scripts | The repo's licences; the kit's liability disclaimers are in the safety notes | Maintainer | Applies |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Notes

- The only figures taken from the standards are the 15:1 rope factor (G6) and the existence of the confined-space duties (G1, G2). Section numbers, limits and classifications that were not read at source are not quoted; they are marked to assess.
- Standards shared across the tunnel-rescue focus area are researched once; HatchSide (air and gas practice, SVD-DDR-001 item 12) is the reference and is not edited here.

## Sources

- OSHA, "Permit Required Confined Spaces, Notice of proposed rulemaking" (59 FR 60735, Docket S-019A), https://www.osha.gov/node/16671, accessed 2026-11-02. Establishes 29 CFR 1910.146 and its rescue paragraph (k); the final text of the standard is to be read at source.
- FireRescue1, "NFPA 1983: Where did it come from and what does it mean?", https://www.firerescue1.com/fire-products/technical-rescue/nfpa-1983-where-did-it-come-from-and-what-does-it-mean, accessed 2026-11-02 (15:1 rope factor, consolidation into NFPA 2500 on 2021-09-15).
- European Agency for Safety and Health at Work, "Regulation (EU) 2023/1230 on machinery", https://osha.europa.eu/en/legislation/directive/regulation-20231230eu-machinery, accessed 2026-11-02 (applies from 2027-01-20; replaces Directive 2006/42/EC).
- Estonian Centre for Standardisation and Accreditation, EVS-EN ISO 12100:2010 catalogue entry, https://www.evs.ee/en/evs-en-iso-12100-2010, accessed 2026-11-02.
- Hazchem Safety, "BW Gas Alert Micro Clip XL 4 Gas Detector (O2, LEL, CO, H2S)", https://www.hazchemsafety.com/product/bw-gas-alert-micro-clip-xl-4-gas-detector-o2-lel-co-h2s/, accessed 2026-11-02 (GBP 776.52 excluding VAT).
- NFPA 1670, 29 CFR 1926 Subpart AA, ATEX 2014/34/EU, IEC 60079 and the Indian guidance (G2, G3, G8, G9) are named from general knowledge and not read at source in this session: to assess.
