from typing import Callable, List
from dataclasses import dataclass

from types import EllipticCurve

# common divisor functions -> for natural positive numbers
# returns list of divisors of number n
divs: Callable[[int], List[int]] = lambda n: [
    i for i in range(1, n + 1) if n % i == 0
]

# interface: GCD and Bezout coefficients (x, y), so ax+bx=gcd(a, b)
@dataclass
class GcdProps:
    gcd: int  # prime modulus
    x: int  # order of the base point
    y: int = 1


egcdStep: Callable[[int, int, GcdProps], GcdProps] = lambda a, b, g: GcdProps(
    g.gcd, g.y - (b // a) * g.x, g.x
)

# extended GCD euclidean algorithm
egcd: Callable[[int, int], GcdProps] = lambda a, b: GcdProps(
    b, 0, 1
) if a == 0 else egcdStep(a, b, egcd(b % a, a))

# modular multiplicative inverse integer (a/b vs b/a); it is necessary to compute the slope f.ex.
# gcd(a, prime) = x*a + y*prime -> x is the inverse
multInvert: Callable[
    [EllipticCurve, int], int
] = lambda ec, i: 0 if i == 0 else (
    ec.field.p - multInvert(ec, -i)
) if i < 0 else (
    lambda g=egcd(i, ec.field.p): None if g.gcd != 1 else g.x % ec.field.p
)()
