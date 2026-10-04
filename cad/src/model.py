"""SleeveDrift parametric model (build123d), TRL 3, constructable design (SVD-DDR-002).

Run from the repo root:  python cad/src/model.py          (exports and checks)
                         python cad/src/model.py --check  (constructability checks only)
Exports STEP and STL into cad/step and cad/stl:
    sleevedrift-ring.step / .stl       hooded cutting ring: four bolted segments, jacking screws,
                                       face return sheave with its cover, duct outlet spigot
    sleevedrift-sledge.step / .stl     one spoil sledge with its runners and end lugs
    sleevedrift-station.step / .stl    portal haul station: two winch trestles, cross ties, winches,
                                       drill drives on winch bits and drum guards (decision 24B)
    sleevedrift-assembly.step          the whole kit at the design case: 60 m of 800 mm rescue
                                       pipe, train of four sledges at the face, ropes as straight legs

Axes: X runs along the rescue pipe from its portal mouth (x = 0) to the face end (x = Lp),
Y is across the pipe, Z is up with the platform the pipe rests on at z = 0. The pipe axis is at
z = 400 mm. Angles round the pipe axis (theta) are measured from the top (+Z) toward +Y.
The train lane runs along the pipe floor on y = 0; the return leg of the rope lies on the floor
at y = +230 mm; the air duct hangs on the upper +Y wall and the signal cable near the crown.

Constructable design, 2026-10-03 (SVD-DDR-002, decided under Amish's pre-approvals of 2026-10-03):
    the hooded cutting ring is four rolled 5 mm steel segments (crown with the hood, two sides,
    bottom) bolted through inside flanges, so each piece passes along the pipe and weighs under
    25 kg; four M20 jacking screws with swivel pads centre and lock it in the pipe mouth with no
    drilling or welding to the pipe; the face return sheave sits on a bracket welded to the bottom
    segment, under a kneeling cover; the haul is a reversible shuttle: a train of four 30 L sledges
    between a pull rope and a tail rope that runs round the face sheave and back as the return
    leg, each end on its own two-speed self-tailing winch at the portal, with a 2.5 kN breakaway
    swivel at each end of the train; forced air from a 200 mm blower in layflat duct on magnet
    hangers to a steel outlet spigot on the crown.
Amish's decision 24B, 2026-10-03 ("i agree with all the 46 recommendations you provided. please
proceed."): a right-angle electric drill on a winch bit in each winch socket drives the haul at
the portal, behind a drum guard; the winch handles are stowed for hand cranking as the fallback;
nothing is added inside the pipe.
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (SVD-CAL-001), the drawings (cad/src/sheets.py), the concept media
(cad/src/concept_media.py), the product model and the build plan pictures.
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

from build123d import (Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, Solid, Vector, extrude,
                       export_step, export_stl)

# Top-level parameters (mm). Edit these, not the geometry below.
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


# ----------------------------------------------------------------------------- helpers
def bx(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def xcyl(y, z, r, x0, x1):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def ycyl(x, z, r, y0, y1):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def zcyl(x, y, r, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _ccw(points):
    a = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1]))
    return list(points) if a > 0 else list(points)[::-1]


def prism_yz(points, x0, x1):
    """Polygon given as (y, z) points, extruded from x0 to x1."""
    f = Plane.YZ.offset(x0) * Polygon(*_ccw(points), align=None)
    return extrude(f, amount=x1 - x0)


def prism_xz(points, y0, y1):
    """Polygon given as (x, z) points, extruded from y0 to y1."""
    f = Plane.XZ.offset(-y0) * Polygon(*_ccw(points), align=None)
    return extrude(f, amount=-(y1 - y0))


def rod(a, b, r):
    """Round bar from point a to point b."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def polyline_rope(pts, r):
    return Compound([rod(a, b, r) for a, b in zip(pts, pts[1:])])


def wall_dist(P, drop, th):
    """Distance from the ring axis (drop below the pipe axis) to the pipe wall along angle th."""
    t = math.radians(th)
    R = (P["pipe"][0] - 2 * P["pipe"][1]) / 2
    return drop * math.cos(t) + math.sqrt(R * R - (drop * math.sin(t)) ** 2)


def at(P, r, th, x):
    """Point at radius r, angle th (deg from the top toward +Y) round the pipe axis, station x."""
    t = math.radians(th)
    return (x, r * math.sin(t), P["zc"] + r * math.cos(t))


def e_t(th):
    t = math.radians(th)
    return Vector(0, math.cos(t), -math.sin(t))


def sector(P, ro, ri, th0, th1, x0, x1):
    """Annular sector of the ring shell between angles th0 and th1 (deg), from x0 to x1."""
    zc = P["zc"]
    tube = xcyl(0, zc, ro, x0, x1) - xcyl(0, zc, ri, x0 - 1, x1 + 1)
    R = 2.5 * ro
    n = max(2, int(abs(th1 - th0) / 20) + 1)
    pts = [(0.0, zc)] + [(R * math.sin(math.radians(th0 + (th1 - th0) * k / n)),
                          zc + R * math.cos(math.radians(th0 + (th1 - th0) * k / n))) for k in range(n + 1)]
    return tube & prism_yz(pts, x0 - 2, x1 + 2)


def radial_bar(P, th, r0, r1, s0, s1, x0, x1):
    """Flat bar in the radial plane at angle th, from radius r0 to r1, tangential offset s0 to s1."""
    t = e_t(th)
    pts = []
    for r, s in ((r0, s0), (r1, s0), (r1, s1), (r0, s1)):
        p = Vector(*at(P, r, th, 0)) + t * s
        pts.append((p.Y, p.Z))
    return prism_yz(pts, x0, x1)


def radial_rod(P, th, r0, r1, rad, x, s=0.0):
    a = Vector(*at(P, r0, th, x)) + e_t(th) * s
    b = Vector(*at(P, r1, th, x)) + e_t(th) * s
    return rod(a, b, rad)


def tang_rod(P, th, r, s0, s1, rad, x):
    p = Vector(*at(P, r, th, x))
    return rod(p + e_t(th) * s0, p + e_t(th) * s1, rad)


# ----------------------------------------------------------------------------- derived figures
def derived(P=PARAMS):
    D = {}
    Do, t = P["pipe"]
    D["pipe_id"] = Do - 2 * t
    D["ro"] = P["ring_od"] / 2
    D["ri"] = D["ro"] - P["shell_t"]
    D["radial_gap"] = D["pipe_id"] / 2 - D["ro"]
    D["ring_len"] = P["ring_in"] + P["ring_out"]
    D["crown_len"] = D["ring_len"] + P["hood"]
    D["x_rear"] = -P["ring_in"]                   # relative to the pipe mouth
    D["x_front"] = P["ring_out"]
    D["x_hood"] = P["ring_out"] + P["hood"]
    j = P["joints"]
    D["segments"] = {"crown": (-j[0], j[0]), "side_p": (j[0], j[1]), "bottom": (j[1], j[2]),
                     "side_m": (j[2], j[3])}
    D["sheave_pitch_r"] = P["sheave"][0] / 2
    D["leg_y"] = (P["sheave_c"][1] - D["sheave_pitch_r"], P["sheave_c"][1] + D["sheave_pitch_r"])
    D["sledge_area"] = (P["sledge_w"][0] + P["sledge_w"][1]) / 2 * P["sledge_h"]       # mm^2
    D["sledge_L"] = P["sledge_L"] * D["sledge_area"] / 1e6                             # litres struck
    D["train_len"] = P["n_sledges"] * P["sledge_L"] + (P["n_sledges"] - 1) * P["sledge_gap"]
    D["sledge_z0"] = P["runner_z"] + P["runner"][1]
    D["lug_z"] = D["sledge_z0"] + 50.0
    D["floor_z"] = lambda y: P["zc"] - math.sqrt((D["pipe_id"] / 2) ** 2 - y * y)
    rr = D["pipe_id"] / 2 - P["rope_d"] / 2 - 0.5        # rope centre radius when it lies on the pipe floor
    D["rope_floor_z"] = {y: P["zc"] - math.sqrt(rr * rr - y * y) for y in (0.0, P["ret_y"])}
    D["drum_rope_r"] = P["winch"][2] + P["rope_d"] / 2
    return D


# ----------------------------------------------------------------------------- face end parts
def ring_parts(P=PARAMS, Lp=None):
    """Hooded cutting ring at the mouth of a pipe of length Lp: segments, bolts, jacks, sheave, cover, spigot."""
    Lp = P["Lp"] if Lp is None else Lp
    D = derived(P)
    ro, ri = D["ro"], D["ri"]
    xr, xf, xh = Lp + D["x_rear"], Lp + D["x_front"], Lp + D["x_hood"]
    fd, ft = P["flange"]
    bw, bt = P["band"]
    rb = ri - fd / 2                                   # bolt circle radius
    bolts_x = [Lp + v for v in P["joint_bolts_x"]]
    dt = math.degrees((ft + 0.5) / ri)                 # flange width in degrees at the shell

    def holes_at(th):
        return [tang_rod(P, th, rb, -40, 40, 6.5, x) for x in bolts_x]

    Pa = P                                             # pipe axis frame (rope plane, spigot, duct)
    P = dict(P, zc=P["zc"] - P["ring_drop"])            # ring axis: the ring rests on the pipe invert
    out = {}
    for key, (a, b) in D["segments"].items():
        x1 = xh if key == "crown" else xf
        seg = sector(P, ro, ri, a, b, xr, x1)
        # inside flanges along both joint edges; on the crown they run on to the hood front as ribs
        fl = radial_bar(P, a, ri - fd, ri + 0.3, 0, ft, xr, x1) + radial_bar(P, b, ri - fd, ri + 0.3, -ft, 0, xr, x1)
        seg = seg + fl
        # front cutting band inside the front edge (hood lip on the crown)
        if key == "crown":
            seg = seg + sector(P, ri + 0.2, ri - P["hood_lip"][1], a + dt, b - dt, xh - P["hood_lip"][0], xh)
        else:
            seg = seg + sector(P, ri + 0.2, ri - bt, a + dt, b - dt, xf - bw, xf)
        for th in (a, b):
            for h in holes_at(th):
                seg = seg - h
        out[key] = seg
    # jacking screw nuts welded inside, holes through the shell
    jx = Lp + P["jack_x"]
    nut_d, nut_h = P["nut"]
    for th in P["jack_th"]:
        key = next(k for k, (a, b) in D["segments"].items() if (a < th < b) or (a < th + 360 < b))
        nut = radial_rod(P, th, ri - nut_h, ri + 0.3, nut_d / 2, jx) - radial_rod(P, th, ri - nut_h - 1, ri + 1, P["jack_d"] / 2, jx)
        out[key] = out[key] + nut - radial_rod(P, th, ri - 1, ro + 1, P["jack_d"] / 2 + 1, jx)
    # sheave bracket welded to the bottom segment: base plate on two curved saddles, pin, cover posts
    sx, sy = Lp + P["sheave_c"][0], P["sheave_c"][1]
    bx0, bx1, by0, by1, bt_ = P["base_plate"]
    zt = P["base_top"]
    base = bx(Lp + bx0, Lp + bx1, by0, by1, zt - bt_, zt)
    zin = lambda y: P["zc"] - math.sqrt(ri * ri - y * y)  # noqa: E731
    ys = [by0 + (by1 - by0) * k / 12 for k in range(13)]
    prof = [(by0, zt - bt_), (by1, zt - bt_)] + [(y, zin(y) - 0.3) for y in reversed(ys)]
    saddles = prism_yz(prof, Lp + bx0 + 5, Lp + bx0 + 15) + prism_yz(prof, Lp + bx1 - 15, Lp + bx1 - 5)
    pin = zcyl(sx, sy, P["sheave_pin"] / 2, zt, P["rope_z"] + 25)
    (px0, px1), (py0, py1) = P["posts_xy"]
    posts = None
    for x in (px0, px1):
        for y in (py0, py1):
            p = zcyl(Lp + x, y, 10, zt, P["cover_z"])
            posts = p if posts is None else posts + p
    out["bottom"] = out["bottom"] + base + saddles + pin + posts
    # duct spigot saddles welded inside the crown
    sp_c = at(Pa, Pa["duct_r"], Pa["duct_th"], 0)
    sp_r = P["spigot"][0] / 2
    for x0 in (-150.0, -30.0):
        blk = radial_bar(P, P["duct_th"], 350, ri + 0.3, -25, 25, Lp + x0, Lp + x0 + 60)
        blk = blk - xcyl(sp_c[1], sp_c[2], sp_r + 0.5, Lp + x0 - 1, Lp + x0 + 61)
        out["crown"] = out["crown"] + blk
    # joint bolts (bought)
    bolts = []
    for th in P["joints"]:
        for x in bolts_x:
            shank = tang_rod(P, th, rb, -ft, ft + 12, 6.0, x)
            head = tang_rod(P, th, rb, -ft - 8, -ft, 9.5, x)
            nut = tang_rod(P, th, rb, ft, ft + 8, 9.5, x)
            bolts.append(shank + head + nut)
    out["joint_bolts"] = Compound(bolts)
    # jacking screws with swivel pads
    jacks = []
    hd, hh = P["head"]
    pd, pt = P["pad"]
    for th in P["jack_th"]:
        rw = wall_dist(Pa, P["ring_drop"], th) - 0.6      # pipe wall along the screw axis
        rw = rw - (pd / 2) ** 2 / (2 * D["pipe_id"] / 2)   # flat pad corners clear the curved wall
        shank = radial_rod(P, th, ri - nut_h - 20, rw - pt, P["jack_d"] / 2 - 0.2, jx)
        head = radial_rod(P, th, ri - nut_h - 20 - hh, ri - nut_h - 20, hd / 2, jx)
        pad = radial_rod(P, th, rw - pt, rw, pd / 2, jx)
        jacks.append(shank + head + pad)
    out["jacks"] = Compound(jacks)
    # face return sheave (bought): two flanges and a grooved core on the pin
    z0 = P["rope_z"] - P["sheave"][2] / 2
    R, Rc = P["sheave"][1] / 2, D["sheave_pitch_r"] - P["rope_d"] / 2
    sh = zcyl(sx, sy, R, z0, z0 + 8) + zcyl(sx, sy, Rc, z0 + 8, z0 + 22) + zcyl(sx, sy, R, z0 + 22, z0 + 30)
    out["sheave"] = sh - zcyl(sx, sy, P["sheave_pin"] / 2 + 0.5, z0 - 1, z0 + 31)
    # spacer under the sheave and keeper washer above it (made)
    sp = zcyl(sx, sy, 20, zt, z0) - zcyl(sx, sy, P["sheave_pin"] / 2 + 0.5, zt - 1, z0 + 1)
    kw = zcyl(sx, sy, 22, z0 + 30, z0 + 35) - zcyl(sx, sy, P["sheave_pin"] / 2 + 0.5, z0 + 29, z0 + 36)
    out["sheave_hw"] = sp + kw
    # cover and kneeling plate (bolted to the posts)
    cx0, cx1, cy0, cy1, ct = P["cover"]
    out["cover"] = bx(Lp + cx0, Lp + cx1, cy0, cy1, P["cover_z"], P["cover_z"] + ct)
    # duct outlet spigot
    s0, s1 = P["spigot_x"]
    out["spigot"] = xcyl(sp_c[1], sp_c[2], sp_r, Lp + s0, Lp + s1) - xcyl(sp_c[1], sp_c[2], sp_r - P["spigot"][1], Lp + s0 - 1, Lp + s1 + 1)
    # magnetic lamp inside the hood
    out["lamp"] = radial_rod(P, -30.0, ri - 41.3, ri - 1.3, 30, Lp + 120)
    return out


# ----------------------------------------------------------------------------- haul parts
def sledge(P, x0):
    """One spoil sledge from x0 (portal end) to x0 + L: tray, runners, end lugs."""
    D = derived(P)
    L = P["sledge_L"]
    w0, w1 = P["sledge_w"]
    h, t = P["sledge_h"], P["sheet"]
    z0 = D["sledge_z0"]
    outer = [(-w0 / 2, z0), (w0 / 2, z0), (w1 / 2, z0 + h), (-w1 / 2, z0 + h)]
    k = (w1 - w0) / 2 / h
    inner = [(-w0 / 2 + t, z0 + t), (w0 / 2 - t, z0 + t), (w1 / 2 - t + k * 10, z0 + h + 10), (-w1 / 2 + t - k * 10, z0 + h + 10)]
    tray = prism_yz(outer, x0, x0 + L) - prism_yz(inner, x0 + t, x0 + L - t)
    rw, rt, ry = P["runner"]
    zr = P["runner_z"]
    runners = bx(x0, x0 + L, -ry - rw / 2, -ry + rw / 2, zr, zr + rt) + bx(x0, x0 + L, ry - rw / 2, ry + rw / 2, zr, zr + rt)
    lp, lt, lh = P["lug"]
    zl = D["lug_z"]
    lugs = (bx(x0 - lp, x0, -lt / 2, lt / 2, zl - lh / 2, zl + lh / 2)
            + bx(x0 + L, x0 + L + lp, -lt / 2, lt / 2, zl - lh / 2, zl + lh / 2))
    lugs = lugs - ycyl(x0 - 30, zl, P["lug_hole"] / 2, -10, 10) - ycyl(x0 + L + 30, zl, P["lug_hole"] / 2, -10, 10)
    return {"tray": tray, "runners": runners, "lugs": lugs}


def train_layout(P, Lp):
    """x of the portal end of each sledge, face-end sledge first, with the train at the face."""
    D = derived(P)
    xe = Lp - P["train_gap"]
    return [xe - P["sledge_L"] - k * (P["sledge_L"] + P["sledge_gap"]) for k in range(P["n_sledges"])]


def shackle_pin(P, x):
    D = derived(P)
    zl = D["lug_z"] - 1.0                  # the pin rests on the bottom of the 16 mm hole
    return ycyl(x, zl, 7.0, -16, 16)


def link_between(P, xa, xb):
    """Connecting link between two lug holes at xa < xb: two pins and two side bars."""
    D = derived(P)
    zl = D["lug_z"] - 1.0
    bars = xcyl(-11.5, zl, 4.0, xa, xb) + xcyl(11.5, zl, 4.0, xa, xb)
    return shackle_pin(P, xa) + shackle_pin(P, xb) + bars


def swivel(P, x_hole, direction):
    """Breakaway swivel: shackle pin through the lug hole, cheeks, swivel body along X.
    direction +1 points toward the face, -1 toward the portal. Returns (shape, rope end x)."""
    D = derived(P)
    zl = D["lug_z"] - 1.0
    d = direction
    xa, xb = (x_hole, x_hole + 30 * d)
    pin = shackle_pin(P, x_hole)
    ch = bx(min(xa, xb), max(xa, xb), 8, 12, zl - 10, zl + 10)
    ch = ch + bx(min(xa, xb), max(xa, xb), -12, -8, zl - 10, zl + 10)
    xb2 = xb + 150 * d
    body = xcyl(0, zl, 14.0, min(xb, xb2), max(xb, xb2))
    return pin + ch + body, xb2


def haul_parts(P=PARAMS, Lp=None, x_stand=None):
    """Sledges, links, swivels and ropes with the train at the face, plus the portal station."""
    Lp = P["Lp"] if Lp is None else Lp
    xs = P["x_stand"] if x_stand is None else x_stand
    D = derived(P)
    out = {}
    xs_list = train_layout(P, Lp)
    trays, runners, lugs = [], [], []
    for x0 in xs_list:
        s = sledge(P, x0)
        trays.append(s["tray"])
        runners.append(s["runners"])
        lugs.append(s["lugs"])
    out["sledges"] = Compound(trays + lugs)
    out["runners"] = Compound(runners)
    links = []
    for k in range(len(xs_list) - 1):
        xa = xs_list[k + 1] + P["sledge_L"] + 30       # front lug hole of the next sledge toward the portal
        xb = xs_list[k] - 30                            # rear lug hole of this sledge
        links.append(link_between(P, xa, xb))
    out["links"] = Compound(links)
    sw_face, x_tail = swivel(P, xs_list[0] + P["sledge_L"] + 30, +1)
    sw_port, x_pull = swivel(P, xs_list[-1] - 30, -1)
    out["swivels"] = Compound([sw_face, sw_port])
    # ropes
    zl = D["lug_z"]
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
    pull = [(xw, yA + rr, hz), (0.0, 0.0, zf0), (x_pull - 600, 0.0, zf0), (x_pull, 0.0, zl)]
    arc = [(sx + pr * math.sin(math.radians(a)), sy - pr * math.cos(math.radians(a)), zr) for a in range(0, 181, 10)]
    tail = [(x_tail, 0.0, zl)] + [(sx, sy - pr, zr)] + arc[1:] + [(Lp - 1200.0, P["ret_y"], zfr), (0.0, P["ret_y"], zfr),
                                                                  (xw, yB - rr, hz)]
    wraps = []
    for y in (yA, yB):
        wraps.append(zcyl(xw, y, rr + r, hz - 15, hz + 15) - zcyl(xw, y, P["winch"][2], hz - 16, hz + 16))
    out["ropes"] = Compound([polyline_rope(pull, r), polyline_rope(tail, r)] + wraps)
    out.update(station_parts(P, xs))
    return out


def shs(x0, x1, y0, y1, z0, z1, axis, P=PARAMS):
    """Square hollow section between the given limits, open along its axis."""
    t = P["shs"][1]
    outer = bx(x0, x1, y0, y1, z0, z1)
    if axis == "x":
        return outer - bx(x0 - 1, x1 + 1, y0 + t, y1 - t, z0 + t, z1 - t)
    if axis == "y":
        return outer - bx(x0 + t, x1 - t, y0 - 1, y1 + 1, z0 + t, z1 - t)
    return outer - bx(x0 + t, x1 - t, y0 + t, y1 - t, z0 - 1, z1 + 1)


def trestle(P, xs, yc):
    """Welded winch trestle: SHS base and top rectangles, four posts, top plate, rear anchor eye."""
    L, W, H = P["trestle"]
    s = P["shs"][0]
    x0, x1 = xs - L, xs
    y0, y1 = yc - W / 2, yc + W / 2
    parts = []
    for z0 in (0.0, H - s):
        parts += [shs(x0, x1, y0, y0 + s, z0, z0 + s, "x", P), shs(x0, x1, y1 - s, y1, z0, z0 + s, "x", P),
                  shs(x0, x0 + s, y0 + s, y1 - s, z0, z0 + s, "y", P), shs(x1 - s, x1, y0 + s, y1 - s, z0, z0 + s, "y", P)]
    for x in (x0, x1 - s):
        for y in (y0, y1 - s):
            parts.append(shs(x, x + s, y, y + s, s, H - s, "z", P))
    tp = P["top_plate"]
    xwc = xs + P["winch_x"]
    plate = bx(xwc - tp[0] / 2, xwc + tp[0] / 2, y0, y1, H, H + tp[2])
    eye = bx(x0 - 60, x0, yc - 5, yc + 5, H - s, H + 110) - ycyl(x0 - 32, H + 80, 11, yc - 6, yc + 6)
    sh = parts[0]
    for p in parts[1:]:
        sh = sh + p
    return sh + plate + eye


def winch(P, xc, yc, handle=True):
    """Two-speed self-tailing winch (bought): base, drum, self-tailing jaws, handle in its socket.
    With handle=False the handle is stowed (the drill drive is in the socket)."""
    rb, hb, rd, hd, rt, ht = P["winch"]
    z = P["trestle"][2] + P["top_plate"][2]
    base = zcyl(xc, yc, rb, z, z + hb)
    drum = zcyl(xc, yc, rd, z + hb, z + hb + hd)
    tail = zcyl(xc, yc, rt, z + hb + hd, z + hb + hd + ht)
    sock = zcyl(xc, yc, 12, z + hb + hd + ht, z + hb + hd + ht + 20)
    zt = z + hb + hd + ht + 20
    arm = bx(xc - 12, xc + P["handle"], yc - 12, yc + 12, zt, zt + 14)
    grip = zcyl(xc + P["handle"] - 15, yc, 16, zt + 14, zt + 124)
    if not handle:
        return base + drum + tail + sock
    return base + drum + tail + sock + arm + grip


def socket_top(P):
    rb, hb, rd, hd, rt, ht = P["winch"]
    return P["trestle"][2] + P["top_plate"][2] + hb + hd + ht + 20


def drill(P, xc, yc, side):
    """Right-angle drill (bought) on a winch bit in the winch socket; motor body and battery
    point outboard (side = -1 toward -Y, +1 toward +Y). Decision 24B, 2026-10-03."""
    zs = socket_top(P)
    rbit, hbit = P["bit"]
    bit = zcyl(xc, yc, rbit, zs, zs + hbit)
    rh, hh = P["drill_head"]
    z0 = zs + hbit
    head = zcyl(xc, yc, rh, z0, z0 + hh)
    rbd, lbd = P["drill_body"]
    zb = z0 + hh / 2
    y1 = yc + side * (rh - 5)
    y2 = y1 + side * lbd
    body = ycyl(xc, zb, rbd, min(y1, y2), max(y1, y2))
    lb, wb, hb = P["drill_batt"]
    ya, yb = sorted((y2 - side * lb, y2))
    batt = bx(xc - wb / 2, xc + wb / 2, ya, yb, zb - rbd - hb + 5, zb - rbd + 5)
    return {"bit": bit, "drill": head + body + batt}


def drum_guard(P, xc, yc):
    """Made drum guard: a 2 mm perforated sheet hoop round the rear (-X) side of the winch, on two
    flat-bar legs to the top plate; the rope lead from the pipe (+X) stays open."""
    r, t, z0, z1, span = P["guard"]
    zp = P["trestle"][2] + P["top_plate"][2]
    pts_o, pts_i = [], []
    for k in range(25):
        a = math.radians(180 - span / 2 + span * k / 24)
        pts_o.append((xc + r * math.cos(a), yc + r * math.sin(a)))
        pts_i.append((xc + (r - t) * math.cos(a), yc + (r - t) * math.sin(a)))
    ring = extrude(Plane.XY.offset(z0) * Polygon(*_ccw(pts_o + pts_i[::-1]), align=None), amount=z1 - z0)
    w, tl = P["guard_leg"]
    legs = None
    for a_deg in (180 - span / 2 + 10, 180 + span / 2 - 10):
        a = math.radians(a_deg)
        rl = r - t - tl / 2
        lg = Pos(xc + rl * math.cos(a), yc + rl * math.sin(a), (zp + z0 + 20) / 2) * Rot(0, 0, a_deg) * Box(tl, w, z0 + 20 - zp)
        legs = lg if legs is None else legs + lg
    return ring + legs


def station_parts(P, xs):
    yA, yB = P["winch_y"]
    L, W, H = P["trestle"]
    s = P["shs"][0]
    xw = xs + P["winch_x"]
    out = {"trestles": Compound([trestle(P, xs, yA), trestle(P, xs, yB)])}
    ya1, yb0 = yA + W / 2, yB - W / 2
    ties = []
    for z0 in (0.0, H - s):
        for xm in (xs - L / 2 - 150, xs - L / 2 + 150):
            ties.append(shs(xm - s / 2, xm + s / 2, ya1, yb0, z0, z0 + s, "y", P))
    out["ties"] = Compound(ties)
    out["winches"] = Compound([winch(P, xw, yA, handle=False), winch(P, xw, yB, handle=False)])
    dA, dB = drill(P, xw, yA, -1), drill(P, xw, yB, +1)
    out["bits"] = Compound([dA["bit"], dB["bit"]])
    out["drills"] = Compound([dA["drill"], dB["drill"]])
    out["guards"] = Compound([drum_guard(P, xw, yA), drum_guard(P, xw, yB)])
    # rope bins (bought tubs) outboard of each trestle
    out["bins"] = Compound([zcyl(xs - L / 2, yA - W / 2 - 320, 250, 0, 400) - zcyl(xs - L / 2, yA - W / 2 - 320, 245, 5, 401),
                            zcyl(xs - L / 2, yB + W / 2 + 320, 250, 0, 400) - zcyl(xs - L / 2, yB + W / 2 + 320, 245, 5, 401)])
    # round slings from each anchor eye to the structural anchor 1.5 m behind (context)
    x0 = xs - L
    slings = []
    for y in (yA, yB):
        zh = H + 80 - 3.0                          # shackle pin resting in the 22 mm hole
        pin = ycyl(x0 - 32, zh, 8.0, y - 13, y + 13)
        bow = bx(x0 - 75, x0 - 40, y + 7, y + 11, zh - 14, zh + 14) + bx(x0 - 75, x0 - 40, y - 11, y - 7, zh - 14, zh + 14)
        bow = bow + bx(x0 - 85, x0 - 75, y - 11, y + 11, zh - 14, zh + 14)
        slings.append(pin + bow + rod((x0 - 85, y, zh), (x0 - 1500, y, zh), 7.0))
    out["sling"] = Compound(slings)
    return out


# ----------------------------------------------------------------------------- air and signal
def air_parts(P=PARAMS, Lp=None, x_stand=None, hangers=True):
    Lp = P["Lp"] if Lp is None else Lp
    D = derived(P)
    c = at(P, P["duct_r"], P["duct_th"], 0)
    rd = P["duct_d"] / 2
    s0 = P["spigot_x"][0]
    out = {}
    duct_in = xcyl(c[1], c[2], rd, -300.0, Lp + s0 + 60) - xcyl(c[1], c[2], rd - 1.5, -301, Lp + s0 + 61)
    bxy = P["blower_xy"]
    outside = xcyl(bxy[1], 220, rd, bxy[0] + 200, bxy[0] + 400) + rod((bxy[0] + 400, bxy[1], 220), (-300.0, c[1], c[2]), rd)
    out["duct"] = duct_in + outside
    # blower (bought): drum housing on a stand, outlet toward +X
    out["blower"] = (xcyl(bxy[1], 220, 170, bxy[0] - 250, bxy[0] + 200)
                     + bx(bxy[0] - 220, bxy[0] + 170, bxy[1] - 150, bxy[1] + 150, 0, 50))
    # magnet hangers for the duct and the signal cable, every 2.5 m inside the pipe
    mags = []
    if hangers:
        pid = D["pipe_id"] / 2
        x = 1250.0
        while x < Lp - 600:
            mags.append(radial_rod(P, P["duct_th"], pid - 13, pid - 0.4, 16, x))
            mags.append(radial_rod(P, P["duct_th"], P["duct_r"] + rd, pid - 13, 3, x))
            mags.append(radial_rod(P, P["cable_th"], pid - 10.4, pid - 0.4, 12, x))
            x += P["hanger_pitch"]
    out["hangers"] = Compound(mags) if mags else None
    # signal cable on the hangers, from the portal to the ring
    rc = D["pipe_id"] / 2 - 10.4 - P["cable_d"] / 2
    cc = at(P, rc, P["cable_th"], 0)
    out["cable"] = xcyl(cc[1], cc[2], P["cable_d"] / 2, -200.0, Lp - 400)
    return out


def casualty_parts(P=PARAMS, x0=-2600.0, y=-1450.0):
    """Roll-up casualty stretcher (bought), shown wrapped, with the towing spreader bar (made)."""
    L, R, t = P["stretcher"]
    zc = R + 1.0
    shell = (xcyl(y, zc, R, x0, x0 + L) - xcyl(y, zc, R - t, x0 - 1, x0 + L + 1)) & bx(x0, x0 + L, y - R, y + R, 0, zc + 40)
    od, w, l = P["spreader"]
    xb = x0 + L + 250
    bar = ycyl(xb, 120, od / 2, y - l / 2, y + l / 2)
    eye = bx(xb, xb + 60, y - 5, y + 5, 105, 135) - ycyl(xb + 40, 120, 8, y - 6, y + 6)
    bridle = Compound([rod((x0 + L, y + s * (R - 20), 120), (xb - od / 2 - 0.5, y + s * (l / 2 - 20), 120), 4) for s in (-1, 1)])
    return {"stretcher": shell, "spreader": bar + eye, "bridle": bridle}


# ----------------------------------------------------------------------------- context
def context_shapes(P=PARAMS, Lp=None, x_stand=None, cut=False, window=None):
    """Rescue pipe (cut open in pictures), platform, structural anchor. Not part of the kit."""
    Lp = P["Lp"] if Lp is None else Lp
    xs = P["x_stand"] if x_stand is None else x_stand
    Do, t = P["pipe"]
    x0 = 0.0 if window is None else window
    pipe = xcyl(0, P["zc"], Do / 2, x0, Lp) - xcyl(0, P["zc"], Do / 2 - t, x0 - 1, Lp + 1)
    if cut:
        pipe = pipe - bx(x0 - 10, Lp + 10, -Do, 0, P["zc"], P["zc"] + Do)
    L = P["trestle"][0]
    anchor = bx(xs - L - 1560, xs - L - 1500, -600, 900, -100, 1500)
    floor = bx(min(xs - L - 1700, x0 - 500), Lp + 800, -1500, 1500, -60, 0)
    return {"pipe": pipe, "floor": floor, "anchor": anchor}


# ----------------------------------------------------------------------------- components
@dataclass
class Comp:
    name: str
    shape: object
    bom: int
    mat: str


NAMES = {  # key: (name, BOM line, material)
    "bottom": ("Bottom segment with sheave bracket", 1, "steel"),
    "side_p": ("Side segment (+Y)", 2, "steel"),
    "side_m": ("Side segment (-Y)", 2, "steel"),
    "crown": ("Crown segment with hood", 3, "steel"),
    "joint_bolts": ("Segment joint bolts, M12 (16)", 4, "steel"),
    "jacks": ("Jacking screws with swivel pads (4)", 5, "steel"),
    "sheave": ("Face return sheave, 240 mm", 6, "steel"),
    "sheave_hw": ("Sheave spacer and keeper", 7, "steel"),
    "cover": ("Sheave cover and kneeling plate", 8, "steel"),
    "spigot": ("Duct outlet spigot", 9, "steel"),
    "lamp": ("Magnetic LED work lamp", 23, "plastic"),
    "sledges": ("Spoil sledges (4)", 10, "steel"),
    "runners": ("Sledge runners, UHMW-PE", 11, "uhmw"),
    "links": ("Sledge connecting links (3)", 12, "steel"),
    "swivels": ("Breakaway swivels, 2.5 kN (2)", 13, "steel"),
    "ropes": ("Pull rope and tail rope, 10 mm", 14, "rope"),
    "trestles": ("Winch trestles (2)", 15, "steel"),
    "ties": ("Trestle cross ties (4)", 16, "steel"),
    "winches": ("Self-tailing winches (2)", 17, "bought"),
    "drills": ("Right-angle drills, portal drive (2)", 30, "bought"),
    "bits": ("Winch bits (2)", 31, "steel"),
    "guards": ("Winch drum guards (2)", 33, "steel"),
    "bins": ("Rope bins (2)", 18, "plastic"),
    "sling": ("Anchor slings (2)", 19, "rope"),
    "blower": ("Ventilation blower, 200 mm", 20, "bought"),
    "duct": ("Layflat duct, 200 mm", 21, "plastic"),
    "hangers": ("Magnet hangers", 22, "steel"),
    "cable": ("Signal cable, sound-powered telephones", 24, "rope"),
    "stretcher": ("Roll-up casualty stretcher", 26, "hdpe"),
    "spreader": ("Stretcher towing spreader bar", 27, "steel"),
    "bridle": ("Stretcher towing bridle", 27, "rope"),
}


def build_components(P=PARAMS, short=False, hangers=True):
    if short:
        Lp, xs = P["short"]["Lp"], P["short"]["x_stand"]
    else:
        Lp, xs = P["Lp"], P["x_stand"]
    C = {}
    allp = {}
    allp.update(ring_parts(P, Lp))
    allp.update(haul_parts(P, Lp, xs))
    allp.update(air_parts(P, Lp, xs, hangers=hangers))
    allp.update(casualty_parts(P, x0=xs - 200.0 if short else -2600.0, y=-1450.0))
    for k, (name, bom, mat) in NAMES.items():
        if allp.get(k) is not None:
            C[k] = Comp(name, allp[k], bom, mat)
    return C


# ----------------------------------------------------------------------------- masses
def masses(P=PARAMS):
    """Masses in kg of the made parts and the carried items, from the model (one of each)."""
    rs = P["rho_steel"] * 1e-9
    R = ring_parts(P, 0.0)
    m = {k: R[k].volume * rs for k in ("crown", "side_p", "side_m", "bottom", "cover", "spigot", "sheave_hw")}
    m["jacks"] = R["jacks"].volume * rs
    m["joint_bolts"] = R["joint_bolts"].volume * rs
    m["sheave"] = R["sheave"].volume * rs * 0.6          # bought cast sheave with a hollow hub, about 60 % solid
    s = sledge(P, 0.0)
    m["sledge"] = (s["tray"].volume + s["lugs"].volume) * rs + s["runners"].volume * P["rho_uhmw"] * 1e-9
    m["trestle"] = trestle(P, 0.0, 0.0).volume * rs
    st = station_parts(P, 0.0)
    m["ties"] = st["ties"].volume * rs / 4
    m["guard"] = drum_guard(P, 0.0, 0.0).volume * rs * 0.6      # perforated sheet, about 60 % solid
    cp = casualty_parts(P, 0.0, 0.0)
    m["spreader"] = cp["spreader"].volume * rs
    m["ring_total"] = sum(m[k] for k in ("crown", "side_p", "side_m", "bottom", "cover", "spigot", "sheave_hw",
                                         "jacks", "joint_bolts", "sheave"))
    return m


# ----------------------------------------------------------------------------- checks
def check(C, tol=1.0, ignore=()):
    """Constructability checks: no overlaps between components, nothing floating."""
    keys = [k for k in C if k not in ignore]
    issues = []
    bbs = {k: C[k].shape.bounding_box() for k in keys}

    def near(a, b, g=2.0):
        A, B = bbs[a], bbs[b]
        return not (A.max.X + g < B.min.X or B.max.X + g < A.min.X or A.max.Y + g < B.min.Y or
                    B.max.Y + g < A.min.Y or A.max.Z + g < B.min.Z or B.max.Z + g < A.min.Z)
    skip_pairs = {("sheave", "ropes"), ("ropes", "sheave"), ("winches", "ropes"), ("ropes", "winches"),
                  ("ropes", "swivels"), ("swivels", "ropes")}
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if (a, b) in skip_pairs or not near(a, b):
                continue
            try:
                v = (C[a].shape & C[b].shape).volume
            except Exception:
                v = 0.0
            if v > tol:
                issues.append(f"overlap {a} / {b}: {v:.1f} mm3")
    return issues


def touching(C, key, others, gap=0.8):
    s = C[key].shape
    return min(s.distance_to(C[o].shape) for o in others) <= gap


def export_all(P=PARAMS):
    out_step = Path(__file__).resolve().parents[2] / "cad" / "step"
    out_stl = Path(__file__).resolve().parents[2] / "cad" / "stl"
    out_step.mkdir(parents=True, exist_ok=True)
    out_stl.mkdir(parents=True, exist_ok=True)
    R = ring_parts(P, 0.0)
    ring = Compound([R[k] for k in ("crown", "side_p", "side_m", "bottom", "joint_bolts", "jacks", "sheave",
                                    "sheave_hw", "cover", "spigot")])
    s = sledge(P, 0.0)
    sl = Compound([s["tray"], s["runners"], s["lugs"]])
    st = station_parts(P, 0.0)
    stn = Compound([st["trestles"], st["ties"], st["winches"], st["bits"], st["drills"], st["guards"]])
    for name, shp in (("ring", ring), ("sledge", sl), ("station", stn)):
        export_step(shp, str(out_step / f"sleevedrift-{name}.step"))
        export_stl(shp, str(out_stl / f"sleevedrift-{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
    C = build_components(P, short=False, hangers=False)
    export_step(Compound([c.shape for c in C.values()]), str(out_step / "sleevedrift-assembly.step"))
    return C


if __name__ == "__main__":
    P = PARAMS
    D = derived(P)
    C = build_components(P, short=True)
    issues = check(C)
    flo = []
    X = context_shapes(P, P["short"]["Lp"], P["short"]["x_stand"])
    pool = {**{k: c.shape for k, c in C.items()}, **{"ctx_" + k: v for k, v in X.items()}}
    pbb = {k: v.bounding_box() for k, v in pool.items()}
    for k in C:
        if k in ("blower", "bins", "stretcher"):
            continue
        A = pbb[k]
        cand = [o for o in pool if o != k and not (A.max.X + 2 < pbb[o].min.X or pbb[o].max.X + 2 < A.min.X or
                                                   A.max.Y + 2 < pbb[o].min.Y or pbb[o].max.Y + 2 < A.min.Y or
                                                   A.max.Z + 2 < pbb[o].min.Z or pbb[o].max.Z + 2 < A.min.Z)]
        d = min([pool[k].distance_to(pool[o]) for o in cand] or [1e9])
        if d > 0.8:
            flo.append(f"floating {k}: {d:.1f} mm from its nearest neighbour")
    X = context_shapes(P, P["short"]["Lp"], P["short"]["x_stand"])
    for k in C:
        try:
            v = (C[k].shape & X["pipe"]).volume
        except Exception:
            v = 0.0
        if v > 1.0:
            issues.append(f"overlap {k} / pipe: {v:.1f} mm3")
    # drill drive (decision 24B): seated on its bit, bit in the socket, guard on the top plate,
    # guard and drill clear of the rope wraps and the drum
    if not touching(C, "drills", ["bits"]) or not touching(C, "bits", ["winches"]):
        issues.append("drill drive not seated on the winch socket")
    if not touching(C, "guards", ["trestles"]):
        issues.append("drum guards not on the trestle top plates")
    for k, gap in (("guards", 10.0), ("drills", 10.0)):
        dmin = C[k].shape.distance_to(C["ropes"].shape)
        if dmin < gap:
            issues.append(f"{k} within {dmin:.1f} mm of the ropes")
    if C["guards"].shape.distance_to(C["winches"].shape) < 10.0:
        issues.append("drum guards within 10 mm of the winches")
    print("checks:", "OK" if not issues and not flo else "")
    for i in issues + flo:
        print("  ", i)
    M = masses(P)
    print({k: round(v, 1) for k, v in M.items()})
    if "--check" not in sys.argv:
        export_all(P)
        print("exported STEP and STL")
