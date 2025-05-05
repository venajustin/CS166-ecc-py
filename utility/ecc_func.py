from .eccMath import Domain, CurvePoint, EllipticCurve

# secp192k1 parameters
secp192k1_field = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFEE37  # standard prime for secp192k1
secp192k1_curve = EllipticCurve(a=0, b=3)
secp192k1_generator = CurvePoint(
    x=0xDB4FF10EC057E9AE26B07D0280B7F4341DA5D1B1EAE06C7D,
    y=0x9B2F2F6D9C5628A7844163D015BE86344082AA88D95E2F9D
)
secp192k1_n = 0xFFFFFFFFFFFFFFFFFFFFFFFE26F2FC170F69466A74DEFD8D
secp192k1_h = 1


# secp256k1 parameters
secp256k1_field = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
secp256k1_curve = EllipticCurve(a=0, b=7)
secp256k1_generator = CurvePoint(
    x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
)
secp256k1_n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
secp256k1_h = 1

recommendedCurves = {
    "secp192k1": Domain(
        field=secp192k1_field,
        curve=secp192k1_curve,
        generator=secp192k1_generator,
        n=secp192k1_n,
        h=secp192k1_h
    ),
    "secp256k1": Domain(
        field=secp256k1_field,
        curve=secp256k1_curve,
        generator=secp256k1_generator,
        n=secp256k1_n,
        h=secp256k1_h
    )
}

def listCurves(curve_id: str = None) -> list:
    if curve_id is None:
        return list(recommendedCurves.keys())
    else:
        if curve_id in recommendedCurves:
            domain = recommendedCurves[curve_id]
            return {
                "identifier": curve_id,
                "field": domain.p,
                "curve_a": domain.curve.a,
                "curve_b": domain.curve.b,
                "generator_x": domain.g.x,
                "generator_y": domain.g.y,
                "n": domain.n,
                "h": domain.h 
            }
        else:
            raise ValueError(f"Curve {curve_id} not found in recommended curves list")
   

def eccGenPublic(private_key: int, domain: Domain) -> CurvePoint:
    if not isinstance(private_key, int) or not isinstance(domain, Domain):
        raise TypeError("Private key must be an integer and domain must be of type Domain")
    if private_key < 1:
        raise ValueError("Private key must be a positive integer.")
    if private_key >= domain.n:
        raise ValueError("Private key must be less than the order of the base point.")

    public_key = domain.multiply(domain.g, private_key)
    if public_key is None:
        raise ValueError("Private key multiplication with the genrator point resulted in a point at infinity.")
    if not domain.verifyPoint(public_key):
        raise ValueError("The generated public key is not on the elliptic curve defined by the domain.")
    return public_key
    
def eccGenShared(private_key: int, public_key: CurvePoint, domain: Domain) -> CurvePoint:
    if not isinstance(private_key, int) or not isinstance(public_key, CurvePoint) or not isinstance(domain, Domain):
        raise TypeError("Private key must be an integer; public key must be of type CurvePoint; domain must be of type Domain.")
    if private_key < 1:
        raise ValueError("Private key must be a positive integer.")
    if private_key >= domain.n:
        raise ValueError("Private key must be less than the order of the base point.")
    if not domain.verifyPoint(public_key):
        raise ValueError("The provided public key is not on the elliptic curve defined by the domain.")


    shared_key = public_key
    while private_key > 0:
        shared_key = domain.add(shared_key, domain.g)
        private_key -= 1

    if shared_key is None:
        raise ValueError("Private key multiplication with the public key resulted in a point at infinity.")
    if not domain.verifyPoint(shared_key):
        raise ValueError("The generated shared key is not on the elliptic curve defined by the domain.")
    return shared_key
