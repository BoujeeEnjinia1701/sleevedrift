"""SleeveDrift sizing calculations (SVD-CAL-001), TRL 3.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every figure quoted in docs/04-calcs/01-sizing.md, tagged [A1], [B2] and so on, and
writes docs/04-calcs/results.csv (one row per requirement). Geometry comes from cad/src/model.py
(PARAMS, derived(), masses()); costs from bom/bom.csv; the value-engineering target from
project.yaml. First-principles estimates for a paper proof of concept, not test results.
"""
import csv
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "cad" / "src")]
from model import PARAMS as P, derived, masses, wall_dist  # noqa: E402

D = derived(P)
M = masses(P)
g = 9.81
OUT = []


def say(tag, text):
    line = f"[{tag}] {text}"
    print(line)
    OUT.append(line)


# ------------------------------------------------------------------ assumptions
A = dict(
    rho_spoil=1.70,          # kg/L loose broken rock, soil and concrete rubble (range 1.5 to 1.9)
    mu_k=0.30, mu_s=0.40,    # UHMW-PE runners on gritty steel pipe floor, sliding and starting
    mu_rope=0.50,            # rope dragging on the pipe floor
    back_N=50.0,             # N, tension held on the easing winch while the other hauls
    eta_sheave=0.95, eta_winch=0.85,
    pr_high=13.0, pr_low=40.0,   # winch power ratios with a 250 mm handle (typical two-speed size 40 class)
    P_crank=60.0,            # W, sustained hand cranking by one person in shifts
    rpm_max=60.0,            # handle rpm, light load
    unload_min_per=1.0,      # min to tip one sledge at the portal (two people)
    load_Lpm=30.0,           # L/min, the second crew member filling sledges with a scoop pan
    signal_min=1.0,          # min per cycle for signals and clipping
    drill_rpm=120.0,         # socket rpm from a right-angle drill with a winch bit (decision 24B)
    eta_drill=0.60,          # drill battery to socket (motor and gearbox), loaded
    clutch_Nm=35.0,          # drill slip clutch setting at the socket
    batt_Wh=90.0,            # 18 V, 5 Ah battery
    m_drill=2.9, m_bit=0.3, m_batt=0.7, m_charger=0.6,   # kg, bought drive parts
    face_adv_m=10.0, face_hours=24.0, bulk=1.30,   # Silkyara hand-mined advance and bulking
    E=205e9, fy=355e6, fy_pin=355e6,
    hood_load=5000.0,        # N, R2
    breakaway=2500.0,        # N, R11 swivel release
    splice=0.90,
    preload_crown=15e3, preload_side=10e3, mu_pad=0.20,
    manikin=100.0, stretcher=9.0, haul_people=3, haul_speed=0.40,   # m/s hand over hand
    duct_f=0.030, duct_K=2.1, leak=0.065, Q=0.27,   # Darcy factor, minor losses, leakage over 65 m, m3/s at the blower
    rho_air=1.20, people=3, met_W=300.0,
)
Lp = P["Lp"] / 1000.0          # m


# ------------------------------------------------------------------ A. fit in the pipe (R1)
pid = D["pipe_id"]
say("A1", f"Pipe inside diameter {pid:.0f} mm (800 x 10 mm assumed); ring outside diameter {P['ring_od']:.0f} mm; "
          f"ring rests on the invert, so the gap is {2 * D['radial_gap']:.0f} mm at the crown and 0 at the invert")
env = D["ro"] + P["pad"][1]
say("A2", f"Pieces that go in: ring segments with pads retracted fit a {2 * env:.0f} mm circle; sledge {P['sledge_w'][1]:.0f} mm wide x "
          f"{D['sledge_z0'] + P['sledge_h']:.0f} mm high; stretcher rolled to about 480 mm; largest single piece the crown "
          f"segment, chord {2 * D['ro'] * math.sin(math.radians(60)):.0f} mm, rise {D['ro'] * (1 - math.cos(math.radians(60))):.0f} mm, {M['crown']:.1f} kg")
# crawl space beside the duct, cable and return rope
duct = (D["ro"] * 0 + P["duct_r"] * math.sin(math.radians(P["duct_th"])), P["duct_r"] * math.cos(math.radians(P["duct_th"])), P["duct_d"] / 2)
rope = (P["ret_y"], D["rope_floor_z"][P["ret_y"]] - P["zc"], P["rope_d"] / 2)
best = (0, 0, 0)
R = pid / 2
for i in range(-80, 81):
    for j in range(-80, 81):
        y, z = i * 4.0, j * 4.0
        dpipe = R - math.hypot(y, z)
        if dpipe <= 0:
            continue
        r = min(dpipe, math.hypot(y - duct[0], z - duct[1]) - duct[2], math.hypot(y - rope[0], z - rope[1]) - rope[2])
        if r > best[0]:
            best = (r, y, z)
say("A3", f"Largest clear circle for a crawling person beside the duct and return rope: {2 * best[0]:.0f} mm "
          f"(the empty pipe gives {pid:.0f} mm)")
ring_clear = 2 * D["ri"]
say("A4", f"Clear height inside the ring and under the hood: {ring_clear:.0f} mm")
say("A5", "600 mm pipe (R1 stretch): kept as a stretch until the co-design partner says whether 600 mm pipes are used for rescue "
          "(decision 26C); the ring, sledge and sheave sizes are parameters in the model")

# ------------------------------------------------------------------ B. hood (R2)
t = P["shell_t"]
rm = D["ro"] - t / 2
pts = []                       # (area mm2, z mm) for the crown section about the ring axis
n = 240
for k in range(n):
    th = math.radians(-60 + 120 * (k + 0.5) / n)
    pts.append((t * rm * math.radians(120) / n, rm * math.cos(th)))
fd, ft = P["flange"]
for k in range(25):
    r = D["ri"] - fd + fd * (k + 0.5) / 25
    for s in (-1, 1):
        pts.append((ft * fd / 25, r * math.cos(math.radians(60))))
Aa = sum(a for a, _ in pts)
zbar = sum(a * z for a, z in pts) / Aa
I = sum(a * (z - zbar) ** 2 for a, z in pts)
cmax = max(abs(D["ro"] - zbar), abs(zbar - (D["ri"] - fd) * math.cos(math.radians(60))))
Lc = (P["ring_out"] + P["hood"]) / 1000
w = A["hood_load"] / Lc
Mb = w * Lc ** 2 / 2
sig = Mb * cmax * 1e-3 / (I * 1e-12)
delta = w * Lc ** 4 / (8 * A["E"] * I * 1e-12)
say("B1", f"Crown section (120 deg of {t:.0f} mm shell plus two 50 x 10 mm ribs): area {Aa:.0f} mm2, I = {I / 1e6:.2f} x 10^6 mm4")
say("B2", f"5 kN spread over the {Lc * 1000:.0f} mm of crown beyond the pipe mouth, crown alone as a cantilever: "
          f"M = {Mb:.0f} N m, stress {sig / 1e6:.1f} MPa (yield {A['fy'] / 1e6:.0f} MPa), tip deflection {delta * 1000:.2f} mm")
p_hood = A["hood_load"] / (Lc * 2 * D["ro"] * math.sin(math.radians(60)) / 1000)
N = p_hood * rm / 1e6
say("B3", f"Arch action across the hood: pressure {p_hood / 1000:.1f} kPa, hoop force {N:.1f} N/mm, stress {N / t:.1f} MPa")
head_gap = 100.0
say("B4", f"With the head form set {head_gap:.0f} mm below the hood, the deflection uses {100 * delta * 1000 / head_gap:.2f} % of the gap; R2 met on paper")
lever = -P["jack_x"]
Fpad = Mb / (lever / 1000) / 2 / math.cos(math.radians(15))
say("B5", f"Ring held in the mouth: the moment is taken by the bottom of the ring at the mouth and the two crown pads "
          f"{lever:.0f} mm inside: {Fpad / 1000:.1f} kN on each crown screw (preload {A['preload_crown'] / 1000:.0f} kN)")

# ------------------------------------------------------------------ C. haul forces (R4, R11)
VL = D["sledge_L"] * P["n_sledges"]
m_spoil = VL * A["rho_spoil"]
m_tare = M["sledge"] * P["n_sledges"] + 3.0
rope_len = 2 * Lp + 2 * abs(P["x_stand"]) / 1000
F_rope = 2 * Lp * P["rope_kgm"] * g * A["mu_rope"]
F_back = A["back_N"] / A["eta_sheave"]
F_load = A["mu_k"] * (m_spoil + m_tare) * g + F_rope + F_back
F_start = A["mu_s"] * (m_spoil + m_tare) * g + F_rope + F_back
F_empty = A["mu_k"] * m_tare * g + F_rope + F_back
say("C1", f"Train: {P['n_sledges']} sledges of {D['sledge_L']:.1f} L = {VL:.0f} L, {m_spoil:.0f} kg of spoil, {m_tare:.0f} kg of sledges and links")
say("C2", f"Rope in the pipe {2 * Lp:.0f} m (pull leg + tail and return), drag {F_rope:.0f} N; back tension through the sheave {F_back:.0f} N")
say("C3", f"Pull: loaded {F_load:.0f} N, starting {F_start:.0f} N, empty {F_empty:.0f} N")
h = lambda F, pr: F / (pr * A["eta_winch"])  # noqa: E731
say("C4", f"Handle force: high gear {h(F_load, A['pr_high']):.0f} N loaded, {h(F_start, A['pr_high']):.0f} N starting; "
          f"low gear {h(F_load, A['pr_low']):.0f} N and {h(F_start, A['pr_low']):.0f} N; R4 met")
heave = 400.0
say("C5", f"Without a limit, one person heaving {heave:.0f} N in low gear puts {heave * A['pr_low'] * A['eta_winch'] / 1000:.1f} kN on the rope; "
          f"the breakaway swivels release at {A['breakaway'] / 1000:.1f} kN (R11)")
fos_rope = P["rope_mbs"] * A["splice"] / A["breakaway"]
say("C6", f"Rope {P['rope_mbs'] / 1000:.0f} kN, {A['splice'] * 100:.0f} % at the splice: factor {fos_rope:.1f} on the release load; "
          f"{P['rope_mbs'] * A['splice'] / F_load:.0f} on the working pull")
Fs = 2 * A["breakaway"]
lev = P["rope_z"] - P["base_top"]
d = P["sheave_pin"]
sig_pin = Fs * lev / (math.pi * d ** 3 / 32)
say("C7", f"Face sheave at the limit: {Fs / 1000:.1f} kN on the pin, {lev:.0f} mm above the base plate: bending stress {sig_pin:.0f} MPa "
          f"(factor {A['fy_pin'] / 1e6 / sig_pin:.1f} on S355 yield)")
Nn = 2 * A["preload_crown"] + 2 * A["preload_side"] + 2 * A["preload_crown"] * math.cos(math.radians(15))
Ff = A["mu_pad"] * Nn
say("C8", f"Ring held against the sheave pull by friction: normal forces {Nn / 1000:.0f} kN, friction at mu {A['mu_pad']:.2f} = {Ff / 1000:.1f} kN, "
          f"factor {Ff / Fs:.1f} on {Fs / 1000:.1f} kN")
x_s = abs(P["x_stand"])
z_drop = P["rope_hz"] - D["rope_floor_z"][0.0]
say("C9", f"Rope lead to the winches: {z_drop:.0f} mm rise over {x_s:.0f} mm = {math.degrees(math.atan(z_drop / x_s)):.1f} deg below the drum, "
          "inside the 5 to 10 deg usual for a self-tailer")
H = P["trestle"][2]
say("C10", f"Trestle: rope {P['rope_hz']:.0f} mm up, sling eye {H + 80:.0f} mm up: overturning moment at the limit "
           f"{A['breakaway'] * (P['rope_hz'] - H - 80) / 1000:.0f} N m against {M['trestle'] * g * P['trestle'][0] / 2000:.0f} N m from the trestle's weight")

# ------------------------------------------------------------------ D. output (R3)
def cycle(v_load, v_empty, n_sl=P["n_sledges"], unload_per=A["unload_min_per"], load_rate=A["load_Lpm"]):
    t_out = Lp / v_load
    t_in = Lp / v_empty
    t_un = n_sl * unload_per
    t_ld = n_sl * D["sledge_L"] / load_rate
    return t_out, t_in, t_un, t_ld, t_out + t_in + t_un + t_ld + A["signal_min"]


per_rev = 2 * math.pi * P["handle"] / 1000 / A["pr_high"]       # m of rope per handle turn, high gear
v_l = min(A["P_crank"] * A["eta_winch"] / F_load, per_rev * A["rpm_max"] / 60) * 60
v_e = min(A["P_crank"] * A["eta_winch"] / F_empty, per_rev * A["rpm_max"] / 60) * 60
c_hand = cycle(v_l, v_e)
q_hand = VL / 1000 / (c_hand[4] / 60)
face = math.pi / 4 * 0.8 ** 2 * A["face_adv_m"] * A["bulk"] / A["face_hours"]
say("D1", f"Hand: loaded {v_l:.1f} m/min ({A['P_crank']:.0f} W at the handle), empty {v_e:.1f} m/min (handle at {A['rpm_max']:.0f} rpm)")
say("D2", f"Hand cycle: out {c_hand[0]:.1f}, unload {c_hand[2]:.1f}, in {c_hand[1]:.1f}, load {c_hand[3]:.1f}, signals {A['signal_min']:.1f}: "
          f"{c_hand[4]:.1f} min for {VL:.0f} L = {q_hand:.2f} m3/h (R3 not met)")
say("D3", f"Silkyara face rate for comparison: about {A['face_adv_m']:.0f} m in {A['face_hours']:.0f} h through 0.8 m, bulked x {A['bulk']}: "
          f"{face:.2f} m3/h of loose spoil")
v_d = per_rev * A["drill_rpm"]
c_b = cycle(v_d, v_d)
q_b = VL / 1000 / (c_b[4] / 60)
say("D4", f"As designed (decision 24B): right-angle drill with a winch bit on each winch at {A['drill_rpm']:.0f} rpm, high gear: {v_d:.1f} m/min, "
          f"{F_load * v_d / 60:.0f} W at the rope loaded; cycle: out {c_b[0]:.1f}, unload {c_b[2]:.1f}, in {c_b[1]:.1f}, load {c_b[3]:.1f}, "
          f"signals {A['signal_min']:.1f} = {c_b[4]:.1f} min = {q_b:.2f} m3/h (R3 not met; faster than the face [D3])")
n6 = 6
m6 = (D["sledge_L"] * n6 * A["rho_spoil"] + M["sledge"] * n6 + 5) * g * A["mu_k"] + F_rope + F_back
c_c = cycle(v_d, v_d, n_sl=n6, unload_per=0.5, load_rate=60.0)
q_c = D["sledge_L"] * n6 / 1000 / (c_c[4] / 60)
say("D5", f"Not adopted (option C): the drill drive plus six sledges, two people tipping at the portal and spoil pre-bagged at the face: "
          f"pull {m6:.0f} N, cycle {c_c[4]:.1f} min = {q_c:.2f} m3/h")
r_h = P["handle"] / 1000
T_load = F_load * r_h / (A["pr_high"] * A["eta_winch"])
T_start = F_start * r_h / (A["pr_high"] * A["eta_winch"])
F_slip_hi = A["clutch_Nm"] * A["pr_high"] * A["eta_winch"] / r_h
F_slip_lo = A["clutch_Nm"] * A["pr_low"] * A["eta_winch"] / r_h
say("D6", f"Drill torque at the socket in high gear: {T_load:.1f} N m loaded, {T_start:.1f} N m starting; clutch set to {A['clutch_Nm']:.0f} N m "
          f"slips at {F_slip_hi / 1000:.2f} kN of rope pull, below the {A['breakaway'] / 1000:.1f} kN swivel release. In low gear the same clutch "
          f"would allow {F_slip_lo / 1000:.1f} kN, so the drill is used in high gear only and the swivels stay the limit")
E_rope = (F_load + F_empty) * Lp            # J per round trip at the rope
E_batt = E_rope / A["eta_winch"] / A["eta_drill"]
Wh_h = E_batt / 3600 * 60 / c_b[4]
say("D7", f"Energy: {E_rope / 1000:.1f} kJ at the rope per round trip, {E_batt / 1000:.0f} kJ ({E_batt / 3600:.0f} Wh) from the battery at "
          f"{A['eta_drill']:.2f} drill efficiency; {Wh_h:.0f} Wh an hour, one {A['batt_Wh']:.0f} Wh battery every {A['batt_Wh'] / Wh_h:.1f} h of hauling; "
          "six batteries and two chargers on portal power keep the haul going")
F_load_e = F_load * Lp / 1000
say("D8", f"Per loaded haul: {F_load * Lp / 1000 / A['eta_winch'] / A['eta_drill']:.1f} kJ from the battery, "
          f"{F_load * Lp / 1000 / A['eta_winch']:.1f} kJ at the socket, {F_load_e:.1f} kJ at the rope, "
          f"{(F_load - F_rope - F_back) * Lp / 1000:.1f} kJ to drag the train; hand cranking at 60 W stays the fallback [D2]")

# ------------------------------------------------------------------ E. casualty (R6)
mc = A["manikin"] + A["stretcher"]
Fc = A["mu_k"] * mc * g + F_rope + F_back
Fc0 = A["mu_s"] * mc * g + F_rope + F_back
tc = Lp / A["haul_speed"] / 60 + 1.0
say("E1", f"Casualty: {mc:.0f} kg on the stretcher, pull {Fc:.0f} N ({Fc0:.0f} N starting)")
say("E2", f"{A['haul_people']} people hand over hand on the pull rope through winch A (which holds when let go): "
          f"{Fc0 / A['haul_people']:.0f} N each at the start, {A['haul_speed'] * 60:.0f} m/min, {tc:.1f} min including 1 min to clip on (R6 met on paper)")
say("E3", f"Cranked in high gear at {A['rpm_max']:.0f} rpm instead: {Lp / (per_rev * A['rpm_max']):.1f} min; with the drill drive "
          f"{Lp / v_d + 1.0:.1f} min including clipping on; so hand hauling is the method")

# ------------------------------------------------------------------ F. air (R5)
Ld = Lp + 5.0
Dd = P["duct_d"] / 1000
v = A["Q"] / (math.pi * Dd ** 2 / 4)
q = A["rho_air"] * v ** 2 / 2
dp = (A["duct_f"] * Ld / Dd + A["duct_K"]) * q
Qf = A["Q"] * (1 - A["leak"]) * 60
say("F1", f"Duct {Ld:.0f} m of 200 mm layflat at {A['Q']:.2f} m3/s: {v:.1f} m/s, loss {dp:.0f} Pa; blower about {A['Q'] * dp / 0.5:.0f} W of shaft power at 50 %")
say("F2", f"Delivered at the face after {A['leak'] * 100:.1f} % leakage: {Qf:.1f} m3/min ({Qf / A['people']:.1f} per person; R5 met with margin)")
Ap = math.pi / 4 * (pid / 1000) ** 2
say("F3", f"Pipe air volume {Ap * Lp:.1f} m3: one change every {Ap * Lp / Qf:.1f} min; return air along the pipe at {Qf / 60 / (Ap - math.pi / 4 * Dd ** 2):.2f} m/s")
dT = A["people"] * A["met_W"] / (A["rho_air"] * 1005 * Qf / 60)
say("F4", f"Body heat of {A['people']} people at {A['met_W']:.0f} W warms the air {dT:.1f} K")

# ------------------------------------------------------------------ G. set-up time (R7)
steps = [("Trestles, winches, guards, slings and bins at the portal; drills fitted and clutches set", 25), ("Blower and first duct lengths at the portal", 10),
         ("Bottom segment taken in on a sledge by a crew member, both ropes paying out", 15),
         ("Bottom segment set in the mouth; tail rope reeved round the sheave", 10),
         ("Crown and side segments sent in on one shuttle trip (drill, high gear)", round(Lp / v_d)),
         ("Segments bolted, jacking screws tightened", 20), ("Train made up and clipped in; first empty run in", round(Lp / v_d)),
         ("Signal check and gas check before digging", 5)]
tot = sum(m for _, m in steps)
say("G1", "Set-up steps (min): " + "; ".join(f"{s} {m}" for s, m in steps))
say("G2", f"Total {tot} min = {tot / 60:.1f} h on the critical path; duct and cable hung in parallel by a second pair (about 40 min); R7 met on paper, verify in drill")

# ------------------------------------------------------------------ H. durability (R9)
cyc = 72 * 60 / c_b[4]
km = cyc * 2 * Lp * 2 / 1000
say("H1", f"72 h at the drill rate: {cyc:.0f} round trips; each metre of rope in the pipe drags about {km:.0f} km over the gritty floor")
wear = cyc * 2 * Lp / 1000 * 0.1
say("H2", f"Sledge runners slide {cyc * 2 * Lp / 1000:.0f} km: about {wear:.1f} mm of 10 mm worn at 0.1 mm/km (UHMW-PE in sandy slurry, assumed)")
say("H3", "Rope abrasion over that distance on gritty steel is not predictable on paper. Managed as maintenance (decision 25A): both ropes "
          f"inspected against a 9 mm wear gauge at every shift change, a spare set of 215 m in the kit, a worn rope swapped in about 20 min; "
          "the drills, clutch settings and guards are checked at the same time")

# ------------------------------------------------------------------ I. masses and cases (R10)
cases = [("Crown segment", M["crown"]), ("Side segments (2)", 2 * M["side_p"]),
         ("Bottom segment, sheave, spacer and cover", M["bottom"] + M["sheave"] + M["sheave_hw"] + M["cover"]),
         ("Winch trestle (each)", M["trestle"]), ("Winches (2, about 9 kg each), handles, ties", 18 + 4 * M["ties"] + 2),
         ("Sledges (4, nested), links, swivels", 4 * M["sledge"] + 5), ("Ropes (215 m) and spare set (215 m)", 2 * (215 * P["rope_kgm"] + 1)),
         ("Drill drive: 2 drills, 2 bits, 2 spare batteries, charger, 2 drum guards",
          2 * A["m_drill"] + 2 * A["m_bit"] + 2 * A["m_batt"] + A["m_charger"] + 2 * M["guard"]),
         ("Blower (about 20 kg)", 20.0), ("Duct (65 m at 0.4 kg/m)", 26.0),
         ("Stretcher, spreader, monitors, phones, lamps", 9 + M["spreader"] + 2 + 12 + 4), ("Tools, spigot, jacks, bolts, hangers", 14 + M["spigot"] + M["jacks"] + M["joint_bolts"] + 6)]
heavy = max(cases, key=lambda c: c[1])
say("I1", "Packages (kg): " + "; ".join(f"{n} {m:.1f}" for n, m in cases))
say("I2", f"Kit {sum(m for _, m in cases):.0f} kg in {len(cases) + 1} packages; heaviest {heavy[0]} {heavy[1]:.1f} kg (R10 met)")

# ------------------------------------------------------------------ J. cost
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
target = float(re.search(r"budget_usd:\s*([\d.]+)", (ROOT / "project.yaml").read_text()).group(1))
top = sorted(rows, key=lambda r: -float(r["qty"]) * float(r["unit_cost_usd"]))[:5]
say("J1", f"Value-engineering target: USD {target:,.0f}. Estimated cost of the constructable design: USD {cost:,.2f} "
          f"(USD {abs(cost - target):,.2f} {'over' if cost > target else 'under'} the target)")
say("J2", "Largest lines: " + "; ".join(f"{r['item'].split(' ', 1)[1]} USD {float(r['qty']) * float(r['unit_cost_usd']):,.0f}" for r in top))

# ------------------------------------------------------------------ results table
R = [
    ("R1", f"all parts pass a {2 * env:.0f} mm circle in a {pid:.0f} mm pipe; 600 mm variant waits for the co-design partner (decision 26C)", "800 mm pipe; 600 mm stretch", "met (800); open (600 stretch, decision 26C)"),
    ("R2", f"{sig / 1e6:.1f} MPa, {delta * 1000:.2f} mm at 5 kN", "5 kN, no head contact", "met on paper"),
    ("R3", f"{q_b:.2f} m3/h with the portal drill drive ({q_hand:.2f} by hand)", "1 m3/h, two-person crew", "not met"),
    ("R4", f"{h(F_start, A['pr_high']):.0f} N high gear starting", "under 200 N", "met on paper"),
    ("R5", f"{Qf:.1f} m3/min at the face", "1 m3/min", "met on paper"),
    ("R6", f"{tc:.1f} min by hand hauling", "under 5 min", "met on paper"),
    ("R7", f"{tot / 60:.1f} h estimated", "2 h", "met on paper (estimate)"),
    ("R8", "battery lamps, gas monitors and sound-powered telephones only", "no power in the pipe", "met by design"),
    ("R9", f"{cyc:.0f} round trips; ropes inspected each shift, spare set carried", "72 h", "managed by inspection and spares (decision 25A); endurance trial at TRL 4"),
    ("R10", f"heaviest package {heavy[1]:.1f} kg", "40 kg", "met"),
    ("R11", f"release {A['breakaway'] / 1000:.1f} kN; rope factor {fos_rope:.1f}", "2.5 kN limit", "met by design"),
    ("R12", "two four-gas monitors in the kit", "continuous monitoring", "met by design"),
]
with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
    wtr = csv.writer(f)
    wtr.writerow(["id", "value", "target", "status"])
    wtr.writerows(R)
print("wrote docs/04-calcs/results.csv")
