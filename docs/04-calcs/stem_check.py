"""SleeveDrift STEM check calculations (SVD-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. These are first-order screens of each claim made for option A (the
rope shuttle of sledges). The sizing itself is in the calculation note (SVD-CAL-001, docs/04-calcs/sizing.py),
which this script imports (it builds the model, about a minute) to close the rows that need the TRL 3 design.
Rows O1, O2, O4 and O5 screen the working principles of options B (rail tramway) and C (pneumatic extraction).
"""
import math
import sys

sys.path.insert(0, ".kit")
from stem_check import Check, G, WITHIN, PLAUSIBLE, FIX  # noqa: E402,F401

sys.path.insert(0, "docs/04-calcs")
import sizing as CAL  # noqa: E402  SVD-CAL-001, reads cad/src/model.py

P, A, D = CAL.P, CAL.A, CAL.D
c = Check()


def plaus(sid, note):
    """Independent review: the arithmetic stands but an input is an assumption, so the verdict is Plausible, not Within."""
    row = next(r for r in c.rows if r["id"] == sid)
    row["verdict"] = PLAUSIBLE
    row["closed_by"] = (row["closed_by"] + "; " if row["closed_by"] else "") + note



# ---------------------------------------------------------------- Physics: hood (R2 / PR-002)
# Independent recomputation: crown section as a cantilever from the pipe mouth, 5 kN spread over the 500 mm that
# stands beyond the mouth (SVD-CAL-001 B2). Section properties are taken from the model, not retyped.
w_line = 5000.0 / 500.0                      # N/mm
c.claim("S1", "The hood's crown carries 5 kN spread over its 500 mm cantilever below the 355 MPa yield of S355 with a factor of 1.5",
        "Physics", "Strength of materials", "Cantilever bending, sigma = M c / I; S355 yield 355 MPa (EN 10025-2, minimum for t up to 16 mm)",
        round(CAL.sig / 1e6, 2), 355.0 / 1.5, "MPa", closed_by="SVD-CAL-001 B2")
d_hood = w_line * 500.0 ** 4 / (8 * 205000.0 * CAL.I)       # mm, uniform load on a cantilever
c.claim("S2", "The hood tip deflects less than 0.1 mm at 5 kN, so no contact with a head form", "Physics", "Strength of materials",
        "Cantilever with uniform load, d = w L^4 / (8 E I); E = 205 GPa", round(d_hood, 4), 0.1, "mm", closed_by="SVD-CAL-001 B2, B4")

# Independent review: the free tip of the hood is an open arch whose ends can spread, so also screen it as a flat strip across its chord
chord = 2 * (P["ring_od"] / 2) * math.sin(math.radians(60))        # 120 degree crown, chord in mm
p_hood = 5000.0 / (500.0 * chord)                                    # N/mm2 over 500 mm x chord
sig_strip = (p_hood * chord ** 2 / 8) / (P["shell_t"] ** 2 / 6)     # per mm width, simply supported strip
c.claim("S1b", "The hood tip, taken as a flat strip across its 658 mm chord with no arch action, stays below yield with a factor of 1.5", "Physics",
        "Strength of materials", "Simply supported strip, sigma = (p c^2 / 8) / (t^2 / 6); conservative because the rolled crown carries part of the load as an arch",
        round(sig_strip, 0), round(355.0 / 1.5, 0), "MPa", margin=0.25, closed_by="SVD-CAL-001 B3 (membrane result); shell finite-element check or load test on CalRig at TRL 4")

# ---------------------------------------------------------------- Physics: haul forces and the overload limit
est_load = A["mu_k"] * (D["sledge_L"] * P["n_sledges"] * A["rho_spoil"] + CAL.M["sledge"] * P["n_sledges"] + 3.0) * G
c.order_of_magnitude("S3", "Dragging the loaded train takes about 790 N at the rope (sledge friction plus rope on the floor)", "Physics", "Mechanics and statics",
                     claimed=CAL.F_load, estimate=est_load + CAL.F_rope + CAL.F_back, unit="N",
                     law="Coulomb friction: F = mu_k m g for the sledges plus the drag of the rope on the floor and the sheave back tension",
                     closed_by="SVD-CAL-001 C3")
c.claim("S4", "A person turning the winch handle in high gear needs less than 200 N to start the loaded train", "Physics", "Mechanics and statics",
        "Winch power ratio and efficiency: handle force = rope force / (power ratio x efficiency); starting friction mu_s",
        round(CAL.h(CAL.F_start, A["pr_high"]), 1), 200.0, "N", closed_by="SVD-CAL-001 C4")
c.claim("S5", "The 18 kN rope keeps a factor of 5 or more on the 2.5 kN release load after a 90 % splice (factor 5.04 at 70 %)", "Physics", "Strength of materials",
        "Rope breaking strength x splice efficiency / release load; factor 5 is working-line practice, not a cited standard (to confirm with the partner)",
        round(CAL.fos_rope, 2), 5.0, "factor", rule="above", closed_by="SVD-CAL-001 C6")
c.claim("S6", "The drill's slip clutch (35 N m) slips below the 2.5 kN swivel release in high gear", "Physics", "Mechanics and statics",
        "Rope force = clutch torque x power ratio x efficiency / drum radius; in low gear the same clutch would pass 4.8 kN, so the drill is used in high gear only",
        round(CAL.F_slip_hi / 1000, 2), A["breakaway"] / 1000, "kN", closed_by="SVD-CAL-001 D6")
c.claim("S7", "Friction at the jacking pads holds the ring against twice the 2.5 kN release load with a factor of 1.5", "Physics", "Mechanics and statics",
        "Coulomb friction, F = mu N; the pad-to-pipe friction coefficient of 0.2 is an assumption for rusty or painted steel",
        round(1.5 * CAL.Fs / 1000, 2), round(CAL.Ff / 1000, 2), "kN", closed_by="SVD-CAL-001 C8; friction coefficient to measure on CalRig at TRL 4", margin=0.1)
plaus("S7", "the friction coefficient 0.20 and the screw preload from a torque coefficient are assumptions (independent review)")

# ---------------------------------------------------------------- Physics: air (R5 / PR-005)
c.claim("S8", "A 200 mm layflat duct passes 0.27 m3/s over 65 m with less than 600 Pa of loss, a pressure a 200 mm axial or mixed-flow portal blower can give",
        "Physics", "Fluid mechanics", "Darcy-Weisbach, dp = (f L / D + K) rho v^2 / 2, f = 0.030, K = 2.1 (SVD-CAL-001 F1)",
        round(CAL.dp, 0), 600.0, "Pa", closed_by="SVD-CAL-001 F1, F2; blower curve to confirm with the blower bought")
plaus("S8", "no named blower curve yet: a 200 mm axial unit must pass 0.27 m3/s at about 570 Pa total (independent review)")

# ---------------------------------------------------------------- Mathematics: output, time, mass
c.claim("S9", "A right-angle drill on each portal winch moves loose spoil at least 0.4 m3/h, faster than a hand-dug face makes it", "Mathematics", "Rates and cycle times",
        "Cycle arithmetic: volume per trip / (out + unload + in + load + signals); drill speed from rpm and drum diameter",
        round(CAL.q_b, 3), 0.4, "m3/h", rule="above", margin=0.1, closed_by="SVD-CAL-001 D4 (restated 2026-10-04, SVD-DDR-004)")
c.claim("S10", "Three people bring a 100 kg casualty out 60 m in under 5 minutes, hand over hand", "Mathematics", "Rates and cycle times",
        "Time = distance / speed (0.4 m/s hand over hand, ergonomics range) plus one minute to clip on", round(CAL.tc, 2), 5.0, "min", closed_by="SVD-CAL-001 E2")
plaus("S10", "the 0.4 m/s hand-over-hand speed is an assumption; below 0.25 m/s the 5 min target fails; timed drill at TRL 4 (independent review)")
c.claim("S11", "The kit goes up in less than 2 hours", "Mathematics", "Rates and cycle times",
        "Sum of the critical-path steps in SVD-CAL-001 G1; step times are estimates to measure in a drill at TRL 4", round(CAL.tot / 60, 2), 2.0, "h",
        margin=0.25, closed_by="SVD-CAL-001 G1, G2")
c.claim("S12", "The heaviest package weighs less than 40 kg", "Mathematics", "Units and dimensional analysis",
        "Sum of component masses from the model (cad/src/model.py masses())", round(CAL.heavy[1], 1), 40.0, "kg", margin=0.1, closed_by="SVD-CAL-001 I2; the case itself is not counted")

# ---------------------------------------------------------------- Biology and chemistry
CO2_PEL = 0.005                               # 5,000 ppm, OSHA 29 CFR 1910.1000 Table Z-1 (8 h)
vco2 = 1.5e-3 / 60 * 1000                     # L/s per person at heavy work (about 1.5 L/min, physiology texts)
q_min = A["people"] * vco2 / 1000 / (CO2_PEL - 0.0004)       # m3/s of fresh air to hold CO2 below 5,000 ppm
c.claim("S13", "5 m3/min of fresh air per person is far more than needed to keep CO2 below 5,000 ppm", "Biology", "Human physiology",
        "Dilution: Q = n x CO2 production / (limit - inlet); heavy work 1.5 L/min CO2 per person (physiology texts, to cite), inlet 400 ppm",
        round(q_min * 60, 2), round(CAL.Qf, 1), "m3/min", closed_by="SVD-CAL-001 F2; heat and dust, not CO2, govern the airflow (SVD-CAL-001 F4)")
c.cited("S14", "Four-gas monitors measure oxygen, carbon monoxide, hydrogen sulphide and flammable gas and alarm", "Chemistry", "Analytical chemistry and gas sensing",
        "Electrochemical cells for O2, CO and H2S and a catalytic bead or infrared cell for combustible gas are standard in portable four-gas monitors (Honeywell BW GasAlertMicroClip XL, listed at GBP 776.52 excluding VAT, checked 2026-11-02)",
        "Commercial monitors exist; fitness for a collapse atmosphere (dust, humidity, calibration) to confirm with the rescue service", WITHIN, "SVD-REG-001 G4")
c.cited("S15", "Rope abrasion over 72 hours of hauling does not part the pull or tail rope", "Engineering and technology", "Standards practice",
        "Polyester double braid dragged over a gritty steel floor: wear per kilometre is not predictable on paper; managed by a wear gauge each shift and a spare set (SVD-DDR-003 decision 25A)",
        "About 250 round trips at the drill rate (SVD-CAL-001 H1); an endurance trial decides whether a tougher rope is needed", PLAUSIBLE)
c.cited("S16", "UHMW-PE runners slide on the pipe floor with a friction coefficient of 0.30 sliding and 0.40 starting", "Physics", "Mechanics and statics",
        "UHMW-PE on dry steel is low friction (about 0.1 to 0.2 clean); grit, wet clay and rust raise it, so 0.30 and 0.40 are conservative assumptions",
        "Not measurable on paper; sled test with pipe-floor debris at TRL 4", PLAUSIBLE)

fos_release = P["rope_mbs"] * A["splice"] / A["breakaway"]
c.cited("S17", "The pull rope can carry a casualty with the 15:1 factor that life-safety rope practice uses (NFPA 1983, FireRescue1 summary)", "Physics", "Strength of materials",
        "Breaking strength x splice efficiency against 15 x the largest load the rope can see, which is the 2.5 kN swivel release, not the starting pull; NFPA 1983 (now in NFPA 2500) is a manufacturer standard and the 15:1 factor is a cited practice, not a requirement on this kit",
        f"Factor {fos_release:.1f} on the 2.5 kN release (15 x 2.5 = 37.5 kN against {P['rope_mbs'] * A['splice'] / 1000:.1f} kN); {P['rope_mbs'] * A['splice'] / 1000:.1f} kN is {P['rope_mbs'] * A['splice'] / (15 * CAL.Fc0):.1f} times the {15 * CAL.Fc0 / 1000:.1f} kN that 15 x the starting pull of {CAL.Fc0:.0f} N would need",
        FIX, "Proposed, awaiting Amish (SVD-DEC-001 open decision 4): a stretcher-only breakaway at 1.0 kN would give a factor of 16 on the rope; it changes the overload limit Amish decided, so it is not implemented")

# ---------------------------------------------------------------- Options B and C: working principle screens
# Option B: wheeled wagons on rails. Rail section modulus from the 40 x 40 mm aluminium T (foot 40 x 4, web 4, head 32 x 8).
parts = [(40.0, 4.0, 2.0), (4.0, 28.0, 18.0), (32.0, 8.0, 36.0)]       # (b, h, centroid height)
a_t = sum(b * h for b, h, _ in parts)
yc = sum(b * h * y for b, h, y in parts) / a_t
i_t = sum(b * h ** 3 / 12 + b * h * (y - yc) ** 2 for b, h, y in parts)
z_top = i_t / (40.0 - yc)
z_bot = i_t / yc
wheel_N = (D["sledge_L"] * 1.0 * A["rho_spoil"] + 40.0) * G / 4         # one wagon, one wheel: spoil of one 30 L tray plus 40 kg of wagon
m_rail = wheel_N * 1000.0 / 4                                          # N mm, simply supported over 1 m of sleeper spacing
c.claim("O1", "Option B: a 40 x 40 x 4 mm aluminium T rail on sleepers 1 m apart carries a loaded wagon wheel below 6061-T6 yield with a factor of 3", "Physics",
        "Strength of materials", "Simply supported beam, M = P L / 4; sigma = M / Z; 6061-T6 yield 240 MPa (minimum, to confirm for the extrusion bought)",
        round(2.0 * m_rail / min(z_top, z_bot), 1), 240.0 / 3, "MPa", closed_by="SVD-OPT-001 Table 1; smallest section modulus and a dynamic factor of 2 at rail joints (independent review)")
crr = 0.02
f_b = crr * (D["sledge_L"] * P["n_sledges"] * A["rho_spoil"] + 40.0 * P["n_sledges"]) * G + CAL.F_rope + CAL.F_back
c.claim("O2", "Option B: rolling the train on rails (rolling resistance 0.02) cuts the pull to less than half of the sliding train", "Physics", "Mechanics and statics",
        "F = c_rr m g plus the same rope drag and back tension; c_rr = 0.02 for polymer wheels on aluminium rail (estimate, to confirm)",
        round(f_b, 0), round(CAL.F_load / 2, 0), "N", closed_by="SVD-OPT-001 Table 1")
v_cap = CAL.per_rev * A["rpm_max"]                                      # m/min at the handle's rpm limit
v_lb = min(A["P_crank"] * A["eta_winch"] / f_b, v_cap / 60) * 60
q_b_hand = CAL.VL / 1000 / (CAL.cycle(v_lb, v_cap)[4] / 60)
c.claim("O5", "Option B: cranked by hand, the rail train keeps ahead of the Silkyara face rate", "Mathematics", "Rates and cycle times",
        "Cycle arithmetic with the handle at its 60 rpm limit both ways (%.1f m/min); option A by hand makes %.2f m3/h" % (v_cap, CAL.q_hand),
        round(q_b_hand, 3), round(CAL.face, 3), "m3/h", rule="above", margin=0.1, closed_by="SVD-OPT-001 Table 1")
# Option C: pneumatic extraction through 150 mm hose over 70 m. Terminal velocity of a lump and the air power to carry it.
RHO_A, RHO_S, Dh, Lh = 1.2, 2600.0, 0.15, 70.0


def p_air(v, loading=2.0, f=0.02):
    q = math.pi / 4 * Dh ** 2 * v
    dp = f * Lh / Dh * RHO_A * v ** 2 / 2
    return loading * q * dp


def v_term(d):
    return math.sqrt(4 * G * d * (RHO_S - RHO_A) / (3 * 1.0 * RHO_A))


LUMP = 0.012                                 # m: the largest lump the face crew feeds to the nozzle (fix, SVD-DEC-001 D1)
p_first = p_air(1.5 * v_term(0.006)) / 0.6 / 1000      # kW: 6 mm fines with the first-draft 2.2 kW fan
p_rubble = p_air(1.5 * v_term(0.05)) / 0.6 / 1000      # kW: the 50 mm rubble of the first draft
c.claim("O4", "Option C, after the fix: a 7.5 kW three-phase high-pressure blower on a portal generator conveys lumps of up to 12 mm through 70 m of 150 mm hose", "Physics", "Fluid mechanics",
        "Conveying air at 1.5 times the terminal velocity v_t = sqrt(4 g d (rho_s - rho_a) / (3 C_d rho_a)), C_d = 1 (v_t = %.0f m/s for 12 mm), solids loading doubles the air power; air power = Q dp, 60 %% efficient. "
        "First draft: the 2.2 kW fan needed %.1f kW for 6 mm fines and a lump of 50 mm needs %.0f kW, so the first draft failed; the fix keeps suction extraction, limits the lump to 12 mm (the crew feeds the nozzle by hand) and sizes the blower on the pressure and flow the hose needs (SVD-DEC-001 D1)" % (v_term(LUMP), p_first, p_rubble),
        round(p_air(1.5 * v_term(LUMP)) / 0.6 / 1000, 1), 7.5, "kW", margin=0.15, closed_by="SVD-DEC-001 D1; a named blower curve passing about %.0f m3/h at %.1f kPa is to assess" % (math.pi / 4 * Dh ** 2 * 1.5 * v_term(LUMP) * 3600, 0.02 * Lh / Dh * RHO_A * (1.5 * v_term(LUMP)) ** 2 / 2 / 1000))

c.write()
