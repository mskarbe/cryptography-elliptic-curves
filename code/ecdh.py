import secrets
from typing import Callable
from dataclasses import dataclass

from types import EllipticCurve, Point, KeyPair, SharedKey, KeyManager
from elapse_time import elapseTimeWithResult
from ec_multiplication import (
    toBinary,
    doubleAndAddBase,
    pointMultiplication,
    anyPointsMultiplication,
)
from curves import getCurve, ELLIPTIC_CURVES

generatePrivateKey: Callable[
    [EllipticCurve], int
] = lambda ec: secrets.randbelow(ec.field.p)

generatePublicKeyFromPrivate: Callable[
    [EllipticCurve, Point], int
] = lambda ec, priv: pointMultiplication(ec, toBinary(priv))

generateKeyPair: Callable[[EllipticCurve], KeyPair] = lambda ec: (
    lambda priv=generatePrivateKey(ec): KeyPair(
        public=pointMultiplication(ec, toBinary(priv)), private=priv
    )
)()

getCurveForKeySize: Callable[[int], EllipticCurve] = lambda size: getCurve(
    ELLIPTIC_CURVES.bp256.value
) if size == 256 else getCurve(
    ELLIPTIC_CURVES.bp512.value
) if size == 512 else None

getSharedKey: Callable[
    [EllipticCurve, int, Point, id], SharedKey
] = lambda ec, a_priv, b_pub, b_id: SharedKey(
    anyPointsMultiplication(ec, b_pub, toBinary(a_priv)), b_id
)


@dataclass
class EcdhReturn:
    a: KeyManager
    b: KeyManager


# function to generate two key pairs and calculate the shared key between them
# the shared key is calculated twice in order to verify that the results are equal.
def ecdhWithKeyGen(size: int, aId: str, bId: str) -> EcdhReturn:
    curve = getCurveForKeySize(size)
    if curve is None:
        raise ValueError("Invalid key size; pick 256 or 512.")
    keysA = generateKeyPair(curve)
    keysB = generateKeyPair(curve)

    sharedForA = SharedKey(
        anyPointsMultiplication(curve, keysB.public, toBinary(keysA.private)),
        bId,
    )
    sharedForB = SharedKey(
        anyPointsMultiplication(curve, keysA.public, toBinary(keysB.private)),
        aId,
    )

    return EcdhReturn(
        a=KeyManager(id=aId, size=size, ownKeys=keysA, shared=[sharedForA]),
        b=KeyManager(id=bId, size=size, ownKeys=keysB, shared=[sharedForB]),
    )
