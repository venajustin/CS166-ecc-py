from utility.eccMath import *
from utility.graphing import GraphContext

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

print()
print("----------------------------------")
print("test: 2")
print("doubling point")

p1 = CurvePoint(-1.7, 2.61285)
print(p1)
doubled = p1.double(domain)
print(doubled)
print("verify: ", curve.verifyPoint(doubled))
print()

print("multiply by 1")
result = p1.multiply(1, domain)
print(result)
print("verify: ", curve.verifyPoint(result))

print("multiply by 2")
result = p1.multiply(2, domain)
print(result)
print("verify: ", curve.verifyPoint(result))

print("multiply by 3")
result = p1.multiply(3, domain)
print(result)
print("verify: ", curve.verifyPoint(result))
print("multiply by 4")
result = p1.multiply(4, domain)
print(result)
print("verify: ", curve.verifyPoint(result))

print("multiply by 5")
x5 = p1.multiply(5, domain)
print(x5)
print("verify: ", curve.verifyPoint(x5))


print()
print("----------------------------------")

#
# Previous tests invalid. ECC math occurs on finite curve with integers numbers. We must test with inputs that are
# integer coordinates falling within the curve. The following example curve has only 6 points within it's field
#
# y^2 = x^3 + 1
# generator  = ( 2, 3 )
# order = 6
# cofactor = 6 / 6 = 1
#
domain = Domain(
    10, # field (don't knwo what to set this to yet)
    EllipticCurve(0, 1),
    CurvePoint(2, 3),
    6,
    1
)

ctx = GraphContext()
domain.draw(ctx)

print(domain.g)
domain.g.draw(ctx)
a = domain.g
for i in range(6):
    print(a)
    a = a.add(domain.g, domain)
    a.draw(ctx)

ctx.flush()



