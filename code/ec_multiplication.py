from typing import Callable
from dataclasses import dataclass

from types import EllipticCurve, Point
from ec_arithmetic import pointAddition, pointDouble

# normal multiplication n*P
def pointMultiplySlow(ec: EllipticCurve, p: Point, n: int):
    sum: Point = p
    for _ in range(1, n):
        sum = pointAddition(ec, sum, p)
    return sum


toBinary: Callable[[int], str] = lambda i: bin(i)[2:]

# standard double and add algorithm
def doubleAndAdd(ec: EllipticCurve, p: Point, bits: str) -> Point:
    sum = ec.inf  # starting point: neutral element
    # from MSB to LSB
    for bit in bits:
        sum = pointDouble(ec, sum)  # double
        if bit == "1":
            sum = pointAddition(ec, sum, p)  # add
    return sum


# standard double and add
# doubleAndAdd: Callable[[EllipticCurve, Point, int], Point] = lambda ec, p, n: \
#    (lambda sum=ec.inf, bits=toBinary(n): [(lambda bit=bit, partSum=pointDouble(ec, sum): \
#        pointAddition(ec1, partSum, p) if bit == '1' else partSum )() for bit in bits])()


# Montgomery ladder double and add algorithm
def montgomeryDoubleAndAdd(ec: EllipticCurve, p: Point, bits: str) -> Point:
    r0 = ec.inf  # sum register
    r1 = p  # intermediate register
    # from MSB to LSB
    for bit in bits:
        if bit == "1":
            r0 = pointAddition(ec, r0, r1)
            r1 = pointDouble(ec, r1)
        else:
            r1 = pointAddition(ec, r0, r1)
            r0 = pointDouble(ec, r0)
    return r0


# short hand notation for base point of the curve

# slow multiply
slowMultiplyBase: Callable[
    [EllipticCurve, int], Point
] = lambda ec, n: pointMultiplySlow(ec, ec.base, n)

# double and add
doubleAndAddBase: Callable[
    [EllipticCurve, str], Point
] = lambda ec, bits: doubleAndAdd(ec, ec.base, bits)

# montgomery ladder is the default algorithm for multiplication
pointMultiplication: Callable[
    [EllipticCurve, str], Point
] = lambda ec, bits: montgomeryDoubleAndAdd(ec, ec.base, bits)

# montgomery ladder is the default algorithm for multiplication
anyPointsMultiplication: Callable[
    [EllipticCurve, Point, str], Point
] = lambda ec, p, bits: montgomeryDoubleAndAdd(ec, p, bits)

# point multiplication (montgomery ladder) with conversion to binary included
pointMultiplyWithInt: Callable[
    [EllipticCurve, int], Point
] = lambda ec, n: montgomeryDoubleAndAdd(ec, ec.base, toBinary(n))
