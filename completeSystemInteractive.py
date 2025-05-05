from utility.eccMath import Domain, EllipticCurve, CurvePoint
from utility.ecc_func import eccGenPublic, eccGenShared
from utility.interactiveGraph import InteractiveContext

# ctx = GraphContext()
inter = InteractiveContext()
domain = Domain(
    None,
    EllipticCurve(0, 1),
    CurvePoint(2, 3),
    6,
    1
)
inter.draw(domain)


# ctx.draw(domain)
sec1 = 2
sec2 = 1
print("domain: " + str(domain))
print("secret1: " +  str(sec1))
print("secret2: " +  str(sec2))
pub1 = eccGenPublic(sec1, domain)


inter.draw(domain.g)

inter.draw_add(domain.g, domain.g, domain)

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
inter.draw_add(pub1, domain.g, domain)
inter.draw(shared1)

shared2 = eccGenShared(sec1, pub2, domain)
print("shared2: ", shared2)
inter.draw_add(inter.draw(inter.draw_add(pub2, domain.g, domain)), domain.g, domain)
# ctx.draw(shared2)
inter.draw(shared2)

inter.start()

