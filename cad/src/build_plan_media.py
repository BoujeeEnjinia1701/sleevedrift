"""SleeveDrift prototype build plan pictures (SVD-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py, so the
pictures and the model never disagree:
    docs/05-build-plan/overview.png       every component pulled apart, numbered in build order
    cad/drawings/SVD-DWG-101 to 112       making sketches for the made components
    docs/05-build-plan/joint-NN.png       close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png        one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from build123d import Pos  # noqa: E402
from model import (PARAMS as P, derived, ring_parts, sledge, station_parts, casualty_parts, build_components,  # noqa: E402
                   context_shapes, at, bx, link_between, swivel, xcyl)

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
D = derived(P)
R = ring_parts(P, 0.0)                    # face end with the pipe mouth at x = 0
ST = station_parts(P, 0.0)                # station with its front at x = 0
CP = casualty_parts(P, 0.0, 0.0)
SL = sledge(P, 0.0)
PR = dict(P, zc=P["zc"] - P["ring_drop"])  # ring axis frame
Do, tw = P["pipe"]
PIPE_WIN = (xcyl(0, P["zc"], Do / 2, -900, 0) - xcyl(0, P["zc"], Do / 2 - tw, -901, 1)) - bx(-910, 10, -Do, 0, P["zc"], P["zc"] + Do)

COL = {"bottom": "#0F766E", "side_p": "#14B8A6", "side_m": "#14B8A6", "crown": "#C2410C", "joint_bolts": "#111827",
       "jacks": "#1D4ED8", "sheave": "#D4A017", "sheave_hw": "#6B7280", "cover": "#475569", "spigot": "#7C3AED",
       "lamp": "#FACC15", "sledges": "#2563EB", "runners": "#94A3B8", "links": "#111827", "swivels": "#DC2626",
       "ropes": "#E11D48", "trestles": "#0E7490", "ties": "#155E75", "winches": "#6B7280", "bins": "#F97316",
       "drills": "#DC2626", "bits": "#111827", "guards": "#475569",
       "sling": "#FB923C", "blower": "#CA8A04", "duct": "#65A30D", "hangers": "#374151", "cable": "#111827",
       "stretcher": "#EA580C", "spreader": "#7C2D12", "bridle": "#E11D48", "pipe": "#D1D5DB"}


def part(name, shape, key, explode=(0, 0, 0)):
    return Part(name, shape, COL[key], None, tuple(explode))


def crop(shape, x0, x1, y0, y1, z0, z1):
    return shape & bx(x0, x1, y0, y1, z0, z1)


def ctx_pipe():
    return Part("Rescue pipe end (cut open)", PIPE_WIN, COL["pipe"])


# ----------------------------------------------------------------- overview
def overview():
    sy, ty, cy = -1700.0, 2300.0, -2900.0
    items = [
        ("Bottom segment with sheave bracket", R["bottom"], "bottom", (0, 0, -350)),
        ("Side segments (2)", Pos(0, 550, 0) * R["side_p"] + Pos(0, -550, 0) * R["side_m"], "side_p", (0, 0, 0)),
        ("Crown segment with hood", R["crown"], "crown", (0, 0, 550)),
        ("Jacking screws with swivel pads (4)", R["jacks"], "jacks", (0, 0, 1000)),
        ("Sheave spacer and keeper", R["sheave_hw"], "sheave_hw", (800, 0, 150)),
        ("Sheave cover and kneeling plate", R["cover"], "cover", (800, 0, 350)),
        ("Duct outlet spigot", R["spigot"], "spigot", (-800, 0, 450)),
        ("Spoil sledge (4 alike)", SL["tray"] + SL["lugs"], "sledges", (-500, sy, 0)),
        ("Winch trestles (2)", ST["trestles"], "trestles", (1400, ty, 0)),
        ("Trestle cross ties (4)", ST["ties"], "ties", (1400, ty, 300)),
        ("Stretcher spreader bar", CP["spreader"], "spreader", (-1200, cy, 0)),
        ("Winch drum guards (2)", ST["guards"], "guards", (1400, ty, 800)),
        ("Segment joint bolts (16), bought", R["joint_bolts"], "joint_bolts", (-800, 0, -300)),
        ("Face return sheave, bought", R["sheave"], "sheave", (800, 0, 0)),
        ("Sledge runners, bought strip", SL["runners"], "runners", (-500, sy, -150)),
        ("Self-tailing winches (2), bought", ST["winches"], "winches", (1400, ty, 500)),
        ("Right-angle drills on winch bits (2), bought", ST["drills"] + ST["bits"], "drills", (1400, ty, 1100)),
        ("Roll-up stretcher, bought", CP["stretcher"], "stretcher", (-1200, cy, 0)),
    ]
    parts = [part(n, s, k, e) for n, s, k, e in items]
    bv.overview(parts, OUT / "overview.png", "SleeveDrift prototype: every component in build order",
                subtitle="Made parts first (1 to 12), then the main bought parts; ropes, duct, blower, signal line, lamps, monitors and tools not shown",
                key=True, size=(11, 7.5))


# ----------------------------------------------------------------- making sketches
def sheets():
    ring_n = [Part(k, R[k], "#D1D5DB") for k in ("crown", "side_p", "side_m", "bottom", "cover", "sheave", "spigot")]
    st_n = [Part(k, v, "#D1D5DB") for k, v in ST.items() if k not in ("sling", "bins", "drills", "bits", "guards")]
    xw, yA = P["winch_x"], P["winch_y"][0]
    gd_n = [Part("winch", crop(ST["winches"], xw - 300, xw + 300, yA - 300, yA + 300, 0, 1000), "#D1D5DB"),
            Part("plate", crop(ST["trestles"], xw - 300, xw + 300, yA - 300, yA + 300, 540, 600), "#D1D5DB")]
    S = [
        ("SVD-DWG-101", "Bottom segment with sheave bracket: making sketch", R["bottom"], "bottom", ring_n,
         "5 mm S355 plate, 50 x 10 and 60 x 10 flat, 10 mm plate, 25 mm and 20 mm bar",
         ["Shell: 5 mm plate rolled to 760 OD, 60 deg of arc (398 long on the outside), 450 long",
          "Flanges 50 x 10 along both long edges, inside, flush with the edge faces",
          "Cutting band 60 x 10 rolled to fit inside the front edge; grind the front to a 30 deg bevel",
          "Drill four 13 holes per flange at 120 pitch, 25 in from the shell, with the side segment clamped on",
          "Saddles 10 mm cut to the shell curve, 325 apart; base plate 345 x 195 x 10, top 135 above the shell inside",
          "Sheave pin 25 bar, 60 above the plate, 35 from its left edge, 170 from its rear edge; 6 cross hole",
          "Four 20 bar posts 80 long on the plate corners, tapped M8 at the top",
          "Check: sits flat on a 760 template; pin square to the plate within 0.5 deg"]),
        ("SVD-DWG-102", "Side segment (two, mirrored): making sketch", R["side_p"], "side_p", ring_n,
         "5 mm S355 plate, 50 x 10 and 60 x 10 flat, M20 weld nut",
         ["Shell: 5 mm plate rolled to 760 OD, 90 deg of arc (597 long on the outside), 450 long",
          "Flanges 50 x 10 along both long edges, inside, flush with the edge faces",
          "Cutting band 60 x 10 inside the front edge, front ground to a 30 deg bevel",
          "M20 weld nut inside, 20 deg round from the crown joint, 25 from the rear edge",
          "22 hole through the shell under the nut for the jacking screw",
          "Make one for each side: the nut is on the upper part of each segment",
          "Check: matches the 760 template within 2 mm; flange faces flat"]),
        ("SVD-DWG-103", "Crown segment with hood: making sketch", R["crown"], "crown", ring_n,
         "5 mm S355 plate, 50 x 10 and 60 x 10 flat, 25 mm plate, M20 weld nuts",
         ["Shell: 5 mm plate rolled to 760 OD, 120 deg of arc (796 long on the outside), 700 long",
          "The rear 450 is the ring; the front 250 is the hood that reaches past the other segments",
          "Flanges 50 x 10 run the full 700 and stiffen the hood edges",
          "Hood lip 60 x 10 rolled inside the front edge",
          "Two M20 weld nuts 15 deg either side of the top, 25 from the rear edge, with 22 holes through",
          "Two saddles from 25 plate at 40 deg from the top, cut to the 194 spigot, 60 long",
          "Check: rest the hood on the floor; the lip touches all along"]),
        ("SVD-DWG-104", "Jacking screw with swivel pad: making sketch", R["jacks"] & bx(-300, 0, 0, 200, 600, 900), "jacks", ring_n,
         "M20 x 90 class 8.8 set screw, mild steel bar for the pad",
         ["Four alike; screw bought, pad turned",
          "Pad 50 diameter x 7, ball seat 10 deep for the screw tip",
          "Round the screw tip to a 12 radius so the pad can tilt 5 deg",
          "Locknut on the screw inside the nut",
          "Pad sits against the pipe wall; the screw pushes it out",
          "Check: pad swivels freely on the tip"]),
        ("SVD-DWG-105", "Sheave spacer and keeper: making sketch", R["sheave_hw"], "sheave_hw", ring_n,
         "40 x 7.5 mm tube, 5 mm plate",
         ["Spacer 40 OD, 25.5 bore, 20 long, under the sheave",
          "Keeper washer 44 OD, 25.5 bore, 5 thick, above the sheave",
          "R-clip through the 6 cross hole in the pin above the keeper",
          "Check: the sheave turns freely between them"]),
        ("SVD-DWG-106", "Sheave cover and kneeling plate: making sketch", R["cover"], "cover", ring_n,
         "4 mm chequer plate",
         ["Plate 345 x 300 x 4, chequer side up",
          "Four 9 holes on the post centres: 321 x 171 apart",
          "Overhangs the base plate by 105 on the left, over the return rope",
          "Break all edges; paint the -X edge yellow",
          "Check: four M8 screws enter the posts without forcing"]),
        ("SVD-DWG-107", "Duct outlet spigot: making sketch", R["spigot"], "spigot", ring_n,
         "194 x 2 mm steel tube",
         ["Tube 194 OD x 2, 410 long",
          "Roll a 3 bead 20 from the rear end so the duct cannot pull off",
          "Sits in the two crown saddles; held with two band clamps",
          "Its front end is 50 past the pipe mouth, under the hood",
          "Check: the duct end slides over it by hand"]),
        ("SVD-DWG-108", "Spoil sledge: making sketch", SL["tray"] + SL["lugs"] + SL["runners"], "sledges",
         [Part("ropes", SL["runners"], "#D1D5DB")],
         "1.5 mm galvanised sheet, 8 mm plate, UHMW-PE strip",
         ["Tray: base 160 wide, sides flaring to 300 at 130 high, 1,000 long; folded in one piece",
          "End plates welded or riveted; hand holes 100 x 40 in both ends",
          "Lugs 8 mm, 50 x 40, on the centre line, 16 hole 30 out from the end plate, 50 above the tray floor",
          "Two runners 40 x 10 under the base, 110 apart on centres, countersunk M6 screws",
          "Holds 29.9 L struck: about 51 kg of spoil",
          "Check: rocks less than 3 mm on a 780 pipe section"]),
        ("SVD-DWG-109", "Winch trestle: making sketch", ST["trestles"] & bx(-800, 100, -500, 100, -10, 800), "trestles", st_n,
         "40 x 40 x 3 SHS, 10 mm plate",
         ["Base and top rectangles 700 x 500 outside; four posts, 560 high overall",
          "Long rails full length; short rails between them; posts on the long rails",
          "Top plate 300 x 500 x 10 across the top rails, centred 300 from the front",
          "Drill the top plate to the winch base pattern of the winch bought",
          "Anchor eye 10 plate on the rear top rail, centre line; 22 hole 640 up",
          "Two 11 holes in each long rail for the cross ties",
          "Check: diagonals of each rectangle within 3 mm; sits without rocking"]),
        ("SVD-DWG-110", "Trestle cross tie: making sketch", ST["ties"] & bx(-560, -440, 0, 300, -10, 50), "ties", st_n,
         "40 x 40 x 3 SHS, 6 mm plate",
         ["Four alike: 140 long between the trestles",
          "End plates 6 mm, 80 x 40, two 11 holes 60 apart",
          "M10 bolts through the end plates and the trestle rails",
          "Two at the top rails and two at the base rails",
          "Check: trestles stand 140 apart and square"]),
        ("SVD-DWG-111", "Stretcher towing spreader bar: making sketch", CP["spreader"], "spreader",
         [Part("stretcher", CP["stretcher"], "#D1D5DB")],
         "26.9 x 2.6 mm tube, 10 mm plate",
         ["Tube 26.9 x 2.6, 450 long; bridle holes 10 at 20 from each end",
          "Towing eye 10 plate, 60 x 30, 16 hole, welded at the centre",
          "Bridle legs of 10 mm rope from the bar ends to the stretcher's head grommets",
          "The breakaway swivel clips to the eye",
          "Check: the bar sits square when both legs are pulled"]),
        ("SVD-DWG-112", "Winch drum guard: making sketch", crop(ST["guards"], xw - 300, xw + 300, yA - 300, yA + 300, 0, 1000), "guards", gd_n,
         "2 mm perforated steel sheet, 30 x 5 mm flat bar",
         ["Two alike: a hoop 260 outside diameter round the rear 120 deg of the winch",
          "Sheet 2 mm perforated, 175 high, rolled; top edge 790 above the ground",
          "Two legs 30 x 5 flat, 65 long, welded inside the hoop 10 deg in from each end",
          "Each leg turned out at the foot and bolted M8 into the trestle top plate",
          "Open toward the pipe (+X) so the rope reaches the drum",
          "Check: 10 clear of the drum and rope; nothing to catch a sleeve"]),
    ]
    for dwg, title, shape, key, nb, mat, notes in S:
        bv.component_sheet(Part(title, shape, COL[key]), nb, "SleeveDrift", dwg, title, mat, notes, DATE, out_dir=str(DWG))
        print("sheet", dwg)


# ----------------------------------------------------------------- joints
def joints():
    import math
    ri = D["ri"]
    # 1 crown to side joint at 60 deg
    c = at(PR, ri - 25, 60, 0)
    r1 = (-200, 10, c[1] - 70, c[1] + 70, c[2] - 70, c[2] + 70)
    bv.joint([part("Crown segment and its flange", crop(R["crown"], *r1), "crown"),
              part("Side segment and its flange", crop(R["side_p"], *r1), "side_p"),
              part("M12 bolts, nuts and washers", crop(R["joint_bolts"], *r1), "joint_bolts")],
             OUT / "joint-01.png", "Joint 1: crown to side segment", "Flanges face to face inside the ring; four M12 bolts per joint",
             elev=20, azim=-150)
    # 2 jacking screw at 15 deg
    c = at(PR, 370, 15, P["jack_x"])
    r2 = (P["jack_x"] - 40, P["jack_x"], c[1] - 70, c[1] + 70, c[2] - 90, c[2] + 60)
    bv.joint([part("Crown shell and weld nut", crop(R["crown"], *r2), "crown"),
              part("M20 screw and swivel pad", crop(R["jacks"], *r2), "jacks"),
              part("Rescue pipe wall", crop(PIPE_WIN + (xcyl(0, P["zc"], Do / 2, -900, 0) - xcyl(0, P["zc"], Do / 2 - tw, -901, 1)), *r2), "pipe")],
             OUT / "joint-02.png", "Joint 2: jacking screw pressing the pad on the pipe", "Cut through the screw: nut welded inside the shell, pad against the pipe wall",
             elev=10, azim=-90)
    # 3 face sheave on its pin, cut through the pin
    sx, sy = P["sheave_c"]
    r3 = (sx - 170, sx + 170, sy, sy + 160, 0, 250)
    bv.joint([part("Base plate, saddle, pin and posts", crop(R["bottom"], *r3), "bottom"),
              part("Spacer and keeper", crop(R["sheave_hw"], *r3), "sheave_hw"),
              part("Sheave", crop(R["sheave"], *r3), "sheave"),
              part("Cover and kneeling plate", crop(R["cover"], *r3), "cover")],
             OUT / "joint-03.png", "Joint 3: face sheave on its pin, under the cover", "Cut through the pin: plate, spacer, sheave, keeper and R-clip, cover above",
             elev=12, azim=-90)
    # 4 sledge link
    s1, s2 = sledge(P, 0.0), sledge(P, -1150.0)
    lk = link_between(P, -150.0 + 30, -30.0)
    r4 = (-260, 110, -120, 120, 20, 180)
    bv.joint([part("Sledge end and lug", crop(s1["tray"] + s1["lugs"], *r4), "sledges"),
              part("Next sledge end and lug", crop(s2["tray"] + s2["lugs"], *r4), "runners"),
              part("Connecting link and pins", lk, "links")],
             OUT / "joint-04.png", "Joint 4: link between two sledges", "Pins through the 16 mm lug holes; split pins keep them in", elev=30, azim=-60)
    # 5 breakaway swivel at the train front
    sw, xe = swivel(P, -30.0, -1)
    rope = xcyl(0, D["lug_z"] - 1.0, 5, xe - 250, xe)
    r5 = (-420, 110, -120, 120, 20, 180)
    bv.joint([part("Front sledge lug", crop(s1["tray"] + s1["lugs"], *r5), "sledges"),
              part("Breakaway swivel, 2.5 kN", sw, "swivels"),
              part("Pull rope with eye splice", rope, "ropes")],
             OUT / "joint-05.png", "Joint 5: breakaway swivel between rope and train", "It parts at 2.5 kN so a jam cannot overload the rope or the ring", elev=24, azim=-60)
    # 6 duct spigot in the crown saddles (short layout)
    C = build_components(P, short=True, hangers=False)
    Lp = P["short"]["Lp"]
    c = at(P, P["duct_r"], P["duct_th"], 0)
    r6 = (Lp - 420, Lp + 60, c[1] - 140, c[1] + 140, c[2] - 140, c[2] + 160)
    bv.joint([part("Crown shell and saddles", crop(C["crown"].shape, *r6), "crown"),
              part("Duct outlet spigot", crop(C["spigot"].shape, *r6), "spigot"),
              part("Layflat duct end", crop(C["duct"].shape, *r6), "duct")],
             OUT / "joint-06.png", "Joint 6: duct over the outlet spigot", "The spigot sits in two saddles inside the crown; band clamps hold both", elev=25, azim=-130)
    # 7 winch on the trestle top plate
    xw = P["winch_x"]
    yA = P["winch_y"][0]
    r7 = (xw - 200, xw + 200, yA - 260, yA + 260, 480, 1000)
    bv.joint([part("Trestle top rails and plate", crop(ST["trestles"], *r7), "trestles"),
              part("Self-tailing winch (handle stowed)", crop(ST["winches"], *r7), "winches")],
             OUT / "joint-07.png", "Joint 7: winch on its trestle", "Winch base bolted through the 10 mm top plate with its own bolts", elev=22, azim=-55)
    # 8 anchor eye and sling
    x0 = -P["trestle"][0]
    r8 = (x0 - 300, x0 + 60, yA - 60, yA + 60, 480, 760)
    bv.joint([part("Trestle rear rail and anchor eye", crop(ST["trestles"], *r8), "trestles"),
              part("Bow shackle and round sling", crop(ST["sling"], *r8), "sling")],
             OUT / "joint-08.png", "Joint 8: sling on the anchor eye", "The sling runs level at rope height to a structural anchor behind", elev=20, azim=-60)


    # 9 drill on its winch bit in the winch socket, behind the drum guard
    r9 = (xw - 220, xw + 220, yA - 560, yA + 200, 560, 1000)
    bv.joint([part("Trestle top plate", crop(ST["trestles"], *r9), "trestles"),
              part("Winch and socket", crop(ST["winches"], *r9), "winches"),
              part("Drum guard", crop(ST["guards"], *r9), "guards"),
              part("Winch bit", crop(ST["bits"], *r9), "bits"),
              part("Right-angle drill", crop(ST["drills"], *r9), "drills")],
             OUT / "joint-09.png", "Joint 9: drill on the winch socket", "Winch bit in the socket, drill body outboard; guard round the rear of the drum",
             elev=22, azim=-55)


# ----------------------------------------------------------------- steps
def steps():
    n = 0

    def shot(done, new, title, sub, context=(), size=(8, 6), elev=24, azim=-58):
        nonlocal n
        n += 1
        if n < int(__import__("os").environ.get("SKIP_TO", "0")):
            return
        only = __import__("os").environ.get("ONLY")
        if only and str(n) not in only.split(","):
            return
        done = [p for p in done if p.shape.volume > 1.0]
        bv.step(done, new, OUT / f"step-{n:02d}.png", title, sub, context=context, label_done=False, size=size, elev=elev, azim=azim)

    yA, yB = P["winch_y"]
    from model import trestle as trestle_shape
    tA = part("Trestle A", trestle_shape(P, 0.0, yA), "trestles")
    tB = part("Trestle B", trestle_shape(P, 0.0, yB), "trestles")
    ties = part("Cross ties (4)", ST["ties"], "ties")
    win = part("Self-tailing winches", ST["winches"], "winches")
    grd = part("Drum guards", ST["guards"], "guards")
    sl = part("Round slings and shackles", ST["sling"], "sling")
    bins = part("Rope bins", ST["bins"], "bins")
    mv = lambda p, e: Part(p.name, p.shape, p.color, None, e)  # noqa: E731
    shot([tA], [mv(tB, (0, 400, 0)), mv(ties, (0, 0, 300))], "Step 1: set the trestles and bolt the cross ties",
         "On level ground 5.5 m behind the pipe mouth, in line with it; M10 bolts")
    shot([tA, tB, ties], [mv(win, (0, 0, 300)), mv(grd, (-300, 0, 300))], "Step 2: bolt the winches and drum guards to the top plates",
         "Winch A (pull rope) on the -Y trestle, winch B (tail rope) on the +Y trestle; guards behind the drums")
    shot([tA, tB, ties, win, grd], [mv(sl, (-300, 0, 0)), mv(bins, (0, 0, 300))], "Step 3: slings to the structural anchor; rope bins out",
         "Slings level at rope height, tight; never to the pipe-pushing machine")
    pipe = ctx_pipe()
    bot, sp, sm, cr = (part("Bottom segment", R["bottom"], "bottom"), part("Side segment (+Y)", R["side_p"], "side_p"),
                       part("Side segment (-Y)", R["side_m"], "side_m"), part("Crown segment", R["crown"], "crown"))
    bolts = part("Joint bolts", R["joint_bolts"], "joint_bolts")
    jk = part("Jacking screws and pads", R["jacks"], "jacks")
    shot([], [mv(bot, (-700, 0, 0))], "Step 4: set the bottom segment in the pipe mouth",
         "It rides in on a sledge; 200 mm stays inside the pipe, the bevel faces the debris", context=[pipe])
    shot([bot], [mv(sp, (-500, 150, 150)), mv(sm, (-500, -150, 150))], "Step 5: bolt the side segments to the bottom",
         "Eight M12 bolts, heads inside the ring toward the -Y side; finger tight", context=[pipe])
    shot([bot, sp, sm], [mv(cr, (-600, 0, 250)), mv(bolts, (0, 0, 0))], "Step 6: crown segment on top; tighten all joints",
         "Hood forward; all sixteen bolts to about 80 N m", context=[pipe])
    shot([bot, sp, sm, cr, bolts], [mv(jk, (0, 0, 0))], "Step 7: run the jacking screws out to the pipe wall",
         "Crown screws first to press the ring onto the invert, then the sides; about 60 N m", context=[pipe])
    shk = [part("Sheave", R["sheave"], "sheave"), part("Spacer and keeper", R["sheave_hw"], "sheave_hw")]
    shot([bot, sp, sm, cr, jk], [mv(shk[0], (0, 0, 250)), mv(shk[1], (0, 0, 350))], "Step 8: drop the sheave onto its pin",
         "Spacer, sheave, keeper washer and R-clip; the sheave turns by hand", context=[pipe])
    shot([bot, sp, sm, cr, jk] + shk, [mv(part("Cover and kneeling plate", R["cover"], "cover"), (0, 0, 250))],
         "Step 9: cover over the sheave", "Four M8 screws into the posts, open side toward the portal", context=[pipe])
    C = build_components(P, short=True, hangers=True)
    Lp = P["short"]["Lp"]
    win6 = (Lp - 1500, Lp + 600, -500, 500, -10, 900)
    pipe6 = Part("Rescue pipe (cut open)", crop(context_shapes(P, Lp, P["short"]["x_stand"], cut=True)["pipe"], *win6), COL["pipe"])
    face = [Part(C[k].name, crop(C[k].shape, *win6), "#D1D5DB") for k in ("bottom", "side_p", "side_m", "crown", "jacks", "sheave", "cover")]
    shot(face, [part("Duct outlet spigot", C["spigot"].shape, "spigot", (-400, 0, 0)),
                part("Layflat duct on magnet hangers", crop(C["duct"].shape + C["hangers"].shape, *win6), "duct", (-600, 0, 0))],
         "Step 10: duct spigot into its saddles, duct over it", "Two band clamps; hang the duct every 2.5 m on magnet hangers", context=[pipe6])
    shot(face + [Part("spigot", C["spigot"].shape, "#D1D5DB")],
         [part("Magnetic work lamp", C["lamp"].shape, "lamp", (0, 0, -200)), part("Signal cable and telephone", crop(C["cable"].shape, *win6), "cable", (-500, 0, 0))],
         "Step 11: lamp inside the hood; signal line to the face", "Telephone hung inside the ring rear; lamp aimed at the face", context=[pipe6])
    trays = [part(f"Sledge {k + 1}", Pos(-1150.0 * k, 0, 0) * (SL["tray"] + SL["lugs"] + SL["runners"]), "sledges") for k in range(4)]
    links = [part("Links", link_between(P, -1150.0 * (k + 1) + 1000 + 30, -1150.0 * k - 30), "links") for k in range(3)]
    sw1, _ = swivel(P, 1030.0, +1)
    sw2, _ = swivel(P, -1150.0 * 3 - 30, -1)
    shot(trays, [Part("Connecting links (3)", links[0].shape + links[1].shape + links[2].shape, COL["links"], None, (0, 0, 250)),
                 part("Breakaway swivels (2)", sw1 + sw2, "swivels", (0, 0, 250))],
         "Step 12: make up the train", "Four sledges, three links and a breakaway swivel at each end", size=(9, 5.5), elev=28)
    win13 = (Lp - 1800, Lp + 600, -500, 500, -10, 900)
    done13 = [Part(C[k].name, crop(C[k].shape, *win13), "#D1D5DB") for k in ("bottom", "side_p", "side_m", "sheave", "sledges", "links", "swivels")]
    shot(done13, [part("Tail rope round the sheave and back", crop(C["ropes"].shape, *win13), "ropes", (0, 0, 0))],
         "Step 13: reeve the tail rope round the face sheave", "From the train's face end round the sheave, back along the left of the floor to winch B",
         context=[Part("pipe", crop(context_shapes(P, Lp, P["short"]["x_stand"], cut=True)["pipe"], win13[0], win13[1], -500, 500, -10, 300), COL["pipe"])],
         elev=62, azim=-125)
    shot([part("Stretcher (rolled)", CP["stretcher"], "stretcher")], [part("Spreader bar and bridle", CP["spreader"] + CP["bridle"], "spreader", (400, 0, 0))],
         "Step 14: casualty stretcher ready at the portal", "Spreader bar on the head grommets; swivels clip to its eye in place of the train", size=(8, 5))
    dr = part("Drills on winch bits (2)", ST["drills"] + ST["bits"], "drills")
    shot([tA, tB, ties, win, grd], [mv(dr, (0, 0, 300))], "Step 15: drills on the winch sockets for hauling",
         "High gear only; clutch about 35 N m; handles stowed for hand cranking")
    print("steps", n)


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    OUT.mkdir(parents=True, exist_ok=True)
    for w in what:
        globals()[w]()
