"""SleeveDrift product appearance model (build123d), TRL 3, constructable design (SVD-DDR-002).

For photoreal renders only (.kit/export_views.py, then .kit/photoreal.py on Amish's Mac). Every
part is the model.py solid itself, in the shortened picture layout of model.py; colours and
materials are added for the look. The hero shows the face end: the last 2.8 m of the rescue pipe,
cut open on the camera side, with the hooded cutting ring, the face sheave under its cover, the
two face-end sledges of the train, the ropes, the duct and its outlet spigot, the signal cable
and the lamp. A posed 1.75 m mannequin stands on the platform beside the pipe's far end, clear of
the line of sight. The detail view shows the portal haul station with a right-angle drill on each
winch and the drum guards (Amish's decision 24B, 2026-10-03). Appearance additions not in
model.py, recorded in docs/REVIEW.md: the pipe window and platform slab cropped for the picture
and the mannequin. CONCEPT, NOT FOR FABRICATION.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Pos  # noqa: E402
from model import PARAMS as P, build_components, context_shapes, bx  # noqa: E402

TITLE = "SleeveDrift: hand-mining kit for crews inside a rescue pipe"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["ring", "haul", "context"], "explode": False, "el": 22, "az": -40,
     "note": "Product render from the front right and above (about 22 deg elevation): the face end of an 800 mm "
             "rescue pipe, cut open on the near side, with the hooded cutting ring, the face sheave under its "
             "kneeling cover, two spoil sledges on the haul rope, the air duct and the signal line; a 1.75 m person "
             "stands beside the pipe for scale"},
    {"name": "exploded", "groups": ["ring"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded hooded cutting ring from the front right and above (about 26 deg elevation): crown segment "
             "with hood, two side segments, bottom segment with the sheave bracket, joint bolts, jacking screws, "
             "sheave, cover and duct spigot"},
    {"name": "detail", "groups": ["station"], "explode": False, "el": 28, "az": -35,
     "note": "Detail from the front right and above (about 28 deg elevation): portal haul station with two "
             "self-tailing winches on welded trestles, each turned by a right-angle drill behind a drum guard, rope bins, anchor slings, blower and the rolled casualty "
             "stretcher; layout shortened"},
]

LOOK = {  # key: (colour, material, group, exploded offset)
    "bottom": ("#0F766E", "painted steel", "ring", (0, 0, -350)),
    "side_p": ("#14B8A6", "painted steel", "ring", (0, 450, 0)),
    "side_m": ("#14B8A6", "painted steel", "ring", (0, -450, 0)),
    "crown": ("#C2410C", "painted steel", "ring", (0, 0, 450)),
    "joint_bolts": ("#9CA3AF", "zinc plated steel", "ring", (0, 0, 0)),
    "jacks": ("#1D4ED8", "zinc plated steel", "ring", (0, 0, 700)),
    "sheave": ("#D4A017", "zinc plated steel", "ring", (0, 0, 150)),
    "sheave_hw": ("#6B7280", "steel", "ring", (0, 0, 200)),
    "cover": ("#374151", "chequer plate steel", "ring", (0, 0, 350)),
    "spigot": ("#7C3AED", "painted steel", "ring", (-500, 0, 250)),
    "lamp": ("#FACC15", "plastic", "ring", (0, 0, 900)),
    "sledges": ("#2563EB", "galvanised steel", "haul", (0, 0, 0)),
    "runners": ("#F8FAFC", "white plastic", "haul", (0, 0, 0)),
    "links": ("#111827", "steel", "haul", (0, 0, 0)),
    "swivels": ("#DC2626", "painted steel", "haul", (0, 0, 0)),
    "ropes": ("#E11D48", "polyester rope", "haul", (0, 0, 0)),
    "duct": ("#FDE047", "yellow vinyl duct", "haul", (0, 0, 0)),
    "hangers": ("#111827", "steel", "haul", (0, 0, 0)),
    "cable": ("#111827", "rubber cable", "haul", (0, 0, 0)),
    "trestles": ("#0E7490", "painted steel", "station", (0, 0, 0)),
    "ties": ("#155E75", "painted steel", "station", (0, 0, 0)),
    "winches": ("#D1D5DB", "polished aluminium", "station", (0, 0, 0)),
    "drills": ("#DC2626", "red plastic power tool", "station", (0, 0, 0)),
    "bits": ("#111827", "black oxide steel", "station", (0, 0, 0)),
    "guards": ("#4B5563", "perforated steel sheet", "station", (0, 0, 0)),
    "bins": ("#F97316", "plastic", "station", (0, 0, 0)),
    "sling": ("#7C3AED", "polyester webbing", "station", (0, 0, 0)),
    "blower": ("#FACC15", "painted steel", "station", (0, 0, 0)),
    "stretcher": ("#EA580C", "orange plastic", "station", (0, 0, 0)),
    "spreader": ("#7C2D12", "painted steel", "station", (0, 0, 0)),
    "bridle": ("#E11D48", "polyester rope", "station", (0, 0, 0)),
}


def product_parts(P=P):
    S = P["short"]
    Lp, xs = S["Lp"], S["x_stand"]
    C = build_components(P, short=True)
    X = context_shapes(P, Lp, xs, cut=True)
    face = bx(Lp - 2800, Lp + 700, -1000, 1000, -50, 1000)
    port = bx(xs - 2000, xs + 2200, -2000, 2000, -50, 1500)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    for k, c in C.items():
        color, mat, grp, ex = LOOK[k]
        shape = c.shape
        if grp == "haul":
            shape = shape & face
            if shape.volume < 1.0:
                continue
        if grp == "station":
            shape = shape & port
            if shape.volume < 1.0:
                continue
        add(c.name, shape, color, mat, c.bom, grp, ex)
    # context for the hero: pipe window, platform, and a person standing clear of the line of sight
    add("Rescue pipe, 800 mm, cut open (context)", X["pipe"] & face, "#9CA3AF", "weathered steel", None, "context", (0, 0, 0))
    add("Platform (context)", bx(Lp - 4400, Lp + 700, -1400, 1400, -60, 0), "#D6D3D1", "concrete", None, "context", (0, 0, 0))
    from context_parts import mannequin
    person = Pos(Lp - 3800.0, 900.0, 0) * mannequin(1750, "stand")
    add("Person, 1.75 m (scale)", person, "#D1D5DB", "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:44s} {p['group']:9s} {p['material']:20s} vol={s.volume / 1000:9.1f} cm3")
