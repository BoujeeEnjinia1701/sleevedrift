"""SleeveDrift parametric model, kit 1.9 interface (STANDARDS section 24), detail level D3 for every option.

Run from the repo root:
    python .kit/cad_check.py --export     fidelity check, STEP per part and per assembly (cad/step/)
    python cad/src/model.py               part list with masses, and STL of the chosen design (cad/stl/)

Axes: X runs along the rescue pipe from its portal end (x = 0) to the face end (x = Lp), Y is across the pipe, Z is
up with the platform the pipe rests on at z = 0. The pipe axis is at z = 400 mm. Angles round the pipe axis (theta)
are measured from the top (+Z) toward +Y. The train lane runs along the pipe floor on y = 0; the return leg of the
rope lies on the floor at y = +230 mm; the air duct hangs on the upper +Y wall and the signal cable near the crown.
components() uses the shortened picture layout (6.8 m of pipe, station 2.4 m behind the pipe end) because a 60 m
assembly adds nothing but repeated duct, rope and hangers; PARAMS["Lp"] is the 60 m design case that the
calculations use.

Options (SVD-OPT-001):
    A  rope shuttle of sliding sledges: four 30 L sledges between a pull rope and a tail rope, two self-tailing
       winches turned by right-angle drills at the portal (the current design, decisions of 2026-10-03)
    B  rail tramway: aluminium rails laid on the pipe floor in 3 m sections, a train of wheeled wagons on them,
       same ring, ropes and portal station
    C  pneumatic extraction: a 150 mm suction hose from a nozzle under the hood to a cyclone and blower at the
       portal, no sledges, no winches; a casualty line replaces the shuttle for evacuation

Every part is a cad_parts.part() dict: made, bought, fastener, weld or context. BOM line numbers are given for the
chosen option (A) only. `group` carries the legacy component key that the drawing sheets, build plan pictures and
product model pick parts by.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, Solid, Sphere, Vector, extrude, Sketch, Circle  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, at, break_edges  # noqa: E402
from sd_parts import (bx, xcyl, ycyl, zcyl, rod, place, bead, ring_weld, prism_yz, sector, radial_bar,  # noqa: E402
                      radial_rod, tang_rod, at_ring, e_t, e_r, csk_screw, _ccw)

TITLE = "SleeveDrift"

PARAMS = {
    # rescue pipe (context): outside diameter, wall, length at the design case; axis height
    "pipe": (800.0, 10.0), "Lp": 60000.0, "zc": 400.0,
    "short": {"Lp": 6800.0, "x_stand": -2400.0},       # shortened layout for pictures
    # 1 to 3 hooded cutting ring: outside diameter, shell thickness, rear length inside the pipe,
    # front length beyond the pipe mouth, hood reach beyond the ring front
    "ring_od": 760.0, "shell_t": 5.0, "ring_in": 200.0, "ring_out": 250.0, "hood": 250.0,
    # segment joints (deg from the top toward +Y): crown -60..60, sides 60..150 and 210..300, bottom 150..210
    "joints": (60.0, 150.0, 210.0, 300.0),
    "flange": (50.0, 10.0),                  # inside joint flange: radial depth x thickness
    "joint_bolts_x": (-170.0, -50.0, 70.0, 190.0),  # bolt stations from the pipe mouth (x - Lp)
    "band": (60.0, 10.0),                    # front cutting band: width x thickness
    "hood_lip": (60.0, 10.0),                # hood front lip band
    # 5 jacking screws M20: angles, station; nut, head, swivel pad
    "jack_th": (15.0, -15.0, 80.0, -80.0), "jack_x": -175.0, "jack_d": 20.0, "ring_drop": 9.8,
    "nut": (30.0, 16.0), "head": (30.0, 13.0), "pad": (50.0, 8.0),
    # 6 to 8 face return sheave: centre (x - Lp, y), rope plane height, pitch dia, OD, width, pin
    "sheave_c": (-20.0, 110.0), "rope_z": 185.0, "sheave": (240.0, 260.0, 30.0), "sheave_pin": 25.0,
    "base_plate": (-190.0, 155.0, -50.0, 145.0, 10.0), "base_top": 150.0,
    "cover": (-190.0, 155.0, -50.0, 250.0, 4.0), "cover_z": 230.0, "posts_xy": ((-178.0, 143.0), (-38.0, 133.0)),
    # 10 spoil sledges: count, length, gap, base and top width, depth, sheet, runners, lugs
    "n_sledges": 4, "sledge_L": 1000.0, "sledge_gap": 150.0, "sledge_w": (160.0, 300.0), "sledge_h": 130.0,
    "sheet": 1.5, "runner": (40.0, 10.0, 55.0), "runner_z": 17.5, "lug": (50.0, 8.0, 40.0), "lug_hole": 16.0,
    "train_gap": 1200.0,                     # face-end sledge end to the pipe mouth, train at the face
    # 13 rope: 10 mm polyester double braid; return leg offset; linear mass kg/m
    "rope_d": 10.0, "rope_mbs": 18000.0, "rope_kgm": 0.065, "ret_y": 230.0, "train_leg_y": -10.0,
    # 14 to 16 portal haul station: trestle footprint, height, SHS; winch centres; stand distance
    "x_stand": -5500.0, "trestle": (700.0, 500.0, 560.0), "shs": (40.0, 3.0), "winch_y": (-200.0, 440.0),
    "winch_x": -300.0, "top_plate": (300.0, 500.0, 10.0),
    "winch": (100.0, 40.0, 45.0, 110.0, 85.0, 70.0), "handle": 250.0, "rope_hz": 650.0,
    # 30 to 32 portal drill drive (Amish's decision 24B, 2026-10-03): winch bit, right-angle head,
    # motor body pointing outboard, battery; drum guard (made) round the rear half of each winch
    "bit": (11.0, 60.0), "drill_head": (38.0, 70.0), "drill_body": (32.0, 300.0), "drill_batt": (110.0, 80.0, 60.0),
    "guard": (130.0, 2.0, 615.0, 790.0, 120.0), "guard_leg": (30.0, 5.0),
    # 20 to 22 air: duct diameter, hanger radius and angle; spigot; blower position
    "duct_d": 200.0, "duct_r": 265.0, "duct_th": 40.0, "spigot": (194.0, 2.0), "spigot_x": (-360.0, 50.0),
    "hanger_pitch": 2500.0, "blower_xy": (-1200.0, 1100.0),
    # 23 signal cable
    "cable_th": 80.0, "cable_d": 8.0,
    # 26 to 27 casualty stretcher (bought, rolled round a person) and the towing spreader bar
    "stretcher": (2100.0, 240.0, 3.0), "spreader": (26.9, 2.6, 450.0),
    # materials (kg per m^3)
    "rho_steel": 7850.0, "rho_uhmw": 940.0, "rho_hdpe": 950.0, "rho_ply": 550.0,
}
PARAMS.update({
    # D3 detail added in kit 1.9 (modelling only; no design dimension changes)
    "weld_leg": 5.0, "m12": 12, "wnut_h": 18.0,
    "saddle_t": 25.0, "saddle_r": 110.0, "bush": (32.0, 25.4), "cover_screw": 8,
    "runner_screws": (100.0, 500.0, 900.0), "csk": (6, 12.0, 12.0, 3.5),
    "spacer": (40.0, 25.5, 20.0), "keeper": (44.0, 25.5, 5.0),
    "tie": (140.0, 6.0, 80.0), "eye_plate": (60.0, 10.0, 110.0), "eye_hole": 22.0,
    "stretcher_roll": 240.0,
    # option B: rails and wagons
    "rail": (32.0, 40.0, 4.0), "gauge": 240.0, "rail_len": 3000.0, "wheel": (80.0, 24.0), "wagon_n": 4,
    "wagon_L": 1000.0, "wagon_gap": 150.0, "wagon_z0": 90.0,
    # option C: suction plant
    "hose_d": 150.0, "hose_wall": 4.0, "cyc_d": 600.0, "cyc_h": 900.0,
})
P = PARAMS

OPTIONS = {"A": "Rope shuttle of sledges", "B": "Rail tramway", "C": "Pneumatic extraction"}
PRINCIPLES = {
    "A": "Four low sledges slide on the pipe floor between a pull rope and a tail rope that turns round a sheave "
         "on the ring; two self-tailing winches turned by drills at the portal haul it.",
    "B": "Wheeled wagons roll on aluminium rails laid on the pipe floor in 3 m sections; the same ropes and portal "
         "winches shuttle the train, but rolling replaces sliding friction.",
    "C": "Spoil is sucked into a 150 mm hose at the face by a blower at the portal and thrown out in a cyclone into "
         "a drum; no moving parts in the pipe and no sledges.",
}
CHOSEN = "A"
OPTION_VIEWS = {k: {"el": 22, "az": -55, "scale": "person", "keep_context": True, "ground_z": 0.0} for k in OPTIONS}
ALLOWED_CONTACTS = [("rope", "sheave"), ("rope", "winch"), ("rope", "swivel"), ("rope", "drum"), ("Rope", "Sheave"),
                    ("Rope", "winch"), ("Rope", "Breakaway"), ("Weld", "Weld"), ("split pin", "pin"),
                    ("Split pin", "pin"), ("bush", "Sheave"), ("Bush", "Sheave"), ("Rope", "Casualty"),
                    ("Layflat duct 200 mm, inside", "portal run"), ("portal run", "Ventilation blower"), ("Cyclone body", "Cyclone inlet box")]


def wall_dist(P, drop, th):
    """Distance from the ring axis (drop below the pipe axis) to the pipe wall along angle th."""
    t = math.radians(th)
    R = (P["pipe"][0] - 2 * P["pipe"][1]) / 2
    return drop * math.cos(t) + math.sqrt(R * R - (drop * math.sin(t)) ** 2)


def at_p(P, r, th, x):
    return at_ring(P["zc"], r, th, x)


def derived(P=PARAMS):
    D = {}
    Do, t = P["pipe"]
    D["pipe_id"] = Do - 2 * t
    D["ro"] = P["ring_od"] / 2
    D["ri"] = D["ro"] - P["shell_t"]
    D["radial_gap"] = D["pipe_id"] / 2 - D["ro"]
    D["ring_len"] = P["ring_in"] + P["ring_out"]
    D["crown_len"] = D["ring_len"] + P["hood"]
    D["x_rear"] = -P["ring_in"]
    D["x_front"] = P["ring_out"]
    D["x_hood"] = P["ring_out"] + P["hood"]
    j = P["joints"]
    D["segments"] = {"crown": (-j[0], j[0]), "side_p": (j[0], j[1]), "bottom": (j[1], j[2]),
                     "side_m": (j[2], j[3])}
    D["sheave_pitch_r"] = P["sheave"][0] / 2
    D["leg_y"] = (P["sheave_c"][1] - D["sheave_pitch_r"], P["sheave_c"][1] + D["sheave_pitch_r"])
    D["sledge_area"] = (P["sledge_w"][0] + P["sledge_w"][1]) / 2 * P["sledge_h"]
    D["sledge_L"] = P["sledge_L"] * D["sledge_area"] / 1e6
    D["train_len"] = P["n_sledges"] * P["sledge_L"] + (P["n_sledges"] - 1) * P["sledge_gap"]
    D["sledge_z0"] = P["runner_z"] + P["runner"][1]
    D["lug_z"] = D["sledge_z0"] + 50.0
    D["floor_z"] = lambda y: P["zc"] - math.sqrt((D["pipe_id"] / 2) ** 2 - y * y)
    rr = D["pipe_id"] / 2 - P["rope_d"] / 2 - 0.5
    D["rope_floor_z"] = {y: P["zc"] - math.sqrt(rr * rr - y * y) for y in (0.0, P["ret_y"])}
    D["drum_rope_r"] = P["winch"][2] + P["rope_d"] / 2
    return D


def layout(short=True):
    if short:
        return P["short"]["Lp"], P["short"]["x_stand"]
    return P["Lp"], P["x_stand"]


# material shorthands
ST, GALV, ZP, UH, ROPE, PL = "painted_steel", "galvanised", "zinc_plated", "hdpe_natural", "rope", "hdpe_black"


def mk(name, shape, mat, kind, bom, group, explode=(0, 0, 0), note=""):
    return part(name, shape, mat, kind=kind, bom=bom, group=group, explode=explode, note=note)


def bolt_set(d, grip, origin, zdir, bom, group, xdir=None, label="", explode=(0, 0, 0)):
    """ISO bolt, two washers and nut clamping 'grip' mm, head on the side the z axis points toward."""
    out = []
    for nm, sh in cp.hex_bolt_set(d, grip):
        out.append(mk(nm + label, place(sh, origin, zdir, xdir), ZP, "fastener", bom, group, explode))
    return out


# ----------------------------------------------------------------------------- face end: the hooded cutting ring
def _tup(v):
    return (v.X, v.Y, v.Z)


def face_end(P=PARAMS, Lp=None, sheave=True):
    """Hooded cutting ring at the end of a pipe of length Lp: four rolled segments with flanges, bands, welds and
    weld nuts, joint bolts, jacking screws and pads, sheave bracket with sheave and cover, duct spigot, lamp."""
    Lp = P["Lp"] if Lp is None else Lp
    D = derived(P)
    ro, ri = D["ro"], D["ri"]
    zr = P["zc"] - P["ring_drop"]
    xr, xf, xh = Lp + D["x_rear"], Lp + D["x_front"], Lp + D["x_hood"]
    fd, ft = P["flange"]
    bw, bt = P["band"]
    rb = ri - fd / 2
    bxs = [Lp + v for v in P["joint_bolts_x"]]
    dt = math.degrees((ft + 0.5) / ri)
    leg = P["weld_leg"]
    jx = Lp + P["jack_x"]
    bomof = {"crown": 3, "side_p": 2, "side_m": 2, "bottom": 1}
    out = []
    jack_seg = {}
    for th in P["jack_th"]:
        jack_seg[th] = next(k for k, (a, b) in D["segments"].items() if (a < th < b) or (a < th + 360 < b))
    for key, (a, b) in D["segments"].items():
        x1 = xh if key == "crown" else xf
        bm = bomof[key]
        nm = {"crown": "Crown segment", "side_p": "Side segment (+Y)", "side_m": "Side segment (-Y)", "bottom": "Bottom segment"}[key]
        shell = sector(zr, ro, ri, a, b, xr, x1)
        for th, k in jack_seg.items():
            if k == key:
                shell = shell - radial_rod(zr, th, ri - 1, ro + 1, 11.0, jx)
        out.append(mk(f"{nm} shell, 5 mm S355 plate rolled to 760 mm OD", break_edges(shell, 0.8), ST, "made", bm, key,
                      explode={"crown": (0, 0, 450), "side_p": (0, 450, 0), "side_m": (0, -450, 0), "bottom": (0, 0, -350)}[key]))
        for th, s0, tag in ((a, 0.0, "first"), (b, -ft, "second")):
            fl = radial_bar(zr, th, ri - fd, ri - 0.2, s0, s0 + ft, xr, x1)
            for x in bxs:
                fl = fl - tang_rod(zr, th, rb, -40, 40, 6.5, x)
            out.append(mk(f"{nm} joint flange {tag}, 50 x 10 flat bar", break_edges(fl, 0.5), ST, "made", bm, key,
                          explode=(0, 0, 0)))
            ax = (1.0, 0.0, 0.0)
            sd, sg = (ft, 1) if tag == "first" else (-ft, -1)      # the far side; the facing side meets the next flange
            p0 = Vector(*at_ring(zr, ri, th, xr)) + e_t(th) * sd
            out.append(mk(f"Weld, {nm.lower()} flange {tag}, far side",
                          bead(_tup(p0), ax, x1 - xr - bw - 2.0, leg, _tup(-e_r(th)), _tup(e_t(th) * sg)), ST, "weld", bm, key))
        if key == "crown":
            band = sector(zr, ri - 0.1, ri - P["hood_lip"][1], a + dt, b - dt, xh - P["hood_lip"][0], xh)
            out.append(mk("Hood lip band, 60 x 10 flat rolled", break_edges(band, 0.5), ST, "made", bm, key))
        else:
            band = sector(zr, ri - 0.1, ri - bt, a + dt, b - dt, xf - bw, xf)
            out.append(mk(f"Cutting band {nm.lower()}, 60 x 10 flat rolled", break_edges(band, 0.5), ST, "made", bm, key))
    # weld nuts and jacking screws
    nut_h = cp.ISO[20][2]
    pd, pt = P["pad"]
    Pa = P
    for th in P["jack_th"]:
        seg = jack_seg[th]
        er = e_r(th)
        base = Vector(*at_ring(zr, ri - 0.5, th, jx))
        out.append(mk(f"M20 weld nut at {th:.0f} deg", place(cp.hex_nut(20), _tup(base), _tup(-er)), ZP, "fastener", bomof[seg], seg))
        rw = wall_dist(Pa, P["ring_drop"], th) - 0.6 - (pd / 2) ** 2 / (2 * D["pipe_id"] / 2)
        tip = rw - pt
        L = 60.0
        head_at = Vector(*at_ring(zr, tip - L, th, jx))
        out.append(mk(f"M20 x {L:.0f} jacking screw at {th:.0f} deg (ISO 4017)", place(cp.hex_bolt(20, L), _tup(head_at), _tup(-er)), ZP,
                      "fastener", 5, "jacks", explode=(0, 0, 650)))
        lock = Vector(*at_ring(zr, ri - 0.5 - nut_h - 1.0, th, jx))
        out.append(mk(f"M20 locknut at {th:.0f} deg", place(cp.hex_nut(20), _tup(lock), _tup(-er)), ZP, "fastener", 5, "jacks"))
        padc = Vector(*at_ring(zr, tip, th, jx))
        padsh = cp.round_bar(pd, pt, 1.5)
        padsh = padsh - Pos(0, 0, 0.0) * Cylinder(6, 3) if False else padsh
        out.append(mk(f"Swivel pad at {th:.0f} deg, 50 x 8 mild steel", place(padsh, _tup(padc), _tup(er)), "mild_steel", "made", 5, "jacks",
                      explode=(0, 0, 650)))
    # joint bolts: head on the first-segment side, nut on the second
    for th in P["joints"]:
        for x in bxs:
            o = Vector(*at_ring(zr, rb, th, x)) + e_t(th) * (-ft)
            for nm_, sh in cp.hex_bolt_set(P["m12"], 2 * ft):
                out.append(mk(nm_ + f" at {th:.0f} deg", place(sh, _tup(o), _tup(-e_t(th))), ZP, "fastener", 4, "joint_bolts"))
    # sheave bracket on the bottom segment
    if sheave:
        sx, sy = Lp + P["sheave_c"][0], P["sheave_c"][1]
        bx0, bx1, by0, by1, bt_ = P["base_plate"]
        zt = P["base_top"]
        bp = Pos(Lp + (bx0 + bx1) / 2, (by0 + by1) / 2, zt - bt_) * cp.sheet(bx1 - bx0, by1 - by0, bt_, r_corner=6.0)
        out.append(mk("Sheave base plate, 10 mm S355", bp, ST, "made", 1, "bottom", (0, 0, 120)))
        zin = lambda y: zr - math.sqrt(ri * ri - y * y)  # noqa: E731
        ys = [by0 + (by1 - by0) * k / 12 for k in range(13)]
        prof = [(by0, zt - bt_), (by1, zt - bt_)] + [(y, zin(y) + 0.3) for y in reversed(ys)]
        sad_x = [(Lp + bx0 + 5, Lp + bx0 + 15), (Lp + bx1 - 15, Lp + bx1 - 5)]
        for i, (xa, xb) in enumerate(sad_x):
            out.append(mk(f"Sheave saddle {i + 1}, 10 mm plate cut to the shell", break_edges(prism_yz(prof, xa, xb), 0.5), ST, "made", 1, "bottom"))
            for xe, sgn in ((xa, -1), (xb, 1)):
                out.append(mk(f"Weld, saddle {i + 1} to base plate, {'rear' if sgn < 0 else 'front'}",
                              bead((xe, by0, zt - bt_), (0, 1, 0), by1 - by0, leg, (0, 0, -1), (sgn, 0, 0)), ST, "weld", 1, "bottom"))
        pinsh = cp.round_bar(P["sheave_pin"], 70.0, 1.0) - Pos(0, 0, 62.0) * Rot(0, 90, 0) * Cylinder(3.2, 40)
        out.append(mk("Sheave pin, 25 mm bright bar S355", place(pinsh, (sx, sy, zt), (0, 0, 1)), "mild_steel", "made", 1, "bottom", (0, 0, 120)))
        out.append(mk("Weld, pin to base plate", ring_weld(P["sheave_pin"] / 2, 3.0, (sx, sy, zt), (0, 0, 1)), ST, "weld", 1, "bottom"))
        (px0, px1), (py0, py1) = P["posts_xy"]
        for i, (x, y) in enumerate([(px0, py0), (px0, py1), (px1, py0), (px1, py1)]):
            post = cp.round_bar(20.0, P["cover_z"] - zt, 1.0) - Pos(0, 0, P["cover_z"] - zt - 10.0) * Cylinder(4.0, 20.0)
            out.append(mk(f"Cover post {i + 1}, 20 mm round bar", place(post, (Lp + x, y, zt), (0, 0, 1)), ST, "made", 1, "bottom", (0, 0, 200)))
            out.append(mk(f"Weld, post {i + 1} to base plate", ring_weld(10.0, 4.0, (Lp + x, y, zt), (0, 0, 1)), ST, "weld", 1, "bottom"))
        # sheave (bought) with its bush, spacer, keeper and R-clip
        z0 = P["rope_z"] - P["sheave"][2] / 2
        R, Rc = P["sheave"][1] / 2, D["sheave_pitch_r"] - P["rope_d"] / 2
        sh = zcyl(0, 0, R, 0, 8) + zcyl(0, 0, Rc, 8, 22) + zcyl(0, 0, R, 22, 30) + zcyl(0, 0, 24, 0, 30)
        sh = break_edges(sh - zcyl(0, 0, 16.0, -1, 31), 0.8)
        out.append(mk("Face return sheave, 240 mm pitch, 260 mm OD, for 10 mm rope", Pos(sx, sy, z0) * sh, "zinc_plated", "bought", 6, "sheave", (0, 0, 150)))
        out.append(mk("Sheave bush, bronze, 32 x 25.4 x 30", place(cp.bush(32.0, 25.4, 30.0), (sx, sy, z0), (0, 0, 1)), "brass", "bought", 6, "sheave", (0, 0, 150)))
        sp = cp.round_tube(40.0, 7.25, 20.0) - Cylinder(16.5, 8.0).moved(Pos(0, 0, 4.0)) if False else cp.round_tube(40.0, 7.25, 20.0) - Pos(0, 0, 2.0) * Cylinder(16.5, 4.0)
        out.append(mk("Sheave spacer, 40 x 7.25 tube, 20 long", place(sp, (sx, sy, zt), (0, 0, 1)), "mild_steel", "made", 7, "sheave_hw", (0, 0, 200)))
        kp = extrude(Sketch() + Circle(22.0) - Circle(12.75), 5.0)
        out.append(mk("Sheave keeper washer, 44 x 5", Pos(sx, sy, z0 + 30) * break_edges(kp, 0.5), "mild_steel", "made", 7, "sheave_hw", (0, 0, 200)))
        out.append(mk("R-clip (split pin) through the pin cross hole", Pos(sx, sy, zt + 62.0) * cp.split_pin(18.75), ZP, "fastener", 7, "sheave_hw", (0, 0, 200)))
        # cover and kneeling plate
        cx0, cx1, cy0, cy1, ct = P["cover"]
        ccx, ccy = Lp + (cx0 + cx1) / 2, (cy0 + cy1) / 2
        holes = [(Lp + x - ccx, y - ccy, 9.0) for x in (px0, px1) for y in (py0, py1)]
        out.append(mk("Sheave cover and kneeling plate, 4 mm chequer plate", Pos(ccx, ccy, P["cover_z"]) * cp.sheet(cx1 - cx0, cy1 - cy0, ct, holes, r_corner=6.0),
                      ST, "made", 8, "cover", (0, 0, 350)))
        for x in (px0, px1):
            for y in (py0, py1):
                zt_c = P["cover_z"] + ct
                wsh = place(cp.washer(8), (Lp + x, y, zt_c), (0, 0, 1))
                out.append(mk("M8 washer (ISO 7089)", wsh, ZP, "fastener", 8, "cover"))
                out.append(mk("M8 x 20 cover screw (ISO 4017)", place(cp.hex_bolt(8, 20), (Lp + x, y, zt_c + cp.ISO[8][4]), (0, 0, 1)), ZP, "fastener", 8, "cover"))
    # duct spigot, saddles, clamps
    cy, cz = at_ring(P["zc"], P["duct_r"], P["duct_th"], 0)[1:]
    sp_r = P["spigot"][0] / 2
    s0, s1 = P["spigot_x"]
    tube = place(cp.round_tube(P["spigot"][0], P["spigot"][1], s1 - s0), (Lp + s0, cy, cz), (1, 0, 0))
    bead_r = place(extrude(Sketch() + Circle(98.2) - Circle(sp_r - 0.5), 4.0), (Lp + s0 + 20, cy, cz), (1, 0, 0))
    out.append(mk("Duct outlet spigot, 194 x 2 steel tube with rolled bead", tube + bead_r, ST, "made", 9, "spigot", (-500, 0, 250)))
    for i, x0 in enumerate((-150.0, -30.0)):
        disc = xcyl(cy, cz, P["saddle_r"], Lp + x0, Lp + x0 + P["saddle_t"])
        inside = xcyl(0, zr, ri - 0.25, Lp + x0 - 1, Lp + x0 + P["saddle_t"] + 1)
        bore = xcyl(cy, cz, sp_r + 0.5, Lp + x0 - 1, Lp + x0 + P["saddle_t"] + 1)
        out.append(mk(f"Spigot saddle {i + 1}, 25 mm plate", break_edges(disc & inside - bore, 0.5), ST, "made", 3, "crown"))
    for i, x in enumerate((-340.0, -320.0)):
        cl = place(extrude(Sketch() + Circle(103.0) - Circle(100.05), 12.0), (Lp + x - 6, cy, cz), (1, 0, 0))
        hs = Pos(Lp + x, cy + 106.0, cz) * Box(12, 10, 12)
        out.append(mk(f"Band clamp {i + 1}, worm drive, 180 to 200 mm", cl + hs, "stainless", "fastener", 9, "spigot"))
    # magnetic lamp inside the hood
    lamp = cp.round_bar(60.0, 40.0, 3.0) - Pos(0, 0, 38.5) * Cylinder(24.0, 3.0)
    out.append(mk("Magnetic LED work lamp, 1,000 lm", place(lamp, at_ring(zr, ri - 41.3, -30.0, Lp + 120), _tup(e_r(-30.0))), "matte_black", "bought", 23, "lamp", (0, 0, 900)))
    return out


# ----------------------------------------------------------------------------- the train: sledges, links, swivels, ropes
def _tray_pts(P, z0):
    w0, w1 = P["sledge_w"]
    h, t = P["sledge_h"], P["sheet"]
    k = (w1 - w0) / 2 / h

    def half(z):
        return w0 / 2 - t + k * (z - z0 - t)          # inner half width at height z
    return k, half


def sledge_parts(P, x0, tag, bom=True, group="sledges", runners=True):
    """One spoil sledge from x0 (portal end) to x0 + L: folded tray, two welded end plates, lugs, runners with
    countersunk screws and nuts."""
    D = derived(P)
    L = P["sledge_L"]
    w0, w1 = P["sledge_w"]
    h, t = P["sledge_h"], P["sheet"]
    z0 = D["sledge_z0"]
    k, half = _tray_pts(P, z0)
    B = (lambda n: n) if bom else (lambda n: None)
    outer = [(-w0 / 2, z0), (w0 / 2, z0), (w1 / 2, z0 + h), (-w1 / 2, z0 + h)]
    ztop = z0 + h
    inner = [(-half(z0 + t), z0 + t), (half(z0 + t), z0 + t), (half(ztop + 10), ztop + 10), (-half(ztop + 10), ztop + 10)]
    runner_x = [x0 + v for v in P["runner_screws"]]
    rw, rt, ry = P["runner"]
    zr = P["runner_z"]
    csk_d, csk_len, csk_hd, csk_hh = P["csk"]
    tray = prism_yz(outer, x0, x0 + L) - prism_yz(inner, x0 - 1, x0 + L + 1)
    for x in (runner_x if runners else []):
        for y in (-ry, ry):
            tray = tray - zcyl(x, y, 3.3, z0 - 1, z0 + t + 1)
    out = [mk(f"Sledge tray {tag}, 1.5 mm galvanised sheet, folded", break_edges(tray, 0.4), GALV, "made", B(10), group)]
    ip = [(-half(z0 + t), z0 + t), (half(z0 + t), z0 + t), (half(ztop), ztop), (-half(ztop), ztop)]
    for side, xe in (("portal", x0), ("face", x0 + L - t)):
        pl = prism_yz(ip, xe, xe + t) - bx(xe - 1, xe + t + 1, -50, 50, z0 + 95, z0 + 135)
        out.append(mk(f"Sledge {tag} {side} end plate, 1.5 mm galvanised", pl, GALV, "made", B(10), group))
        xin = xe + t if side == "portal" else xe
        out.append(mk(f"Weld, sledge {tag} {side} end plate to floor",
                      bead((xin, -half(z0 + t), z0 + t), (0, 1, 0), 2 * half(z0 + t), 3.0, (0, 0, 1), (1 if side == "portal" else -1, 0, 0)),
                      GALV, "weld", B(10), group))
    lp, lt, lh = P["lug"]
    zl = D["lug_z"]
    for side, xe, sg in (("portal", x0, -1), ("face", x0 + L, 1)):
        xa, xb = (xe - lp, xe) if sg < 0 else (xe, xe + lp)
        lug = bx(xa, xb, -lt / 2, lt / 2, zl - lh / 2, zl + lh / 2) - ycyl(xe + sg * 30, zl, P["lug_hole"] / 2, -10, 10)
        out.append(mk(f"Sledge {tag} {side} lug, 8 mm plate", break_edges(lug, 0.8), ST, "made", B(10), group))
        ws = [bead((xe, ys * lt / 2, zl - lh / 2), (0, 0, 1), lh, 3.0, (0, ys, 0), (sg, 0, 0)) for ys in (1, -1)]
        out.append(mk(f"Weld, sledge {tag} {side} lug", Compound(ws), ST, "weld", B(10), group))
    for ys, sd in (((-1, "left"), (1, "right")) if runners else ()):
        yc = ys * ry
        r = bx(x0, x0 + L, yc - rw / 2, yc + rw / 2, zr, zr + rt)
        for x in runner_x:
            r = (r - zcyl(x, yc, 6.5, zr - 1, zr + 4.0) - Pos(x, yc, zr + 4.0) * Solid.make_cone(6.2, 3.3, csk_hh)
                 - zcyl(x, yc, 3.3, zr + 4.0, zr + rt + 1))
        out.append(mk(f"Sledge {tag} runner {sd}, UHMW-PE 40 x 10", break_edges(r, 0.8), UH, "bought", B(11), "runners"))
        for x in runner_x:
            sc = place(csk_screw(csk_d, csk_len, csk_hd, csk_hh), (x, yc, zr + 4.0), (0, 0, -1))
            out.append(mk("M6 countersunk screw, stainless", sc, "stainless", "fastener", B(11), "runners"))
            zb = z0 + t
            out.append(mk("M6 washer (ISO 7089)", place(cp.washer(6), (x, yc, zb), (0, 0, 1)), ZP, "fastener", B(11), "runners"))
            out.append(mk("M6 hex nut (ISO 4032)", place(cp.hex_nut(6), (x, yc, zb + cp.ISO[6][4]), (0, 0, 1)), ZP, "fastener", B(11), "runners"))
    return out


def train_layout(P, Lp, n=None):
    xe = Lp - P["train_gap"]
    return [xe - P["sledge_L"] - k * (P["sledge_L"] + P["sledge_gap"]) for k in range(n or P["n_sledges"])]


def _clevis(x, y_head, zl, direction, grip, bom, group, label):
    """Clevis pin of 14 mm through a lug hole, its head on the -Y side (direction +1 = shank toward +Y)."""
    frame = dict(origin=(x, y_head, zl), zdir=(0, -direction, 0), xdir=(0, 0, 1))
    pin = place(cp.clevis_pin(14, grip), frame["origin"], frame["zdir"], frame["xdir"])
    spl = place(Pos(0, 0, -grip - 14) * cp.split_pin(14), frame["origin"], frame["zdir"], frame["xdir"])
    return [mk(f"Clevis pin 14 mm (ISO 2341), {label}", pin, ZP, "fastener", bom, group),
            mk(f"Split pin (ISO 1234), {label}", spl, ZP, "fastener", bom, group)]


def link_parts(P, xa, xb, tag, bom=True, group="links"):
    """Connecting link between lug holes at xa < xb: two 8 mm side bars, two clevis pins with split pins."""
    D = derived(P)
    zl = D["lug_z"]
    B = 12 if bom else None
    out = []
    for ys in (-1, 1):
        bar = place(cp.flat_bar(20.0, 8.0, xb - xa + 40.0), (xa - 20.0, ys * 11.5, zl), (1, 0, 0), (0, 0, 1))
        bar = bar - ycyl(xa, zl, 7.2, ys * 11.5 - 6, ys * 11.5 + 6) - ycyl(xb, zl, 7.2, ys * 11.5 - 6, ys * 11.5 + 6)
        out.append(mk(f"Link {tag} side bar, 8 mm flat", break_edges(bar, 0.5), ST, "made" if bom else "made", B, group))
    for x, nm in ((xa, "front"), (xb, "rear")):
        out += _clevis(x, -15.5, zl, 1, 31.0, B, group, f"link {tag} {nm}")
    return out


def swivel_parts(P, x_hole, direction, tag, bom=True, group="swivels"):
    """Breakaway swivel: fork on a clevis pin through the lug hole, body with a shear pin, eye for the rope.
    direction +1 points toward the face, -1 toward the portal. Returns (parts, x of the eye centre)."""
    D = derived(P)
    zl = D["lug_z"]
    d = direction
    B = 13 if bom else None
    xb = x_hole + 30 * d
    xb2 = xb + 150 * d
    body = place(cp.round_bar(28.0, 150.0, 1.5), (xb, 0, zl), (d, 0, 0))
    body = body - Pos((xb + xb2) / 2, 0, zl) * Rot(90, 0, 0) * Cylinder(3.0, 40)
    fx0, fx1 = min(x_hole - 12, xb), max(x_hole + 12, xb)
    if d > 0:
        fx0, fx1 = x_hole - 12, xb
    else:
        fx0, fx1 = xb, x_hole + 12
    fork = Compound([bx(fx0, fx1, ys * 10 - 2 + 0, ys * 10 + 2, zl - 10, zl + 10) for ys in (-1, 1)])
    fork = fork - ycyl(x_hole, zl, 7.2, -14, 14)
    eye_c = xb2 + 19 * d
    from build123d import Torus
    eye = Pos(eye_c, 0, zl) * Rot(90, 0, 0) * Torus(14.0, 5.0)
    out = [mk(f"Breakaway swivel {tag}, 2.5 kN, fork and body", Compound([fork, body, eye]), "stainless", "bought", B, group, (0, 0, 250))]
    out += _clevis(x_hole, -15.5, zl, 1, 24.0 + 7.0, B, group, f"swivel {tag}")
    out.append(mk(f"Shear pin 6 mm, swivel {tag}", Pos((xb + xb2) / 2, 0, zl) * Rot(90, 0, 0) * Cylinder(3.0, 40), "brass", "fastener", B, group))
    return out, eye_c


def lift(parts, dz):
    return [dict(p, shape=Pos(0, 0, dz) * p["shape"]) for p in parts] if dz else parts


def haul_parts(P=PARAMS, Lp=None, xs=None, bom=True, n=None, runners=True, dz=0.0, wagon=None):
    """Sledges (or wagons), links, swivels and ropes with the train at the face (options A and B)."""
    D = derived(P)
    xs_list = train_layout(P, Lp, n)
    out = []
    for k, x0 in enumerate(xs_list):
        out += lift(sledge_parts(P, x0, str(k + 1), bom, "sledges", runners), dz)
        if wagon:
            out += wagon(P, x0, str(k + 1))
    for k in range(len(xs_list) - 1):
        xa = xs_list[k + 1] + P["sledge_L"] + 30
        xb = xs_list[k] - 30
        out += lift(link_parts(P, xa, xb, str(k + 1), bom), dz)
    sw_face, x_tail = swivel_parts(P, xs_list[0] + P["sledge_L"] + 30, +1, "face end", bom)
    sw_port, x_pull = swivel_parts(P, xs_list[-1] - 30, -1, "portal end", bom)
    out += lift(sw_face + sw_port, dz)
    out += rope_parts(P, Lp, xs, x_tail, x_pull, bom, dz=dz)
    return out


def rope_parts(P, Lp, xs, x_tail, x_pull, bom=True, tail=True, dz=0.0):
    D = derived(P)
    zl = D["lug_z"] + dz
    r = P["rope_d"] / 2
    sx, sy = Lp + P["sheave_c"][0], P["sheave_c"][1]
    pr = D["sheave_pitch_r"]
    zr = P["rope_z"]
    yA, yB = P["winch_y"]
    xw = xs + P["winch_x"]
    rr = D["drum_rope_r"]
    zf0 = D["rope_floor_z"][0.0]
    zfr = D["rope_floor_z"][P["ret_y"]]
    hz = P["rope_hz"]
    B = (lambda n: n) if bom else (lambda n: None)
    wrap = lambda y: zcyl(xw, y, rr + r, hz - 15, hz + 15) - zcyl(xw, y, P["winch"][2], hz - 16, hz + 16)  # noqa: E731
    pull = [(xw, yA + rr, hz), (0.0, 0.0, zf0), (x_pull - 600, 0.0, zf0), (x_pull, 0.0, zl)]
    out = [mk("Pull rope, 10 mm polyester double braid, 75 m", Compound([cp.rope(pull, P["rope_d"]), wrap(yA)]), ROPE, "bought", B(14), "ropes")]
    if tail:
        arc = [(sx + pr * math.sin(math.radians(a)), sy - pr * math.cos(math.radians(a)), zr) for a in range(0, 181, 10)]
        tl = [(x_tail, 0.0, zl), (sx, sy - pr, zr)] + arc[1:] + [(Lp - 1200.0, P["ret_y"], zfr), (0.0, P["ret_y"], zfr), (xw, yB - rr, hz)]
        out.append(mk("Tail rope, 10 mm polyester double braid, 140 m", Compound([cp.rope(tl, P["rope_d"]), wrap(yB)]), ROPE, "bought", B(14), "ropes"))
    return out


# ----------------------------------------------------------------------------- portal haul station
def _shs_member(P, x0, x1, y0, y1, z0, z1, axis, name, bom, holes=()):
    a, t = P["shs"]
    if axis == "x":
        sh = place(cp.shs(a, t, x1 - x0), (x0, (y0 + y1) / 2, (z0 + z1) / 2), (1, 0, 0))
    elif axis == "y":
        sh = place(cp.shs(a, t, y1 - y0), ((x0 + x1) / 2, y0, (z0 + z1) / 2), (0, 1, 0))
    else:
        sh = place(cp.shs(a, t, z1 - z0), ((x0 + x1) / 2, (y0 + y1) / 2, z0), (0, 0, 1))
    for h in holes:
        sh = sh - h
    return mk(name, sh, ST, "made", bom, "trestles")


def _sq_ring(cx, cy, cz, axis, size, leg):
    """Square weld collar of thickness leg round a square section of side size, its centre at (cx, cy, cz)."""
    o, i = size + 2 * leg, size + 0.4
    if axis == "x":
        return bx(cx, cx + leg, cy - o / 2, cy + o / 2, cz - o / 2, cz + o / 2) - bx(cx - 1, cx + leg + 1, cy - i / 2, cy + i / 2, cz - i / 2, cz + i / 2)
    if axis == "y":
        return bx(cx - o / 2, cx + o / 2, cy, cy + leg, cz - o / 2, cz + o / 2) - bx(cx - i / 2, cx + i / 2, cy - 1, cy + leg + 1, cz - i / 2, cz + i / 2)
    return bx(cx - o / 2, cx + o / 2, cy - o / 2, cy + o / 2, cz, cz + leg) - bx(cx - i / 2, cx + i / 2, cy - i / 2, cy + i / 2, cz - 1, cz + leg + 1)


def tie_x(P, xs):
    L = P["trestle"][0]
    return [xs - L / 2 - 150, xs - L / 2 + 150]


def trestle_parts(P, xs, yc, tag, bom=True):
    """Welded winch trestle: SHS base and top rectangles, four posts, top plate with its holes, anchor eye."""
    L, W, H = P["trestle"]
    s, t = P["shs"]
    B = (lambda n: n) if bom else (lambda n: None)
    x0, x1 = xs - L, xs
    y0, y1 = yc - W / 2, yc + W / 2
    inner_side = +1 if yc < 0 else -1                     # trestle A (y < 0) has its inner long rail on the +Y side
    ry_inner = (y1 - s, y1) if inner_side > 0 else (y0, y0 + s)
    out = []
    ties_x = tie_x(P, xs)
    n = 0
    for zl_, zh_, lvl in ((0.0, s, "base"), (H - s, H, "top")):
        zc_ = (zl_ + zh_) / 2
        for ysd, (ya, yb) in (("rail y-", (y0, y0 + s)), ("rail y+", (y1 - s, y1))):
            holes = []
            if (ya, yb) == ry_inner:
                holes = [ycyl(x, zc_, 5.5, ya - 1, yb + 1) for xt in ties_x for x in (xt - 30, xt + 30)]
            out.append(_shs_member(P, x0, x1, ya, yb, zl_, zh_, "x", f"Trestle {tag} {lvl} long {ysd}, 40 x 40 x 3 SHS", B(15), holes))
        for xsd, (xa, xb) in (("x-", (x0, x0 + s)), ("x+", (x1 - s, x1))):
            out.append(_shs_member(P, xa, xb, y0 + s, y1 - s, zl_, zh_, "y", f"Trestle {tag} {lvl} short {xsd}, 40 x 40 x 3 SHS", B(15)))
    for i, (xa, ya) in enumerate(((x0, y0), (x0, y1 - s), (x1 - s, y0), (x1 - s, y1 - s))):
        out.append(_shs_member(P, xa, xa + s, ya, ya + s, s, H - s, "z", f"Trestle {tag} post {i + 1}, 40 x 40 x 3 SHS", B(15)))
    # welds: posts to rails, short rails to long rails (square collars)
    wp, wr = [], []
    for i, (xa, ya) in enumerate(((x0, y0), (x0, y1 - s), (x1 - s, y0), (x1 - s, y1 - s))):
        cx, cy = xa + s / 2, ya + s / 2
        wp.append(_sq_ring(cx, cy, s + 0.2, "z", s, 3.0))
        wp.append(_sq_ring(cx, cy, H - s - 3.2, "z", s, 3.0))
    for zl_, zh_ in ((0.0, s), (H - s, H)):
        zc_ = (zl_ + zh_) / 2
        for xa in (x0 + s / 2, x1 - s / 2):
            wr.append(_sq_ring(xa, y0 + s + 0.2, zc_, "y", s, 3.0))
            wr.append(Pos(0, 0, 0) * (_sq_ring(xa, y1 - s - 3.2, zc_, "y", s, 3.0)))
    out.append(mk(f"Welds, trestle {tag} posts to rails", Compound(wp), ST, "weld", B(15), "trestles"))
    out.append(mk(f"Welds, trestle {tag} short rails to long rails", Compound(wr), ST, "weld", B(15), "trestles"))
    # top plate drilled for the winch base bolts and the guard feet
    tp = P["top_plate"]
    xwc = xs + P["winch_x"]
    holes = [(dx, dy, 11.0) for dx in (-53.0, 53.0) for dy in (-53.0, 53.0)]
    for (gx, gy) in guard_feet(P, xs, yc):
        holes.append((gx - xwc, gy - yc, 9.0))
    plate = Pos(xwc, yc, H) * cp.sheet(tp[0], tp[1], tp[2], holes, r_corner=6.0)
    out.append(mk(f"Trestle {tag} top plate, 10 mm S355, drilled for the winch base", plate, ST, "made", B(15), "trestles", (0, 0, 120)))
    ws = [bead((xwc + sx_ * tp[0] / 2, ya, H), (0, 1, 0), s, 4.0, (0, 0, 1), (sx_, 0, 0)) for sx_ in (-1, 1) for ya in (y0, y1 - s)]
    out.append(mk(f"Welds, trestle {tag} top plate to rails", Compound(ws), ST, "weld", B(15), "trestles"))
    # anchor eye on the rear top rail
    ep = P["eye_plate"]
    eye = cp.sheet(ep[0], ep[2] + s, ep[1], [(0.0, -((H + 80.0) - (H - s + H + 110.0) / 2), P["eye_hole"])], r_corner=25.0)
    zc_e = (H - s + H + 110.0) / 2
    out.append(mk(f"Trestle {tag} anchor eye plate, 10 mm S355, 22 mm hole", place(eye, (x0 - ep[0] / 2, yc - ep[1] / 2, zc_e), (0, 1, 0), (1, 0, 0)), ST, "made", B(15), "trestles"))
    we = [bead((x0, yc + ys * ep[1] / 2, H - s), (0, 0, 1), s, 4.0, (0, ys, 0), (-1, 0, 0)) for ys in (-1, 1)]
    out.append(mk(f"Welds, trestle {tag} anchor eye", Compound(we), ST, "weld", B(15), "trestles"))
    return out


def guard_feet(P, xs, yc):
    """Positions of the two guard foot bolts (x, y) round the winch whose trestle centre is yc."""
    xw = xs + P["winch_x"]
    r, t, z0, z1, span = P["guard"]
    res = []
    for a_deg in (180 - span / 2 + 10, 180 + span / 2 - 10):
        a = math.radians(a_deg)
        res.append((xw + 142.0 * math.cos(a), yc + 142.0 * math.sin(a)))
    return res


def winch_parts(P, xc, yc, tag, bom=True):
    B = (lambda n: n) if bom else (lambda n: None)
    rb, hb, rd, hd, rt, ht = P["winch"]
    z = P["trestle"][2] + P["top_plate"][2]
    base = zcyl(xc, yc, rb, z, z + hb)
    for dx in (-53.0, 53.0):
        for dy in (-53.0, 53.0):
            base = base - zcyl(xc + dx, yc + dy, 5.5, z - 1, z + hb + 1)
    drum = zcyl(xc, yc, rd, z + hb, z + hb + hd)
    tail = zcyl(xc, yc, rt, z + hb + hd, z + hb + hd + ht)
    sock = zcyl(xc, yc, 12, z + hb + hd + ht, z + hb + hd + ht + 20)
    wi = break_edges(base + drum + tail + sock, 1.5)
    out = [mk(f"Self-tailing winch {tag}, two-speed", wi, "aluminium", "bought", B(17), "winches", (0, 0, 500))]
    for dx in (-53.0, 53.0):
        for dy in (-53.0, 53.0):
            for nm_, sh in cp.hex_bolt_set(10, hb + P["top_plate"][2]):
                out.append(mk(nm_ + f", winch {tag} base", place(sh, (xc + dx, yc + dy, z + hb), (0, 0, 1)), ZP, "fastener", B(17), "winches"))
    return out


def socket_top(P):
    rb, hb, rd, hd, rt, ht = P["winch"]
    return P["trestle"][2] + P["top_plate"][2] + hb + hd + ht + 20


def drill_parts(P, xc, yc, side, tag, bom=True):
    B = (lambda n: n) if bom else (lambda n: None)
    zs = socket_top(P)
    rbit, hbit = P["bit"]
    bit = break_edges(zcyl(xc, yc, rbit, zs, zs + hbit), 1.0)
    rh, hh = P["drill_head"]
    z0 = zs + hbit
    head = break_edges(zcyl(xc, yc, rh, z0, z0 + hh), 2.0)
    rbd, lbd = P["drill_body"]
    zb = z0 + hh / 2
    y1 = yc + side * (rh - 5)
    y2 = y1 + side * lbd
    body = break_edges(ycyl(xc, zb, rbd, min(y1, y2), max(y1, y2)), 2.0)
    lb, wb, hb_ = P["drill_batt"]
    ya, yb = sorted((y2 - side * lb, y2))
    batt = break_edges(bx(xc - wb / 2, xc + wb / 2, ya, yb, zb - rbd - hb_ - 0.3, zb - rbd - 0.3), 3.0)
    return [mk(f"Winch bit {tag}, hex shank to winch socket", bit, "mild_steel", "bought", B(31), "bits", (0, 0, 1100)),
            mk(f"Right-angle drill {tag}, 18 V, slip clutch", head + body, "safety_red", "bought", B(30), "drills", (0, 0, 1100)),
            mk(f"Drill battery {tag}, 5 Ah", batt, "matte_black", "bought", B(30), "drills", (0, 0, 1100))]


def guard_parts(P, xs, xc, yc, tag, bom=True):
    B = (lambda n: n) if bom else (lambda n: None)
    r, t, z0, z1, span = P["guard"]
    zp = P["trestle"][2] + P["top_plate"][2]
    pts_o, pts_i = [], []
    for k in range(25):
        a = math.radians(180 - span / 2 + span * k / 24)
        pts_o.append((xc + r * math.cos(a), yc + r * math.sin(a)))
        pts_i.append((xc + (r - t) * math.cos(a), yc + (r - t) * math.sin(a)))
    hoop = extrude(Plane.XY.offset(z0) * Polygon(*_ccw(pts_o + pts_i[::-1]), align=None), amount=z1 - z0)
    holes = []
    for row in range(3):
        for col in range(11):
            a = math.radians(180 - span / 2 + 8 + (span - 16) * col / 10)
            holes.append(place(Cylinder(5.0, 8.0), (xc + (r - 1) * math.cos(a), yc + (r - 1) * math.sin(a), z0 + 35 + 52 * row),
                               (math.cos(a), math.sin(a), 0)))
    hoop = hoop - Compound(holes)
    out = [mk(f"Winch drum guard {tag}, 2 mm perforated sheet hoop", hoop, "galvanised", "made", B(33), "guards", (0, 0, 800))]
    w, tl = P["guard_leg"]
    feet = guard_feet(P, xs, yc)
    for i, a_deg in enumerate((180 - span / 2 + 10, 180 + span / 2 - 10)):
        a = math.radians(a_deg)
        rl = r - t - 1.0 - tl / 2
        hleg = z0 + 20 - zp - 5.0
        leg = Pos(0, 0, 0) * Rot(0, 0, a_deg) * Pos(rl, 0, zp + 5.0 + hleg / 2) * Box(tl, w, hleg)
        foot = Rot(0, 0, a_deg) * Pos(rl + tl / 2 + 15.0, 0, zp + 2.5) * Box(30, w, 5.0)
        foot = foot - Rot(0, 0, a_deg) * Pos(142.0, 0, zp) * Cylinder(4.5, 12)
        lf = Pos(xc, yc, 0) * (break_edges(leg + foot, 0.5))
        out.append(mk(f"Drum guard {tag} leg {i + 1}, 30 x 5 flat with foot", lf, ST, "made", B(33), "guards", (0, 0, 800)))
        fx, fy = feet[i]
        for nm_, sh in cp.hex_bolt_set(8, 5.0 + P["top_plate"][2]):
            out.append(mk(nm_ + f", guard {tag} foot", place(sh, (fx, fy, zp + 5.0), (0, 0, 1)), ZP, "fastener", B(33), "guards"))
    return out


def tie_parts(P, xs, xt, z_level, tag, bom=True):
    """One cross tie between the two trestles at station xt and level z_level (0 or H - 40)."""
    B = (lambda n: n) if bom else (lambda n: None)
    yA, yB = P["winch_y"]
    W = P["trestle"][1]
    s, t = P["shs"]
    ya1, yb0 = yA + W / 2, yB - W / 2
    tl, pt, pw = P["tie"]
    zc_ = z_level + s / 2
    out = []
    pA = cp.sheet(pw, s, pt, [(-30.0, 0.0, 11.0), (30.0, 0.0, 11.0)], r_corner=4.0)
    pB = pA
    out.append(mk(f"Cross tie {tag} end plate A, 6 mm", place(pA, (xt, ya1, zc_), (0, 1, 0), (1, 0, 0)), ST, "made", B(16), "ties"))
    out.append(mk(f"Cross tie {tag} end plate B, 6 mm", place(pB, (xt, yb0 - pt, zc_), (0, 1, 0), (1, 0, 0)), ST, "made", B(16), "ties"))
    out.append(mk(f"Cross tie {tag} tube, 40 x 40 x 3 SHS", place(cp.shs(s, t, yb0 - ya1 - 2 * pt), (xt, ya1 + pt, zc_), (0, 1, 0)), ST, "made", B(16), "ties"))
    ws = []
    for yy, dy in ((ya1 + pt, 1), (yb0 - pt, -1)):
        for dz in (-1, 1):
            ws.append(bead((xt - s / 2, yy, zc_ + dz * s / 2), (1, 0, 0), s, 3.0, (0, dy, 0), (0, 0, dz)))
    out.append(mk(f"Welds, cross tie {tag} tube to end plates", Compound(ws), ST, "weld", B(16), "ties"))
    for dx in (-30.0, 30.0):
        for nm_, sh in cp.hex_bolt_set(10, pt + s):
            out.append(mk(nm_ + f", tie {tag} end A", place(sh, (xt + dx, ya1 + pt, zc_), (0, 1, 0)), ZP, "fastener", B(16), "ties"))
        for nm_, sh in cp.hex_bolt_set(10, pt + s):
            out.append(mk(nm_ + f", tie {tag} end B", place(sh, (xt + dx, yb0 - pt, zc_), (0, -1, 0)), ZP, "fastener", B(16), "ties"))
    return out


def station_parts(P=PARAMS, xs=None, bom=True, drills=True):
    """Portal haul station: two trestles, ties, two winches with drills and drum guards, bins, slings."""
    B = (lambda n: n) if bom else (lambda n: None)
    yA, yB = P["winch_y"]
    L, W, H = P["trestle"]
    s = P["shs"][0]
    xw = xs + P["winch_x"]
    out = trestle_parts(P, xs, yA, "A", bom) + trestle_parts(P, xs, yB, "B", bom)
    n = 0
    for xt in tie_x(P, xs):
        for zlv in (0.0, H - s):
            n += 1
            out += tie_parts(P, xs, xt, zlv, str(n), bom)
    out += winch_parts(P, xw, yA, "A", bom) + winch_parts(P, xw, yB, "B", bom)
    if drills:
        out += drill_parts(P, xw, yA, -1, "A", bom) + drill_parts(P, xw, yB, +1, "B", bom)
    out += guard_parts(P, xs, xw, yA, "A", bom) + guard_parts(P, xs, xw, yB, "B", bom)
    for tag, y in (("A", yA - W / 2 - 320), ("B", yB + W / 2 + 320)):
        tub = zcyl(xs - L / 2, y, 250, 0, 400) - zcyl(xs - L / 2, y, 245, 5, 401)
        rim = zcyl(xs - L / 2, y, 256, 392, 400) - zcyl(xs - L / 2, y, 245, 391, 401)
        out.append(mk(f"Rope bin {tag}, 80 L plastic tub", break_edges(tub + rim, 1.5), PL, "bought", B(18), "bins"))
    x0 = xs - L
    for tag, y in (("A", yA), ("B", yB)):
        zh = H + 80.0
        pin = cp.round_bar(16.0, 26.0, 1.0)
        out.append(mk(f"Sling shackle pin {tag}", place(pin, (x0 - 30, y - 13, zh), (0, 1, 0)), "stainless", "bought", B(19), "sling"))
        bow = (bx(x0 - 75, x0 - 40, y + 7, y + 11, zh - 14, zh + 14) + bx(x0 - 75, x0 - 40, y - 11, y - 7, zh - 14, zh + 14)
               + bx(x0 - 85, x0 - 75, y - 11, y + 11, zh - 14, zh + 14))
        out.append(mk(f"Sling bow shackle body {tag}", break_edges(bow, 1.5), "stainless", "bought", B(19), "sling"))
        out.append(mk(f"Round sling {tag}, 1 t, 2 m", cp.rope([(x0 - 85, y, zh), (x0 - 1500, y, zh)], 14.0), "rope", "bought", B(19), "sling"))
    return out


# ----------------------------------------------------------------------------- air and signal line
def air_parts(P=PARAMS, Lp=None, xs=None, bom=True, hangers=True):
    B = (lambda n: n) if bom else (lambda n: None)
    D = derived(P)
    c = at_ring(P["zc"], P["duct_r"], P["duct_th"], 0)
    rd = P["duct_d"] / 2
    s0 = P["spigot_x"][0]
    out = []
    xe = Lp + s0 + 60
    duct_in = place(extrude(Sketch() + Circle(rd) - Circle(rd - 1.5), xe + 300.0), (-300.0, c[1], c[2]), (1, 0, 0))
    out.append(mk("Layflat duct 200 mm, inside the pipe", duct_in, "epdm", "bought", B(21), "duct"))
    out[-1]["color"] = "#E3B21C"
    bxy = P["blower_xy"]
    a = (bxy[0] + 400, bxy[1], 220.0)
    b = (-300.0, c[1], c[2])
    outside = rod(a, b, rd) - rod(a, b, rd - 1.5)
    out.append(mk("Layflat duct 200 mm, portal run to the blower", outside, "epdm", "bought", B(21), "duct"))
    out[-1]["color"] = "#E3B21C"
    hous = (xcyl(bxy[1], 220, 170, bxy[0] - 250, bxy[0] + 200) + xcyl(bxy[1], 220, 100, bxy[0] + 200, bxy[0] + 400)
            - xcyl(bxy[1], 220, 167, bxy[0] - 251, bxy[0] + 200) - xcyl(bxy[1], 220, 97, bxy[0] + 199, bxy[0] + 401))
    hous = break_edges(hous, 1.0)
    out.append(mk("Ventilation blower 200 mm, 230 V, housing", hous, "safety_yellow", "bought", B(20), "blower"))
    out.append(mk("Blower stand", break_edges(bx(bxy[0] - 220, bxy[0] + 170, bxy[1] - 150, bxy[1] + 150, 0, 50), 3.0), ST, "bought", B(20), "blower"))
    guard = place(extrude(Sketch() + Circle(172.0) - Circle(160.0), 6.0), (bxy[0] - 256, bxy[1], 220), (1, 0, 0))
    bars = Compound([place(cp.round_bar(5.0, 320.0, 0.5), (bxy[0] - 256, bxy[1], 220 + d), (0, 1, 0)).moved(Pos(0, -160, 0)) for d in (-100, -50, 0, 50, 100)])
    out.append(mk("Blower intake guard", guard + bars, "galvanised", "bought", B(20), "blower"))
    if hangers:
        pid = D["pipe_id"] / 2
        x = 1250.0
        i = 0
        while x < Lp - 600:
            i += 1
            e = e_r(P["duct_th"])
            mag = place(cp.round_bar(32.0, 12.6, 1.5), tuple(Vector(*at_ring(P["zc"], pid - 13, P["duct_th"], x))), (e.X, e.Y, e.Z))
            out.append(mk(f"Pot magnet {i} for the duct", mag, "mild_steel", "bought", B(22), "hangers"))
            hook = place(cp.round_bar(6.0, 12.0, 0.6), tuple(Vector(*at_ring(P["zc"], P["duct_r"] + rd, P["duct_th"], x))), (e.X, e.Y, e.Z))
            out.append(mk(f"Duct hook {i}", hook, "mild_steel", "bought", B(22), "hangers"))
            e2 = e_r(P["cable_th"])
            mag2 = place(cp.round_bar(24.0, 10.0, 1.2), tuple(Vector(*at_ring(P["zc"], pid - 10.4, P["cable_th"], x))), (e2.X, e2.Y, e2.Z))
            out.append(mk(f"Pot magnet {i} for the cable", mag2, "mild_steel", "bought", B(22), "hangers"))
            x += P["hanger_pitch"]
    rc = D["pipe_id"] / 2 - 10.4 - P["cable_d"] / 2
    cc = at_ring(P["zc"], rc, P["cable_th"], 0)
    out.append(mk("Signal cable, two-core, for the sound-powered telephones", place(cp.round_bar(P["cable_d"], Lp - 400 + 200.0, 1.0), (-200.0, cc[1], cc[2]), (1, 0, 0)), "epdm", "bought", B(24), "cable"))
    return out


def casualty_parts(P=PARAMS, x0=-2600.0, y=-1450.0, bom=True, spreader=True):
    """Roll-up casualty stretcher (bought), shown wrapped, with the towing spreader bar and bridle (made)."""
    B = (lambda n: n) if bom else (lambda n: None)
    L, R, t = P["stretcher"]
    zc = R + 1.0
    shell = (xcyl(y, zc, R, x0, x0 + L) - xcyl(y, zc, R - t, x0 - 1, x0 + L + 1)) & bx(x0, x0 + L, y - R, y + R, 0, zc + 40)
    out = [mk("Roll-up casualty stretcher, rolled", break_edges(shell, 0.8), "hdpe_black", "bought", B(26), "stretcher")]
    out[0]["color"] = "#B3261E"
    if not spreader:
        return out
    od, w, l = P["spreader"]
    xb = x0 + L + 250
    bar = place(cp.round_tube(od, w, l), (xb, y - l / 2, 120.0), (0, 1, 0))
    for sg in (-1, 1):
        bar = bar - Pos(xb, y + sg * (l / 2 - 20), 120.0) * Cylinder(5.0, 40.0)
    out.append(mk("Stretcher towing spreader bar, 26.9 x 2.6 tube", bar, ST, "made", B(27), "spreader"))
    eye = place(cp.sheet(75.0, 30.0, 10.0, [(15.0, 0.0, 16.0)], r_corner=6.0), (xb + od / 2 + 37.5, y - 5.0, 120.0), (0, 1, 0), (1, 0, 0))
    out.append(mk("Towing eye plate, 10 mm, 16 mm hole", eye, ST, "made", B(27), "spreader"))
    ws = [bead((xb + od / 2, y + ys * 5.0, 105.0), (0, 0, 1), 30.0, 4.0, (0, ys, 0), (1, 0, 0)) for ys in (-1, 1)]
    out.append(mk("Welds, eye plate to spreader bar", Compound(ws), ST, "weld", B(27), "spreader"))
    br = Compound([rod((x0 + L, y + s_ * (R - 20), 120), (xb - od / 2 - 0.5, y + s_ * (l / 2 - 20), 120), 4) for s_ in (-1, 1)])
    out.append(mk("Stretcher bridle, 10 mm polyester", br, ROPE, "bought", B(27), "bridle"))
    return out


def context_parts(P=PARAMS, Lp=None, xs=None, cut=True, window=None):
    """Rescue pipe (cut open in pictures), platform, structural anchor. Not part of the kit."""
    Do, t = P["pipe"]
    x0 = 0.0 if window is None else window
    pipe = xcyl(0, P["zc"], Do / 2, x0, Lp) - xcyl(0, P["zc"], Do / 2 - t, x0 - 1, Lp + 1)
    if cut:
        pipe = pipe - bx(x0 - 10, Lp + 10, -Do, 0, P["zc"], P["zc"] + Do)
    L = P["trestle"][0]
    anchor = bx(xs - L - 1560, xs - L - 1500, -600, 900, -100, 1500)
    floor = bx(min(xs - L - 1700, x0 - 500), Lp + 800, -1500, 1500, -60, 0)
    return [part("Rescue pipe, 800 x 10 mm, cut open (site)", pipe, "mild_steel", kind="context", group="context"),
            part("Platform (site)", floor, "concrete", kind="context", group="context"),
            part("Structural anchor behind the station (site)", anchor, "concrete", kind="context", group="context")]


# ----------------------------------------------------------------------------- option A
def option_a(P=PARAMS, short=True, bom=True, hangers=True):
    Lp, xs = layout(short)
    out = face_end(P, Lp)
    out += haul_parts(P, Lp, xs, bom)
    out += station_parts(P, xs, bom)
    out += air_parts(P, Lp, xs, bom, hangers)
    out += casualty_parts(P, x0=xs - 200.0, y=-1450.0, bom=bom)
    return out
# ----------------------------------------------------------------------------- option B: rail tramway
def rail_profile(P):
    """T rail in the YZ plane about its centre line: foot 40 x 4, web 4, head 32 x 8, height 40."""
    hw, h, t = P["rail"]
    return [(-20, 0), (20, 0), (20, 4), (2, 4), (2, h - 8), (hw / 2, h - 8), (hw / 2, h), (-hw / 2, h), (-hw / 2, h - 8), (-2, h - 8), (-2, 4), (-20, 4)]


def floor_z(P, y):
    return P["zc"] - math.sqrt((P["pipe"][0] / 2 - P["pipe"][1]) ** 2 - y * y)


def tram_geometry(P):
    """Levels of the tramway: sleeper bottom, rail foot, rail head top and wheel axle."""
    gy = P["gauge"] / 2
    zs = floor_z(P, gy + 40.0) + 0.5
    zf = zs + 10.0
    zt = zf + P["rail"][1]
    az = zt + P["wheel"][0] / 2 + 0.2
    return dict(gy=gy, zs=zs, zf=zf, zt=zt, az=az, z0w=az + 10.0)


FISH_DX = (-105.0, -45.0, 45.0, 105.0)


def tram_parts(P, Lp):
    """Rails in 3 m sections, sleepers, fishplates and rail bolts on the pipe floor (option B)."""
    G = tram_geometry(P)
    gy, zs, zf = G["gy"], G["zs"], G["zf"]
    st = 10.0
    x_a = 300.0
    L = P["rail_len"]
    out = []
    prof = rail_profile(P)
    sleepers = [800.0 + 1000.0 * i for i in range(6)]
    xj = x_a + L
    zw = zf + 18.0                                          # web centre height
    for yr in (-gy, gy):
        sd = "right" if yr > 0 else "left"
        for si in range(2):
            xa = x_a + si * L
            r = prism_yz([(yr + u, zf + v) for u, v in prof], xa, xa + L)
            for xs_ in sleepers:
                if xa + 30 < xs_ < xa + L - 30:
                    for du in (-14.0, 14.0):
                        r = r - zcyl(xs_, yr + du, 3.4, zf - 1, zf + 5)
            for dx in FISH_DX:
                if (dx < 0) == (si == 0):
                    r = r - ycyl(xj + dx, zw, 3.3, yr - 3, yr + 3)
            out.append(mk(f"Rail section {si + 1}, {sd}, aluminium T 40 x 40, 3 m", break_edges(r, 0.6), "aluminium", "made", None, "rails"))
        for k, (ya, yb, sg) in enumerate(((yr - 6.0, yr - 2.0, -1), (yr + 2.0, yr + 6.0, 1))):
            fp = bx(xj - 150, xj + 150, ya, yb, zw - 12, zw + 12)
            for dx in FISH_DX:
                fp = fp - ycyl(xj + dx, zw, 3.3, ya - 1, yb + 1)
            out.append(mk(f"Fishplate {k + 1}, {sd} rail joint, aluminium flat 24 x 4", break_edges(fp, 0.5), "aluminium", "made", None, "rails"))
        for dx in FISH_DX:
            for nm_, sh in cp.hex_bolt_set(6, 12.0):
                out.append(mk(nm_ + f", {sd} rail fishplate", place(sh, (xj + dx, yr + 6.0, zw), (0, 1, 0)), ZP, "fastener", None, "rails"))
    for i, xs_ in enumerate(sleepers):
        sl = Pos(xs_, 0, zs) * cp.sheet(60.0, 2 * (gy + 40.0), st, [(0.0, y_ + du, 6.0) for y_ in (-gy, gy) for du in (-14.0, 14.0)], r_corner=6.0)
        out.append(mk(f"Sleeper {i + 1}, aluminium flat 60 x 10", sl, "aluminium", "made", None, "rails"))
        for yr in (-gy, gy):
            for du in (-14.0, 14.0):
                nm = f"rail {'right' if yr > 0 else 'left'} to sleeper {i + 1}"
                out.append(mk("M6x15 hex bolt (ISO 4017), tapped sleeper, " + nm, place(Pos(0, 0, 1.6) * cp.hex_bolt(6, 15.0), (xs_, yr + du, zf + 4.0), (0, 0, 1)), ZP, "fastener", None, "rails"))
                out.append(mk("M6 washer (ISO 7089), " + nm, place(cp.washer(6), (xs_, yr + du, zf + 4.0), (0, 0, 1)), ZP, "fastener", None, "rails"))
    return out


def wagon_parts(P, x0, tag):
    """Axles, hanger plates, wheels, spacers and axle nuts under one wagon tray (option B)."""
    G = tram_geometry(P)
    gy, az, z0w = G["gy"], G["az"], G["z0w"]
    L = P["sledge_L"]
    out = []
    for ai, xa in enumerate((x0 + 150.0, x0 + L - 150.0)):
        lab = f"wagon {tag} axle {ai + 1}"
        out.append(mk(f"Axle 16 mm, {lab}", place(cp.round_bar(16.0, 306.0, 1.0), (xa, -153.0, az), (0, 1, 0)), "mild_steel", "made", None, "wagons"))
        for ys in (-1, 1):
            pl = place(cp.sheet(50.0, 35.0, 6.0, [(0.0, -7.5, 17.0)], r_corner=5.0), (xa, ys * 40.0 - 3.0, az - 7.5), (0, 1, 0), (1, 0, 0))
            out.append(mk(f"Axle hanger plate, {lab}, {'right' if ys > 0 else 'left'}", pl, ST, "made", None, "wagons"))
            ws = [bead((xa - 25.0, ys * 40.0 + sg * 3.0, z0w), (1, 0, 0), 50.0, 3.0, (0, 0, -1), (0, sg, 0)) for sg in (-1, 1)]
            out.append(mk(f"Welds, hanger plate, {lab}, {'right' if ys > 0 else 'left'}", Compound(ws), ST, "weld", None, "wagons"))
            yin, yw = ys * 99.7, ys * (gy - 12.0)
            sp = place(cp.round_tube(19.0, 1.5, 52.5), (xa, ys * 47.0, az), (0, ys, 0))
            out.append(mk(f"Spacer tube, {lab}, {'right' if ys > 0 else 'left'}", sp, "mild_steel", "made", None, "wagons"))
            r = gy * ys
            w = (ycyl(xa, az, 40.0, min(r - 12, r + 12), max(r - 12, r + 12)) + ycyl(xa, az, 30.0, *sorted((r - ys * 20.3, r - ys * 12.0)))
                 + ycyl(xa, az, 45.0, *sorted((r - ys * 20.3, r - ys * 16.3))))
            w = break_edges(w - ycyl(xa, az, 8.6, -400, 400), 0.8)
            out.append(mk(f"Wheel 80 mm flanged, {lab}, {'right' if ys > 0 else 'left'}", w, UH, "bought", None, "wagons"))
            out.append(mk("M16 washer (ISO 7089)", place(cp.washer(16), (xa, ys * (gy + 12.0), az), (0, ys, 0)), ZP, "fastener", None, "wagons"))
            out.append(mk("M16 hex nut (ISO 4032)", place(cp.hex_nut(16), (xa, ys * (gy + 15.0), az), (0, ys, 0)), ZP, "fastener", None, "wagons"))
    return out


def option_b(P=PARAMS, short=True):
    """Rail tramway: the same ring, ropes, winch station and air line, but wheeled wagons on rails."""
    Lp, xs = layout(short)
    G = tram_geometry(P)
    D = derived(P)
    dz = G["z0w"] - D["sledge_z0"]
    out = face_end(P, Lp)
    out += tram_parts(P, Lp)
    out += haul_parts(P, Lp, xs, False, n=P["wagon_n"], runners=False, dz=dz, wagon=wagon_parts)
    out += station_parts(P, xs, False)
    out += air_parts(P, Lp, xs, False, True)
    out += casualty_parts(P, x0=xs - 200.0, y=-1450.0, bom=False)
    return out
# ----------------------------------------------------------------------------- option C: pneumatic extraction
def hollow_run(pts, ro, ri):
    """Hollow round duct along a polyline with a spherical elbow at each interior vertex (one solid)."""
    out_, in_ = [], []
    for a, b in zip(pts[:-1], pts[1:]):
        out_.append(rod(a, b, ro))
        d = Vector(*b) - Vector(*a)
        ext = Vector(*b) + d.normalized() * 2.0
        in_.append(rod(Vector(*a) - d.normalized() * 2.0, ext, ri))
    for p in pts[1:-1]:
        out_.append(Pos(*p) * Solid.make_sphere(ro))
        in_.append(Pos(*p) * Solid.make_sphere(ri))
    sh = out_[0]
    for o in out_[1:]:
        sh = sh + o
    for i in in_:
        sh = sh - i
    return sh


def clamp_band(p, axis, name, group, up=(0, 0, 1), od=150.0, w=25.0, bom=None):
    """Hose clamp band (4 mm sheet ring, split, with two bolted ears on the 'up' side) round a duct of outside
    diameter od, centred at p."""
    t = 4.0
    ro = od / 2 + t
    o = tuple(p[i] - axis[i] * w / 2 for i in range(3))
    loc = cp.round_tube(2 * ro, t, w)
    loc = loc + bx(ro - 0.5, ro + 14.0, 2.5, 9.5, 0.0, w) + bx(ro - 0.5, ro + 14.0, -9.5, -2.5, 0.0, w)
    loc = loc - bx(ro - 5.0, ro + 15.0, -2.5, 2.5, -1.0, w + 1.0) - ycyl(ro + 7.0, w / 2, 3.3, -10.0, 10.0)
    out = [mk(f"Hose clamp band, {name}", place(break_edges(loc, 0.4), o, axis, up), ZP, "bought", bom, group)]
    for nm_, sh in cp.hex_bolt_set(6, 19.0):
        loc_b = Pos(ro + 7.0, 9.5, w / 2) * Rot(-90, 0, 0) * sh
        out.append(mk(nm_ + f", {name} clamp", place(loc_b, o, axis, up), ZP, "fastener", bom, group))
    return out


def flange_ring(xc, yc, z, ri, ro, t, nb, rb, d=8, hole=4.2):
    f = zcyl(xc, yc, ro, z, z + t) - zcyl(xc, yc, ri, z - 1, z + t + 1)
    for k in range(nb):
        a = 2 * math.pi * k / nb
        f = f - zcyl(xc + rb * math.cos(a), yc + rb * math.sin(a), hole, z - 1, z + t + 1)
    return f


def suction_parts(P, Lp):
    """Nozzle, hose in three lengths with couplings and saddles, riser (option C)."""
    D = derived(P)
    f0 = D["floor_z"](0.0)
    zh = f0 + 110.0
    R, r = P["hose_d"] / 2, P["hose_d"] / 2 - P["hose_wall"]
    xn, xe = Lp - 500.0, -1300.0
    out = []
    cone = Solid.make_cone(R, 110.0, 200.0)
    cone = cone - Solid.make_cone(R - 4.0, 110.0 - 4.0, 200.0)
    out.append(mk("Suction nozzle, 4 mm rubber lined mouth", break_edges(place(cone, (xn, 0, zh), (1, 0, 0)), 0.6), "epdm", "bought", None, "hose"))
    xj = [xn - (xn - xe) * k / 3 for k in (1, 2)]
    ends = [xn] + xj + [xe]
    for k in range(3):
        xa, xb = ends[k + 1], ends[k]
        if k == 0:
            xa_, xb_ = xa + 1.0, xb - 1.0
        else:
            xa_, xb_ = xa + 1.0, xb - 1.0
        if k < 2:
            h = xcyl(0, zh, R, xa_, xb_) - xcyl(0, zh, r, xa_ - 1, xb_ + 1)
            out.append(mk(f"Suction hose {k + 1}, 150 mm EPDM, 2.5 m", break_edges(h, 0.5), "epdm", "bought", None, "hose"))
        else:
            zin = 1290.0
            h = hollow_run([(xb_, 0, zh), (xe, 0, zh), (xe, 0, zin)], R, r)
            out.append(mk("Suction hose 3 with riser, 150 mm EPDM", h, "epdm", "bought", None, "hose"))
    for k, x in enumerate(xj):
        sp = place(cp.round_tube(2 * (r - 0.2), 3.8, 200.0), (x - 100.0, 0, zh), (1, 0, 0))
        out.append(mk(f"Coupling spigot {k + 1}, aluminium tube", sp, "aluminium", "made", None, "hose"))
        for sg in (-1, 1):
            out += clamp_band((x + sg * 70.0, 0, zh), (1, 0, 0), f"coupling {k + 1} {'face' if sg > 0 else 'portal'} side", "hose", up=(0, 0, 1))
    for k, x in enumerate((900.0, 2200.0, 3500.0, 4800.0, 6000.0)):
        blk = bx(x - 60, x + 60, -100, 100, f0 + 0.3, zh) - xcyl(0, zh, R + 0.3, x - 61, x + 61)
        out.append(mk(f"Hose saddle {k + 1}, HDPE block", break_edges(blk, 1.5), UH, "made", None, "hose"))
    return out


def cyclone_parts(P):
    """Cyclone on four legs, inlet box, lid, vortex finder, dust drum, exhaust duct, filter and fan stack."""
    out = []
    xe = -1300.0
    xc, yc = -1900.0, 225.0
    Ro, Ri = 300.0, 297.0
    zc0, zc1, zb1 = 650.0, 1150.0, 1450.0
    body = zcyl(xc, yc, Ro, zc1, zb1) - zcyl(xc, yc, Ri, zc1 - 1, zb1 + 1)
    out.append(mk("Cyclone body, 3 mm rolled sheet", break_edges(body, 0.8), ST, "made", None, "cyclone"))
    cone = Pos(xc, yc, zc0) * (Solid.make_cone(90.0, Ro, zc1 - zc0) - Solid.make_cone(87.0, Ri, zc1 - zc0))
    out.append(mk("Cyclone cone, 3 mm rolled sheet", break_edges(cone, 0.8), ST, "made", None, "cyclone"))
    sup = zcyl(xc, yc, 380.0, zc1, zc1 + 6.0) - zcyl(xc, yc, Ro, zc1 - 1, zc1 + 7.0)
    out.append(mk("Cyclone support ring, 6 mm plate", break_edges(sup, 0.8), ST, "made", None, "cyclone"))
    out.append(mk("Cyclone outlet tube, 180 mm", place(cp.round_tube(180.0, 3.0, 60.0), (xc, yc, 590.0), (0, 0, 1)), ST, "made", None, "cyclone"))
    fl = flange_ring(xc, yc, zb1, Ro, 330.0, 6.0, 12, 315.0)
    out.append(mk("Cyclone top flange ring, 6 mm", break_edges(fl, 0.6), ST, "made", None, "cyclone"))
    lid = flange_ring(xc, yc, zb1 + 6.0, 75.5, 330.0, 6.0, 12, 315.0)
    out.append(mk("Cyclone lid, 6 mm plate, finder hole", break_edges(lid, 0.6), ST, "made", None, "cyclone"))
    for k in range(12):
        a = 2 * math.pi * k / 12
        for nm_, sh in cp.hex_bolt_set(8, 12.0):
            out.append(mk(nm_ + ", cyclone lid", place(sh, (xc + 315 * math.cos(a), yc + 315 * math.sin(a), zb1 + 12.0), (0, 0, 1)), ZP, "fastener", None, "cyclone"))
    out.append(mk("Vortex finder tube, 150 mm", place(cp.round_tube(150.0, 3.0, 450.0), (xc, yc, 1250.0), (0, 0, 1)), ST, "made", None, "cyclone"))
    # inlet box, tangential, with a hole for the riser
    bx0, bx1 = xc + 150.0, xe + 75.0
    ib = bx(bx0, bx1, -75.0, 75.0, 1290.0, 1425.0) - bx(bx0 - 1, bx1 - 3.0, -72.0, 72.0, 1293.0, 1422.0) - zcyl(xe, 0, 71.0, 1289.0, 1294.0)
    out.append(mk("Cyclone inlet box, 3 mm sheet", break_edges(ib, 0.8), ST, "made", None, "cyclone"))
    out.append(mk("Riser collar, aluminium tube", place(cp.round_tube(158.0, 4.0, 40.0), (xe, 0, 1250.0), (0, 0, 1)), "aluminium", "made", None, "cyclone"))
    # legs with feet and anchors
    for k, (sx, sy) in enumerate(((1, 1), (1, -1), (-1, 1), (-1, -1))):
        lx, ly = xc + sx * 240.4, yc + sy * 240.4
        leg = place(cp.shs(40.0, 3.0, 1136.0), (lx, ly, 8.0), (0, 0, 1))
        out.append(mk(f"Cyclone leg {k + 1}, 40 x 40 x 3 SHS", leg, ST, "made", None, "cyclone"))
        foot = Pos(lx, ly, 0) * cp.sheet(100.0, 100.0, 8.0, [(-35.0, 0.0, 12.0), (35.0, 0.0, 12.0)], r_corner=6.0)
        out.append(mk(f"Cyclone foot plate {k + 1}, 8 mm", foot, ST, "made", None, "cyclone"))
        ws = [bead((lx - 20.0, ly + sy2 * 20.0, 8.0), (1, 0, 0), 40.0, 4.0, (0, sy2, 0), (0, 0, 1)) for sy2 in (-1, 1)]
        out.append(mk(f"Welds, cyclone leg {k + 1} to foot", Compound(ws), ST, "weld", None, "cyclone"))
        for dx in (-35.0, 35.0):
            out.append(mk("M12 anchor bolt, washer and nut", place(cp.anchor_bolt(12, 80.0), (lx + dx, ly, 8.0), (0, 0, 1)), ZP, "fastener", None, "cyclone"))
    # dust drum and lid
    drum = zcyl(xc, yc, 260.0, 0, 600.0) - zcyl(xc, yc, 258.8, 1.2, 601.0)
    out.append(mk("Dust drum 120 L, steel", break_edges(drum, 1.0), ST, "bought", None, "drum"))
    dl = zcyl(xc, yc, 262.0, 600.0, 603.0) - zcyl(xc, yc, 91.0, 599.0, 604.0)
    out.append(mk("Dust drum lid, steel", break_edges(dl, 0.6), ST, "bought", None, "drum"))
    # exhaust duct, filter housing and fan
    xf = -2800.0
    top = 808.0
    ex = hollow_run([(xc, yc, 1702.0), (xc, yc, 1900.0), (xf, yc, 1900.0), (xf, yc, top + 12.0)], 75.0, 71.0)
    out.append(mk("Exhaust duct, 150 mm EPDM", ex, "epdm", "bought", None, "exhaust"))
    out += clamp_band((xc, yc, 1700.0), (0, 0, 1), "vortex finder to exhaust duct", "exhaust", up=(1, 0, 0))
    return out
    # filter housing on the fan, both on a base plate
    fy = yc
    bp = Pos(xf, fy, 0) * cp.sheet(560.0, 560.0, 8.0, [(dx, dy, 11.0) for dx in (-230.0, 230.0) for dy in (-230.0, 230.0)], r_corner=8.0)
    out.append(mk("Fan base plate, 8 mm", bp, ST, "made", None, "filter"))
    fan = (zcyl(xf, fy, 240.0, 8.0, 248.0) - zcyl(xf, fy, 236.0, 12.0, 244.0))
    fan = fan + (xcyl(fy, 128.0, 100.0, xf, xf + 480.0) - xcyl(fy, 128.0, 96.0, xf - 1, xf + 481.0))
    out.append(mk("High-pressure blower 7.5 kW, casing and outlet spigot", break_edges(fan, 1.0), "safety_yellow", "bought", None, "filter"))
    for dx in (-230.0, 230.0):
        for dy in (-230.0, 230.0):
            out.append(mk("M10 hex bolt (ISO 4017), fan to base plate", place(Pos(0, 0, 2.0) * cp.hex_bolt(10, 12.0), (xf + dx, fy + dy, 8.0), (0, 0, 1)), ZP, "fastener", None, "filter"))
    hz0, hz1 = 258.0, top
    hs = bx(xf - 250, xf + 250, fy - 250, fy + 250, hz0, hz1) - bx(xf - 248, xf + 248, fy - 248, fy + 248, hz0 - 1, hz1 + 1)
    hs = hs + (bx(xf - 250, xf + 250, fy - 250, fy + 250, hz1 - 2.0, hz1) - bx(xf - 230, xf + 230, fy - 230, fy + 230, hz1 - 3.0, hz1 + 1.0))
    for dx in (-238.0, 238.0):
        for dy in (-238.0, 238.0):
            hs = hs - zcyl(xf + dx, fy + dy, 4.2, hz1 - 3.0, hz1 + 1.0)
    out.append(mk("Filter housing, 2 mm sheet, top flange", break_edges(hs, 0.6), ST, "made", None, "filter"))
    tp = Pos(xf, fy, hz1) * cp.sheet(500.0, 500.0, 4.0, [(dx, dy, 8.4) for dx in (-238.0, 238.0) for dy in (-238.0, 238.0)] + [(0.0, 0.0, 142.0)], r_corner=6.0)
    out.append(mk("Filter housing top plate, 4 mm", tp, ST, "made", None, "filter"))
    for dx in (-238.0, 238.0):
        for dy in (-238.0, 238.0):
            for nm_, sh in cp.hex_bolt_set(8, 6.0):
                out.append(mk(nm_ + ", filter top plate", place(sh, (xf + dx, fy + dy, hz1 + 4.0), (0, 0, 1)), ZP, "fastener", None, "filter"))
    out.append(mk("Exhaust collar, aluminium tube", place(cp.round_tube(158.0, 4.0, 40.0), (xf, fy, hz1 + 4.0), (0, 0, 1)), "aluminium", "made", None, "filter"))
    seat = bx(xf - 248, xf + 248, fy - 248, fy + 248, 740.0, 743.0) - zcyl(xf, fy, 150.0, 739.0, 744.0)
    out.append(mk("Filter seat plate, 3 mm", break_edges(seat, 0.4), ST, "made", None, "filter"))
    ws = [bead((xf + sx * 248.0, fy - 248.0, 743.0), (0, 1, 0), 496.0, 3.0, (0, 0, 1), (-sx, 0, 0)) for sx in (-1, 1)]
    ws += [bead((xf - 248.0, fy + sy * 248.0, 743.0), (1, 0, 0), 496.0, 3.0, (0, 0, 1), (0, -sy, 0)) for sy in (-1, 1)]
    out.append(mk("Welds, filter seat plate", Compound(ws), ST, "weld", None, "filter"))
    cart = zcyl(xf, fy, 200.0, 743.0, 1143.0) - zcyl(xf, fy, 120.0, 742.0, 1144.0)
    out.append(mk("Filter cartridge, pleated, 400 mm", break_edges(cart, 1.5), "coir", "bought", None, "filter"))
    return out


def option_c(P=PARAMS, short=True):
    """Pneumatic extraction: the same ring (no sheave), air line and casualty line, with a suction hose, cyclone and fan."""
    Lp, xs = layout(short)
    out = face_end(P, Lp, sheave=False)
    out += suction_parts(P, Lp)
    out += cyclone_parts(P)
    out += air_parts(P, Lp, xs, False, True)
    out += casualty_parts(P, x0=xs - 200.0, y=-1450.0, bom=False)
    return out


# ----------------------------------------------------------------------------- option assembly and masses
def grouped(parts, keys=None):
    """Legacy view: {group: Compound} of the non-context parts, for the drawing sheets and picture scripts."""
    g = {}
    for p in parts:
        if p["kind"] == "context" or (keys and p["group"] not in keys):
            continue
        g.setdefault(p["group"], []).append(p["shape"])
    return {k: Compound(v) for k, v in g.items()}


def components(option=CHOSEN):
    """Every part of one option in the shortened layout (pipe 6.8 m, station 2.4 m outside the portal), as
    cad_parts.part() dicts, with the pipe, platform and anchor as context."""
    Lp, xs = layout(True)
    parts = {"A": option_a, "B": option_b, "C": option_c}[option]()
    return parts + context_parts(P, Lp, xs)


def _mass(parts):
    return sum(cp.mass_kg(p) for p in parts)


def masses(P=PARAMS):
    """Masses in kg of the made parts and the carried items, from the model (one of each)."""
    Lp, xs = layout(True)
    ring = face_end(P, Lp)
    m = {}
    for k in ("crown", "side_p", "side_m", "bottom", "cover", "spigot", "sheave_hw", "jacks", "joint_bolts"):
        m[k] = _mass([p for p in ring if p["group"] == k])
    m["sheave"] = _mass([p for p in ring if p["group"] == "sheave"]) * 0.6      # cast sheave with a hollow hub
    m["sledge"] = _mass(sledge_parts(P, 0.0, "1", False))
    m["trestle"] = _mass(trestle_parts(P, 0.0, 0.0, "A", False))
    m["ties"] = _mass(tie_parts(P, 0.0, 0.0, 0.0, "1", False))
    m["guard"] = _mass(guard_parts(P, 0.0, 0.0, 0.0, "A", False))
    m["spreader"] = _mass([p for p in casualty_parts(P, 0.0, 0.0, False) if p["group"] == "spreader"])
    m["ring_total"] = sum(m[k] for k in ("crown", "side_p", "side_m", "bottom", "cover", "spigot", "sheave_hw",
                                         "jacks", "joint_bolts", "sheave"))
    return m


if __name__ == "__main__":
    import copy
    from build123d import export_stl
    for opt in OPTIONS:
        ps = components(opt)
        real = [q for q in ps if q["kind"] != "context"]
        print(f"option {opt}: {len(real)} parts, {sum(cp.mass_kg(q) for q in real):.1f} kg")
    out = HERE.parents[1] / "cad/stl"
    out.mkdir(parents=True, exist_ok=True)
    a = [q for q in components(CHOSEN) if q["kind"] != "context"]
    export_stl(Compound([copy.copy(q["shape"]) for q in a]), str(out / "sleevedrift-assembly.stl"), tolerance=0.15, angular_tolerance=0.3)
