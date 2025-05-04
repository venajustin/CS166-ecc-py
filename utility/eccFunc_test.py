import unittest
from eccFunc import listCurves, eccGenPublic, eccGenShared, recommendedCurves
from eccMath import CurvePoint

class TestEccFunctions(unittest.TestCase):

    def test_listCurves_no_argument(self):
        # When no argument is passed, listCurves should return a list of available curve identifiers.
        curves = listCurves()
        # Expecting both secp192k1 and secp256k1 to be available.
        self.assertIn("secp192k1", curves)
        self.assertIn("secp256k1", curves)
        self.assertIsInstance(curves, list)

    def test_listCurves_with_argument(self):
        # When a valid curve identifier is passed, listCurves should return a dictionary of parameters.
        secp256k1_info = listCurves("secp256k1")
        expected_keys = {"identifier", "field", "curve_a", "curve_b", "generator_x", "generator_y", "n", "h"}
        self.assertEqual(set(secp256k1_info.keys()), expected_keys)
        self.assertEqual(secp256k1_info["identifier"], "secp256k1")
    
    def test_eccGenPublic(self):
        # Use secp256k1 as test domain.
        domain = recommendedCurves["secp256k1"]
        # Choose a relatively small private key for testing.
        private_key = 5
        public_key = eccGenPublic(private_key, domain)
        self.assertIsInstance(public_key, CurvePoint)
        # Verify that the generated public key lies on the curve.
        self.assertTrue(domain.curve.verifyPoint(public_key, domain))
    
    def test_eccGenShared(self):
        # Use secp256k1 as test domain.
        domain = recommendedCurves["secp256k1"]
        # Private keys for two parties.
        private_key_A = 5
        private_key_B = 7
        
        # Each party computes their public key.
        public_key_A = eccGenPublic(private_key_A, domain)
        public_key_B = eccGenPublic(private_key_B, domain)
        
        # Now compute shared secrets.
        shared_A = eccGenShared(private_key_A, public_key_B, domain)
        shared_B = eccGenShared(private_key_B, public_key_A, domain)
        
        # The shared keys computed using Diffie-Hellman must be equal.
        self.assertIsNotNone(shared_A)
        self.assertIsNotNone(shared_B)
        self.assertEqual(shared_A.x, shared_B.x)
        self.assertEqual(shared_A.y, shared_B.y)

if __name__ == '__main__':
    unittest.main()