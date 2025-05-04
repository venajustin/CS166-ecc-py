from eccMath import Domain, CurvePoint

def eccGenPublic(private_key: int, domain: Domain) -> CurvePoint:
    if not isinstance(private_key, int) or not isinstance(domain, Domain):
        raise TypeError("Private key must be an integer and domain must be of type Domain")
    if private_key < 1:
        raise ValueError("Private key must be a positive integer.")
    if private_key >= domain.n:
        raise ValueError("Private key must be less than the order of the base point.")
    if not domain.curve.verifyPoint(public_key, domain):
        raise ValueError("The generated public key is not on the elliptic curve defined by the domain.")
    

    public_key = domain.generator.multiply(private_key, domain)
    if public_key is None:
        raise ValueError("Private key multiplication with the genrator point resulted in a point at infinity.")
    return public_key
    
def eccGenShared(private_key: int, public_key: CurvePoint, domain: Domain) -> CurvePoint:
    if not isinstance(private_key, int) or not isinstance(public_key, CurvePoint) or not isinstance(domain, Domain):
        raise TypeError("Private key must be an integer; public key must be of type CurvePoint; domain must be of type Domain.")
    if private_key < 1:
        raise ValueError("Private key must be a positive integer.")
    if private_key >= domain.n:
        raise ValueError("Private key must be less than the order of the base point.")
    if not domain.curve.verifyPoint(public_key, domain):
        raise ValueError("The provided public key is not on the elliptic curve defined by the domain.")
    
    shared_key = public_key.multiply(private_key, domain)
    if shared_key is None:
        raise ValueError("Private key multiplication with the public key resulted in a point at infinity.")
    return shared_key
