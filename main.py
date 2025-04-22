from utility.eccMath import *


print("----------------------------------")
print("test: 1")
# Example curve
# a = -3.1, b = 6.3
curve = EllipticCurve(-3.2, 6.3)
# feild of 10000 so that mod wont mess up tests
# 0, 0 and 0 because I don't have values for those yet
domain = Domain(10000, curve, 0, 0, 0)

# example point on above curve
p = CurvePoint(-1.7, 2.61285)
p2 = CurvePoint(2.81, 4.41543)
# adding point to itsself should result in point on the curve
# very high limit was used because I havn't implemented it yet
newp = p.add(p2, domain)


print(curve)

print(p)
valid = curve.verifyPoint(p)
print("Valid: ", valid)

print(p2)
valid = curve.verifyPoint(p2)
print("Valid: ", valid)

print("point + point")
print(newp)

valid = curve.verifyPoint(newp)
print("Valid: ", valid)

