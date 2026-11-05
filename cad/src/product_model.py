"""SleeveDrift product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is a part of components(CHOSEN) from cad/src/model.py exactly as it is (option A, the rope
shuttle of sledges, proposed): hooded ring segments, bands, welds, weld nuts, joint bolts, jacking screws, sheave,
sledges with runners, links and swivels, ropes, trestles, ties, slings, winches, drills, guards, blower, duct,
cable, stretcher and every fastener. Parts that run the whole length of the shortened layout (ropes, duct, cable,
runners, the pipe) are cut at the edge of the picture window; nothing is added to a part. Only the site is
added, as context parts: a tunnel floor slab, the tunnel wall behind the pipe, the debris heap the pipe has been
pushed into and a 1.75 m mannequin standing on the floor for scale. The hero is rendered by .kit/photoreal.py
as an outdoor scene on a concrete floor at model z = 0 (RENDER_VIEWS "args"); every site part reaches below
the ground. The studio view is the portal haul station alone.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "face" (the face end of the pipe with the ring and the first sledges), "station" (the portal haul
station), "context" (site and mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Pos  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part  # noqa: E402
from sd_parts import bx, prism_xz  # noqa: E402

TITLE = "SleeveDrift: hand-mining kit for crews inside a rescue pipe"

_SITE = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=38,-75", "--lens=40"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["face", "context"], "explode": False, "el": 20, "az": -42, "args": _SITE,
     "note": "Site render from the front right and above (about 20 deg elevation): the face end of an 800 mm rescue "
             "pipe pushed into a collapse in a tunnel, cut open on the near side to show the hooded cutting ring, the "
             "face sheave under its kneeling cover, two spoil sledges on the haul rope, the air duct and the signal line; "
             "a 1.75 m person stands on the tunnel floor behind the pipe for scale"},
    {"name": "studio", "groups": ["station"], "explode": False, "el": 28, "az": -35,
     "note": "Studio render from the front right and above (about 28 deg elevation): the portal haul station with "
             "two self-tailing winches on welded trestles, each turned by a right-angle drill behind a drum guard, "
             "rope bins, anchor slings, ventilation blower and the rolled casualty stretcher; layout shortened"},
]

FACE_WIN = (-3200.0, 1500.0)      # mm behind and ahead of Lp, the pipe mouth at the face
STATION_WIN = (-9000.0, 1200.0)   # absolute x, mm, of the station picture window


def _window(shape, x0, x1):
    """The part of a shape between x0 and x1, or None if it lies outside."""
    bb = shape.bounding_box()
    if bb.max.X < x0 or bb.min.X > x1:
        return None
    if bb.min.X >= x0 and bb.max.X <= x1:
        return shape
    cut = shape & (Pos((x0 + x1) / 2, 0, 500) * Box(x1 - x0, 6000, 6000))
    return cut if cut.volume > 1e-6 else None


def site():
    """Tunnel floor, wall and rubble face at the pipe's end, and a mannequin. Ground level is model z = 0
    (photoreal --ground-z=0); every site part reaches 300 mm below it."""
    Lp, xs = M.layout(True)
    out = []
    ctx = lambda n, sh, mat: out.append(part(f"{n} (site)", sh, mat, kind="context", group="context"))
    ctx("Tunnel floor slab", bx(Lp + FACE_WIN[0] - 2500, Lp + 5200, -4200, 4200, -300, 0), "concrete")
    ctx("Tunnel wall behind the pipe", bx(Lp + FACE_WIN[0] - 2500, Lp + 5200, 2600, 2900, -300, 3600), "concrete")
    # collapse debris the pipe has been pushed into: a heap across the tunnel, in front of the ring
    heap = [(Lp + 700, -300), (Lp + 700, 1150), (Lp + 1100, 1500), (Lp + 1700, 1380), (Lp + 2300, 1850), (Lp + 3200, 1250),
            (Lp + 4200, 700), (Lp + 5200, -300)]
    ctx("Collapse debris at the face", prism_xz(heap, -4200, 2600), "soil")
    try:
        import context_parts
        man = Pos(Lp - 2600.0, 1500.0, 0) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    Lp, xs = M.layout(True)
    out = []
    for p in M.components(M.CHOSEN):
        for grp, (x0, x1) in (("face", (Lp + FACE_WIN[0], Lp + FACE_WIN[1])), ("station", STATION_WIN)):
            if p["kind"] == "context":
                if grp == "station" or "Rescue pipe" not in p["name"]:
                    continue
            sh = _window(p["shape"], x0, x1)
            if sh is None:
                continue
            q = dict(p)
            q["shape"], q["group"] = sh, grp
            if p["kind"] == "context":
                q["group"] = "context"
            out.append(q)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    import collections
    print(len(ps), "parts;", dict(collections.Counter(p["group"] for p in ps)))
