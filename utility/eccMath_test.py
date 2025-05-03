import unittest
from eccMath import CurvePoint, EllipticCurve, Domain

class TestEllipticCurve(unittest.TestCase):
    def setUp(self):
        # values obtained from the video
        self.p = 17
        self.curve = EllipticCurve(a=2, b=2)
        self.gen_point = CurvePoint(5, 1)
        self.domain = Domain(field=self.p, curve=self.curve, generator=self.gen_point, n=19, h=1)

    def test_verify_valid_point(self):
        # (5,1) is a valid point.
        self.assertTrue(self.curve.verifyPoint(self.gen_point, self.domain))
    
    def test_verify_invalid_point(self):
        # (4,1) is not on the curve because it does not satisfy the curve equation.
        invalid_point = CurvePoint(4, 1)
        self.assertFalse(self.curve.verifyPoint(invalid_point, self.domain))

class TestCurvePointOperations(unittest.TestCase):
    def setUp(self):
        # values obtained from the video
        self.p = 17
        self.curve = EllipticCurve(a=2, b=2)
        self.P = CurvePoint(5, 1)
        self.domain = Domain(field=self.p, curve=self.curve, generator=self.P, n=19, h=1)

    def test_double(self):
        # values obtained from the video
        doubleP = self.P.double(self.domain)
        self.assertIsNotNone(doubleP)
        self.assertEqual(doubleP.x, 6)
        self.assertEqual(doubleP.y, 3)

    def test_add(self):
        # Let P=(5,1) and Q=2P=(6,3) from our test_double.
        Q = self.P.double(self.domain)
        R = self.P.add(Q, self.domain)
        self.assertIsNotNone(R)
        self.assertEqual(R.x, 10)
        self.assertEqual(R.y, 6)

    def test_multiply(self):
        # 2 * P should equal P.double()
        twoP = self.P.multiply(2, self.domain)
        two_add_result = self.P.double(self.domain)
        self.assertIsNotNone(twoP)
        self.assertEqual(twoP.x, two_add_result.x)
        self.assertEqual(twoP.y, two_add_result.y)
        # 3 * P should equal P + 2P
        threeP = self.P.multiply(3, self.domain)
        three_add_result = self.P.add(two_add_result, self.domain)
        self.assertIsNotNone(threeP)
        self.assertEqual(threeP.x, three_add_result.x)
        self.assertEqual(threeP.y, three_add_result.y)

    def test_slopeTo(self):
        # P=(5,1) and Q=double(P)=(6,3); slope should be computed as:
        # slope = ((1-3)/(5-6)) mod17 = ((-2)/(-1)) mod17 = 2 mod17.
        Q = self.P.double(self.domain)
        slope = self.P.slopeTo(Q, self.domain)
        self.assertIsNotNone(slope)
        self.assertEqual(slope, 2)

if __name__ == '__main__':
    unittest.main()