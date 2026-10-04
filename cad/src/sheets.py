"""SleeveDrift drawing sheets, Rev P2 (TRL 3, constructable design SVD-DDR-002).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/SVD-DWG-001 (hooded cutting ring and face sheave, general arrangement) and
SVD-DWG-002 (portal haul station, general arrangement) as SVG, PDF and PNG from
cad/src/model.py with .kit/drawing.py. Overall sizes are dimensioned by the kit; main dimensions
and interfaces are listed in the notes, taken from PARAMS and derived(). The concept blueprint
in media/ is SVD-DWG-010; the making sketches for the build plan are SVD-DWG-101 onward
(cad/src/build_plan_media.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Compound  # noqa: E402
from drawing import Sheet  # noqa: E402
from model import PARAMS as P, derived, ring_parts, station_parts, masses  # noqa: E402

DATE = "2026-10-03"
REVS = [("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
        ("P2", "SVD-DDR-002: design for construction", DATE, "AC")]
REVS2 = REVS + [("P3", "SVD-DDR-003: drill drive on each winch, drum guards", DATE, "AC")]


def safe_project_views(part, workdir, line_weight=0.35):
    """Front, top, right and iso views, edge by edge, so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center()
    d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out = {}
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    pass
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    return out


def ring_sheet(D, M):
    R = ring_parts(P, 0.0)
    keys = ["crown", "side_p", "side_m", "bottom", "joint_bolts", "jacks", "sheave", "sheave_hw", "cover", "spigot"]
    work = ROOT / "cad" / "drawings" / "_views1"
    views = safe_project_views(Compound([R[k] for k in keys]), work, line_weight=0.3)
    s = Sheet(project="SleeveDrift", title="Hooded cutting ring and face sheave: general arrangement", dwg_no="SVD-DWG-001",
              rev="P2", author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="5 mm S355 rolled plate segments, bought sheave and fasteners per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=REVS)
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 92, label="Isometric view", sublabel="Not to scale; seen from the front right and above")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Ring 760 OD x 5 shell, {D['ring_len']:.0f} long: {P['ring_in']:.0f} inside the pipe, {P['ring_out']:.0f} beyond the mouth",
        f"Hood: crown runs on {P['hood']:.0f} beyond the ring front; tip {D['x_hood']:.0f} from the mouth",
        "Segments: crown 120 deg (3), sides 90 deg (2), bottom 60 deg (1)",
        "Joints at 60, 150, 210, 300 deg from the top; flanges 50 x 10 inside",
        "Four M12 8.8 bolts per joint (4), 120 pitch, 25 in from the shell",
        "Ring rests on the pipe invert; 20 gap at the crown",
        "Jacking screws M20 (5) at 15 deg either side of the top and 80 deg; 175 inside the mouth",
        f"Face sheave 240 pitch (6) on a 25 pin, rope plane {P['rope_z']:.0f} above the platform",
        "Rope legs 240 apart: train lane y = -10, return leg y = +230",
        "Cover and kneeling plate 4 mm (8) on four posts, top 234 up",
        "Duct spigot 194 x 2 (9) on two saddles at 40 deg, 265 off the pipe axis",
        f"Heaviest piece: crown {M['crown']:.1f} kg; ring set {M['ring_total']:.0f} kg",
        "Third-angle; front view from -Y; X toward the face; (n) = BOM line",
    ], x=276, y=135, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "SVD-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote", out)


def station_sheet(D, M):
    st = station_parts(P, 0.0)
    work = ROOT / "cad" / "drawings" / "_views2"
    views = safe_project_views(Compound([st["trestles"], st["ties"], st["winches"], st["bits"], st["drills"], st["guards"]]),
                               work, line_weight=0.3)
    s = Sheet(project="SleeveDrift", title="Portal haul station: general arrangement", dwg_no="SVD-DWG-002", rev="P3",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="40 x 40 x 3 SHS trestles, 10 mm plate; bought winches and drills per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=REVS2)
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 92, label="Isometric view", sublabel="Not to scale; seen from the front right and above")
    s.add_notes("Main dimensions and interfaces (mm)", [
        "Two welded trestles (15), each 700 x 500, 560 high, 40 x 40 x 3 SHS",
        "Right-angle drill (30) on a winch bit (31) in each socket; body outboard",
        "Drill in high gear only, 120 rpm; clutch about 35 N m; no trigger lock",
        "Drum guard (33) round the rear 120 deg, 260 dia, two legs to the top plate",
        "Winch handles stowed; hand cranking is the fallback",
        f"Trestle {M['trestle']:.1f} kg; carried and set one at a time",
        "Top plate 300 x 500 x 10, drilled to the winch base pattern",
        "Winch A (pull rope) at y = -200; winch B (tail rope) at y = +440",
        "Winch centres 300 back from the trestle front (+X face)",
        "Rope reaches the drums about 650 up, 6 to 7 deg rising",
        "Station front 5,500 from the pipe mouth at the design case",
        "Anchor eye 22 hole 640 up; round sling (19) level to a structural anchor",
        "Rope bins (18) outboard; nobody in the rope lines while hauling",
        "Third-angle; front view from -Y; pipe mouth toward +X; (n) = BOM line",
    ], x=276, y=135, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "SVD-DWG-002")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote", out)


if __name__ == "__main__":
    D = derived(P)
    M = masses(P)
    ring_sheet(D, M)
    station_sheet(D, M)
