import numpy as np
from eccMath import Domain, EllipticCurve, CurvePoint

a,b = 2, 2

domain = Domain(
    None,
    EllipticCurve(2, 2),
    None, None, None
)

points = []

for i in range(100000000000000):
    # ecc y in terms of x
    y = np.sqrt(i**3 + domain.curve.a * i + domain.curve.b)
    if y % 1 == 0 and domain.verifyPoint(CurvePoint(i, y)):
        print(f"Point: ({i},{y})")
        exit()



