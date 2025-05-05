from utility.eccMath import Domain, EllipticCurve, CurvePoint
from utility.ecc_func import eccGenPublic, eccGenShared
from utility.interactiveGraph import InteractiveContext

# ctx = GraphContext()
inter = InteractiveContext()
domain = Domain(
    15733,
    EllipticCurve(1, 3),
    CurvePoint(6,15),
    99999999999999999999999999999999,
    0
)
inter.draw(domain)


# ctx.draw(domain)
sec1 = 5
sec2 = 7

print("domain: " + str(domain))
print("private key 1: " +  str(sec1))
print("private key 2: " +  str(sec2))
pub1 = eccGenPublic(sec1, domain)

inter.draw(domain.g)


inter.draw(pub1)
# ctx.draw(domain.g)
# ctx.draw(pub1)
print("public: ", pub1)

pub2 = eccGenPublic(sec2, domain)

# ctx.draw(pub2)
inter.draw(pub2)
print("public2: ", pub2)

shared1 = eccGenShared(sec2, pub1, domain)
print("shared1: ", shared1)
# ctx.draw(shared1)
inter.draw(shared1)

shared2 = eccGenShared(sec1, pub2, domain)
print("shared2: ", shared2)
# ctx.draw(shared2)
inter.draw(shared2)

inter.start()

