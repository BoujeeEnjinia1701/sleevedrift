"""SleeveDrift concept media from the kit 1.9 detailed model (option A, the rope shuttle of sledges, proposed).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|blueprint|web|all]
With no argument it draws everything. On a small machine run one picture per process (the model has several hundred
parts). Every part is a part of components(CHOSEN) from cad/src/model.py in the shortened picture layout (a 6.8 m
length of rescue pipe instead of 60 m, the portal station 2.4 m from the mouth instead of 5.5 m), with the BOM
number of bom/bom.csv. Grey parts (the rescue pipe cut open, the platform, the anchor and a 1.75 m person) are
context only. Figures on the sheet and in the flow diagram come from docs/04-calcs/sizing.py (SVD-CAL-001).
CONCEPT, NOT FOR FABRICATION.
"""
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
import model as M  # noqa: E402

PROJECT, TITLE, DWG, DATE = "SleeveDrift", "Hand-mining rescue kit for an 800 mm pipe", "SVD-DWG-010", "2026-11-02"
MD = ROOT / "media"
GREY = "#D1D5DB"
FACE_EXPLODE = {   # face-end groups of the hooded cutting ring: exploded offset in mm
    "bottom": (0, 0, -350), "side_p": (0, 450, 0), "side_m": (0, -450, 0), "crown": (0, 0, 450), "joint_bolts": (0, 0, 0),
    "jacks": (0, 0, 650), "sheave": (0, 0, 150), "sheave_hw": (0, 0, 200), "cover": (0, 0, 350), "spigot": (-500, 0, 250),
    "lamp": (0, 0, 900)}


def _bom_names():
    import csv
    out = {}
    for r in csv.DictReader((ROOT / "bom/bom.csv").open()):
        n, _, name = r["item"].partition(" ")
        out[int(n)] = name
    return out


def parts(context=False, face_only=False):
    names = _bom_names()
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context":
            if context:
                out.append(Part(p["name"], p["shape"], GREY, None, (0, 0, 0)))
            continue
        if face_only:
            if p["group"] not in FACE_EXPLODE:
                continue
            ex = FACE_EXPLODE[p["group"]]
        else:
            ex = (0, 0, 0)
        out.append(Part(names.get(p["bom"], p["name"]), p["shape"], p["color"], p["bom"], ex))
    return out


def key_figures():
    return ["Hooded ring 760 mm OD, four bolted segments, heaviest 31 kg",
            "Hood 500 mm beyond the pipe mouth; 5 kN gives 5.5 MPa",
            "Train of four 30 L sledges; 794 N loaded pull",
            "Drill drive on each winch: 0.42 m3/h; 72 N by hand",
            "2.5 kN breakaway swivels; rope factor 6.5",
            "15 m3/min fresh air at the face over 65 m of duct",
            "Layout shortened; on site 60 m of pipe, station 5.5 m back"]


def flow_spec():
    return {"title": "energy per loaded 60 m haul of four full sledges, kJ (SVD-CAL-001 estimates, D8)", "unit": "kJ",
            "stages": [("Drill battery at the portal", 93.5), ("Drill output at the winch socket", 56.1), ("Rope at the winch", 47.7),
                       ("Train hauled 60 m", 42.2), ("Spoil delivered to the portal", "120 L, 203 kg")],
            "losses": [(0, "Drill motor and gearbox", 37.4), (1, "Winch gearing", 8.4), (2, "Rope drag and return tension", 5.5),
                       (3, "Runner friction on the pipe floor", 42.2)]}


def exploded():
    return K._render(parts(face_only=True), MD / "exploded.png", offsets=True, labels=True,
                     title="SleeveDrift: face end, exploded view",
                     note="Hooded cutting ring and face sheave seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv")


def cutaway():
    """Section on the pipe's centre plane with the -Y half removed, seen from the -Y side and above."""
    from build123d import Box, Pos
    Lp, _ = M.layout(True)
    cutter = Pos(Lp, 1500, 500) * Box(3000, 3000, 3000)
    out = []
    for p in parts(face_only=True):
        try:
            sh = p.shape & cutter
            if sh.volume > 1e-6:
                out.append(Part(p.name, sh, p.color, p.bom))
        except Exception as e:      # a part that will not cut is left out rather than shown whole
            print("not cut:", p.name, e)
    return K._render(out, MD / "cutaway.png", azim=-90, elev=18, title="SleeveDrift: face end cutaway",
                     note="-Y half removed; seen from the -Y side and above, 18 deg elevation: hood, jacking screws, sheave under its cover, duct spigot")


def hero():
    ps = K.with_scale_figure(parts(context=True))
    return K._render(ps, MD / "hero.png", title=PROJECT,
                     note="Seen from the front right and above, 24 deg elevation. Grey figure: 1.75 m person for scale")


def _tilt(ps, deg=0.006):
    """The same parts turned 0.006 degrees off every axis: the hidden-line projection of the concept sheet stalls on a view
    that looks exactly along an axis of the pipe, and this tilt (invisible at the scale of the sheet) avoids it."""
    from build123d import Rot
    return [Part(p.name, Rot(deg, deg, deg) * p.shape, p.color, p.bom, p.explode) for p in ps]


def everything():
    return K.render_all(_tilt(parts()), PROJECT, TITLE, DWG, key_figures(), date=DATE, rev="P4", cut=False, scale_figure=True,
                        web_model=False, flow=flow_spec(), context=_tilt([p for p in parts(context=True) if p.bom is None]))


def web():
    """Web model: coarse tessellation so model.glb stays under about 20 MB, with the kit's viewer page."""
    from build123d import Compound, Color, export_gltf
    import matplotlib.colors as mc
    kids = []
    for p in parts(context=True):
        if p.bom is None and "Rescue pipe" not in p.name:
            continue
        sh = copy.deepcopy(p.shape)
        sh.color = Color(*mc.to_rgb(p.color))
        sh.label = p.name
        kids.append(sh)
    defl = float(sys.argv[sys.argv.index("--deflection") + 1]) if "--deflection" in sys.argv else 0.5
    export_gltf(Compound(children=kids), str(MD / "model.glb"), binary=True, linear_deflection=defl, angular_deflection=0.5)
    (MD / "viewer.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SleeveDrift: hand-mining rescue kit concept</title>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3/dist/model-viewer.min.js"></script>
<style>body{{margin:0;font-family:system-ui,sans-serif;background:#F9FAFB}}model-viewer{{width:100vw;height:100vh}}
.tag{{position:fixed;left:12px;top:10px;font-size:12px;color:#B45309;letter-spacing:.06em}}</style></head>
<body><div class="tag">CONCEPT, NOT FOR FABRICATION</div>
<model-viewer src="model.glb" poster="hero.png" alt="SleeveDrift: hand-mining rescue kit concept" camera-controls auto-rotate shadow-intensity="0.6"
  exposure="1.0" camera-orbit="-35deg 70deg auto" interaction-prompt="auto"></model-viewer></body></html>
""")
    return MD / "model.glb", round((MD / "model.glb").stat().st_size / 1e6, 2), "MB"


if __name__ == "__main__":
    fns = {"hero": hero, "cutaway": cutaway, "exploded": exploded, "web": web, "all": everything,
           "flow": lambda: K.flow_diagram(flow_spec()["stages"], MD / "flow.png", f"{PROJECT}: {flow_spec()['title']}", "kJ",
                                          flow_spec()["losses"])}
    for w in [a for a in sys.argv[1:] if not a.startswith("--") and a.replace(".", "").isalpha()] or ["all"]:
        print(w, "->", fns[w]())
