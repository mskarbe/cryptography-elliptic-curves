import unittest

from curves import getCurve, ELLIPTIC_CURVES
from ecdh import generatePublicKeyFromPrivate, getSharedKey
from brainpool_test_vectors import bp256_testVector, bp512_testVector


class TestEcdh(unittest.TestCase):
    def testPublicKeys(self):
        bp256 = getCurve(ELLIPTIC_CURVES.bp256.value)
        bp512 = getCurve(ELLIPTIC_CURVES.bp512.value)

        keyA_256 = generatePublicKeyFromPrivate(
            bp256, bp256_testVector.a.private
        )
        keyA_512 = generatePublicKeyFromPrivate(
            bp512, bp512_testVector.a.private
        )

        keyB_256 = generatePublicKeyFromPrivate(
            bp256, bp256_testVector.b.private
        )
        keyB_512 = generatePublicKeyFromPrivate(
            bp512, bp512_testVector.b.private
        )

        self.assertEqual(keyA_256, bp256_testVector.a.public)
        self.assertEqual(keyA_512, bp512_testVector.a.public)
        self.assertEqual(keyB_256, bp256_testVector.b.public)
        self.assertEqual(keyB_512, bp512_testVector.b.public)

    def testSharedKey(self):
        bp256 = getCurve(ELLIPTIC_CURVES.bp256.value)
        bp512 = getCurve(ELLIPTIC_CURVES.bp512.value)
        sharedKey256 = getSharedKey(
            bp256,
            bp256_testVector.a.private,
            bp256_testVector.b.public,
            "test-vector",
        )
        sharedKey512 = getSharedKey(
            bp512,
            bp512_testVector.a.private,
            bp512_testVector.b.public,
            "test-vector",
        )
        self.assertEqual(sharedKey256.key, bp256_testVector.sh.key)
        self.assertEqual(sharedKey512.key, bp512_testVector.sh.key)


unittest.main(argv=[""], verbosity=5, exit=False)
