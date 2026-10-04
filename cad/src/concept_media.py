"""SleeveDrift concept media (TRL 3, constructable design SVD-DDR-002), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes every component from cad/src/model.py in the shortened picture layout (a 6.8 m length of
rescue pipe instead of 60 m, and the portal station 2.4 m from the mouth instead of 5.5 m) and
renders the media set with .kit/concept.py: hero, exploded view of the face end with BOM callouts,
cutaway of the face end, concept blueprint, energy flow per loaded trip, and the web model
(model.glb with viewer.html). Coloured parts carry the BOM line numbers of bom/bom.csv; grey
parts (the rescue pipe, cut open, the platform and a person) are context only. Figures on the
sheet and in the flow diagram come from docs/04-calcs/sizing.py (SVD-CAL-001).
CONCEPT, NOT FOR FABRICATION.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Compound, Color, export_gltf  # noqa: E402
import matplotlib.colors as mc  # noqa: E402
import concept  # noqa: E402
from concept import Part, render_all, human_figure, cutaway_parts  # noqa: E402
from model import PARAMS as P, build_components, context_shapes  # noqa: E402

S = P["short"]
C = build_components(P, short=True)
X = context_shapes(P, S["Lp"], S["x_stand"], cut=True)

STYLE = {  # key: (colour, exploded offset in mm, face-end part)
    "bottom": ("#0F766E", (0, 0, -350), True),
    "side_p": ("#14B8A6", (0, 450, 0), True),
    "side_m": ("#14B8A6", (0, -450, 0), True),
    "crown": ("#C2410C", (0, 0, 450), True),
    "joint_bolts": ("#111827", (0, 0, 0), True),
    "jacks": ("#1D4ED8", (0, 0, 650), True),
    "sheave": ("#D4A017", (0, 0, 150), True),
    "sheave_hw": ("#6B7280", (0, 0, 200), True),
    "cover": ("#475569", (0, 0, 350), True),
    "spigot": ("#7C3AED", (-500, 0, 250), True),
    "lamp": ("#FACC15", (0, 0, 900), True),
    "sledges": ("#2563EB", (0, 0, 0), False),
    "runners": ("#F8FAFC", (0, 0, 0), False),
    "links": ("#111827", (0, 0, 0), False),
    "swivels": ("#DC2626", (0, 0, 0), False),
    "ropes": ("#E11D48", (0, 0, 0), False),
    "trestles": ("#0E7490", (0, 0, 0), False),
    "ties": ("#155E75", (0, 0, 0), False),
    "winches": ("#9CA3AF", (0, 0, 0), False),
    "drills": ("#DC2626", (0, 0, 0), False),
    "bits": ("#111827", (0, 0, 0), False),
    "guards": ("#475569", (0, 0, 0), False),
    "bins": ("#F97316", (0, 0, 0), False),
    "sling": ("#FB923C", (0, 0, 0), False),
    "blower": ("#FDE047", (0, 0, 0), False),
    "duct": ("#A3E635", (0, 0, 0), False),
    "hangers": ("#374151", (0, 0, 0), False),
    "cable": ("#111827", (0, 0, 0), False),
    "stretcher": ("#EA580C", (0, 0, 0), False),
    "spreader": ("#7C2D12", (0, 0, 0), False),
    "bridle": ("#E11D48", (0, 0, 0), False),
}
parts = [Part(c.name, c.shape, STYLE[k][0], c.bom, (0, 0, 0)) for k, c in C.items()]
face = [Part(C[k].name, C[k].shape, STYLE[k][0], C[k].bom, STYLE[k][1]) for k in C if STYLE[k][2]]

L = P["trestle"][0]
person = human_figure(1750.0, x=S["x_stand"] - L / 2, y=P["winch_y"][1] + 900.0, z=0.0)
context = [Part("Rescue pipe, 800 mm, cut open (context)", X["pipe"], "#D1D5DB"),
           Part("Structural anchor behind the station (context)", X["anchor"], "#A8A29E"), person]

flow = {"title": "energy per loaded 60 m haul of four full sledges, kJ (SVD-CAL-001 estimates, D8)", "unit": "kJ",
        "stages": [("Drill battery at the portal", 92.5), ("Drill output at the winch socket", 55.5), ("Rope at the winch", 47.2),
                   ("Train hauled 60 m", 41.7), ("Spoil delivered to the portal", "120 L, 203 kg")],
        "losses": [(0, "Drill motor and gearbox", 37.0), (1, "Winch gearing", 8.3), (2, "Rope drag and return tension", 5.5),
                   (3, "Runner friction on the pipe floor", 41.7)]}

outs = render_all(
    parts, project="SleeveDrift", title="Hand-mining rescue kit for an 800 mm pipe", dwg_no="SVD-DWG-010",
    key_figures=["Hooded ring 760 mm OD, four bolted segments, heaviest 31 kg",
                 "Hood 500 mm beyond the pipe mouth; 5 kN gives 5.5 MPa",
                 "Train of four 30 L sledges; 786 N loaded pull",
                 "Drill drive on each winch: 0.42 m3/h; 71 N by hand",
                 "2.5 kN breakaway swivels; rope factor 6.5",
                 "15 m3/min fresh air at the face over 65 m of duct",
                 "Layout shortened; on site 60 m of pipe, station 5.5 m back"],
    scale_figure=False, context=context, cut=False, web_model=False, flow=flow)

md = ROOT / "media"
concept._render(face, md / "exploded.png", offsets=True, labels=True, title="SleeveDrift: face end, exploded view",
                note="Hooded cutting ring and face sheave seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv")
cut = cutaway_parts([Part(p.name, p.shape, p.color, p.bom) for p in face], keep="+Y")
concept._render(cut, md / "cutaway.png", azim=-90, elev=18, title="SleeveDrift: face end cutaway",
                note="-Y half removed; seen from the -Y side and above, 18 deg elevation: hood, jacking screws, sheave under its cover, duct spigot")
outs["exploded"], outs["cutaway"] = md / "exploded.png", md / "cutaway.png"

# Web model at a coarse tessellation (a few MB), with the kit's viewer page
kids = []
for p in parts + context[:1]:
    sh = p.shape
    sh.color = Color(*mc.to_rgb(p.color))
    sh.label = p.name
    kids.append(sh)
export_gltf(Compound(kids), str(md / "model.glb"), binary=True, linear_deflection=1.0, angular_deflection=0.35)
(md / "viewer.html").write_text("""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SleeveDrift: hand-mining rescue kit concept</title>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3/dist/model-viewer.min.js"></script>
<style>body{margin:0;font-family:system-ui,sans-serif;background:#F9FAFB}model-viewer{width:100vw;height:100vh}
.tag{position:fixed;left:12px;top:10px;font-size:12px;color:#B45309;letter-spacing:.06em}</style></head>
<body><div class="tag">CONCEPT, NOT FOR FABRICATION</div>
<model-viewer src="model.glb" poster="hero.png" alt="SleeveDrift: hand-mining rescue kit concept" camera-controls auto-rotate shadow-intensity="0.6"
  exposure="1.0" camera-orbit="-35deg 70deg auto" interaction-prompt="auto"></model-viewer></body></html>
""")
print({k: str(v) for k, v in outs.items()}, "model.glb", round((md / "model.glb").stat().st_size / 1e6, 2), "MB")
