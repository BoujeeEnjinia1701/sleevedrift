"""SleeveDrift repo-specific CAD helpers (kit 1.9 parts library extensions).

These sit beside .kit/cad_parts.py. They are candidates for a future kit release (see docs/REVIEW.md):

    bx, xcyl, ycyl, zcyl, rod         box and cylinders between limits, round bar between two points
    prism_yz, prism_xz                a polygon extruded between two stations
    place()                           put a shape built along +Z on any axis (origin, z direction)
    bead()                            straight fillet weld bead along any axis with its two legs on any two faces
    ring_weld()                       round fillet weld bead round a post or pin
    sector(), radial_bar(), at()      pieces of a rolled ring about the pipe axis (angles from the top toward +Y)

All sizes in millimetres. X runs along the rescue pipe from the portal (x = 0) to the face end (x = Lp), Y is
across the pipe, Z is up from the platform; the pipe axis is at z = zc.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[2] / ".kit")]
from build123d import (Box, Compound, Cylinder, Location, Plane, Polygon, Pos, Rot, Solid, Vector,  # noqa: E402
                       extrude)
import cad_parts as cp  # noqa: E402


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


def place(shape, origin, zdir, xdir=None):
    """Move a shape built along +Z (origin at its z = 0 end) so that its axis points along zdir from origin."""
    kw = dict(origin=tuple(origin), z_dir=tuple(zdir))
    if xdir is not None:
        kw["x_dir"] = tuple(xdir)
    return Location(Plane(**kw)) * shape


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def bead(start, axis, length, leg, d1, d2, eps=0.25):
    """Fillet weld bead from start along the unit vector axis for length, its legs along the unit vectors d1 and d2
    (the two faces it joins; axis, d1 and d2 mutually perpendicular). The corner is lifted eps off both faces so the
    bead touches without overlapping. Uses cad_parts.weld_fillet."""
    b = cp.weld_fillet(length, leg)
    s = tuple(start[i] + eps * (d1[i] + d2[i]) for i in range(3))
    for a_, b_ in ((d1, d2), (d2, d1)):
        if all(abs(x - y) < 1e-6 for x, y in zip(_cross(b_, axis), a_)):
            return Location(Plane(origin=s, x_dir=tuple(axis), z_dir=tuple(b_))) * b
    raise ValueError("bead: axis, d1 and d2 must be mutually perpendicular unit vectors")


def ring_weld(r, leg, origin, n, eps=0.2):
    """Round fillet weld bead of leg 'leg' round a post or pin of radius r standing on a plate: the cone between
    the plate face (at 'origin', normal n) and the post surface."""
    cone = Solid.make_cone(r + leg, r + eps, leg) - Solid.make_cylinder(r + eps, leg)
    return place(cone, tuple(origin[i] + eps * n[i] for i in range(3)), n)


# ----------------------------------------------------------------------------- rolled ring about the pipe axis
def at_ring(zc, r, th, x):
    """Point at radius r and angle th (deg from the top toward +Y) about an axis at height zc, station x."""
    t = math.radians(th)
    return (x, r * math.sin(t), zc + r * math.cos(t))


def e_t(th):
    t = math.radians(th)
    return Vector(0, math.cos(t), -math.sin(t))


def e_r(th):
    t = math.radians(th)
    return Vector(0, math.sin(t), math.cos(t))


def sector(zc, ro, ri, th0, th1, x0, x1):
    """Annular sector of a rolled shell between angles th0 and th1 (deg), from x0 to x1, axis at height zc."""
    tube = xcyl(0, zc, ro, x0, x1) - xcyl(0, zc, ri, x0 - 1, x1 + 1)
    R = 2.5 * ro
    n = max(2, int(abs(th1 - th0) / 20) + 1)
    pts = [(0.0, zc)] + [(R * math.sin(math.radians(th0 + (th1 - th0) * k / n)),
                          zc + R * math.cos(math.radians(th0 + (th1 - th0) * k / n))) for k in range(n + 1)]
    return tube & prism_yz(pts, x0 - 2, x1 + 2)


def radial_bar(zc, th, r0, r1, s0, s1, x0, x1):
    """Flat bar in the radial plane at angle th, from radius r0 to r1, tangential offset s0 to s1, x0 to x1."""
    t = e_t(th)
    pts = []
    for r, s in ((r0, s0), (r1, s0), (r1, s1), (r0, s1)):
        p = Vector(*at_ring(zc, r, th, 0)) + t * s
        pts.append((p.Y, p.Z))
    return prism_yz(pts, x0, x1)


def radial_rod(zc, th, r0, r1, rad, x, s=0.0):
    a = Vector(*at_ring(zc, r0, th, x)) + e_t(th) * s
    b = Vector(*at_ring(zc, r1, th, x)) + e_t(th) * s
    return rod(a, b, rad)


def tang_rod(zc, th, r, s0, s1, rad, x):
    p = Vector(*at_ring(zc, r, th, x))
    return rod(p + e_t(th) * s0, p + e_t(th) * s1, rad)


def csk_screw(d, length, head_d, head_h):
    """Countersunk machine screw along +Z: head top at z = 0 (flat), shank down to -length."""
    head = Solid.make_cone(d / 2, head_d / 2, head_h)          # narrow end at z = 0 ... flipped below
    head = Pos(0, 0, -head_h) * Solid.make_cone(d / 2, head_d / 2, head_h)
    shank = Pos(0, 0, -head_h - (length - head_h) / 2) * Cylinder(d / 2, length - head_h)
    return head + shank
