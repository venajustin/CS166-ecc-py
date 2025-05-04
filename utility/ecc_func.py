from .eccMath import Domain, CurvePoint

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
