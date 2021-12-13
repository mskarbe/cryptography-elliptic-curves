from typing import Callable

from types import EllipticCurve, Point
from egcd import multInvert

# check if point is on curve [in the field Fp]
# y^2 % p = (x^3 + Ax + B) % p
isOnCurve: Callable[[EllipticCurve, Point], bool] = lambda ec, p: (
    p.y ** 2 - p.x ** 3 - ec.a * p.x - ec.b
) % ec.field.p == 0

# point of infinnity check
isZero: Callable[[EllipticCurve, Point], bool] = lambda ec, p: (
    p.y == ec.inf.y and p.x == ec.inf.x
)

# invert the point (y axis)
invert: Callable[[EllipticCurve, Point], Point] = lambda ec, p: p if isZero(
    ec, p
) else Point(p.x, (-p.y) % ec.field.p)

# check if two points are inverse
areInverse: Callable[[EllipticCurve, Point, Point], bool] = lambda ec, p1, p2: (
    p1 == invert(ec, p2)
)

# slope of the line crossing p1, p2 and inverse of result
# calculates appropriate formula w.r.t if points are on same coordinates
slope: Callable[[EllipticCurve, Point, Point], int] = lambda ec, p1, p2: (
    (p2.y - p1.y) * multInvert(ec, (p2.x - p1.x))
) % ec.field.p if (p1 != p2) else ec.inf if p1.y == 0 else (
    (3 * p1.x ** 2 + ec.a) * multInvert(ec, 2 * p1.y)
) % ec.field.p

sumPoints: Callable[[EllipticCurve, Point, Point], Point] = lambda ec, p1, p2: (
    lambda s=slope(ec, p1, p2): (
        lambda xr=((s ** 2 - p1.x - p2.x) % ec.field.p): Point(
            xr, (s * (p1.x - xr) - p1.y) % ec.field.p
        )
    )()
)()

pointAddition: Callable[
    [EllipticCurve, Point, Point], Point
] = lambda ec, p1, p2: p1 if isZero(ec, p2) else p2 if isZero(
    ec, p1
) else ec.inf if areInverse(
    ec, p1, p2
) else sumPoints(
    ec, p1, p2
)

# point doubling
pointDouble: Callable[
    [EllipticCurve, Point], Point
] = lambda ec, p1: pointAddition(ec, p1, p1)
