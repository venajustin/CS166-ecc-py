# ...main.py genpublic <domain_file> <private_key_file> <output_file>
# and
# ...main.py genshared <domain_file> <private_key_file> <other_key_file> <output_file> 
# 23847293847293  would be a key
# -> parse the command entered and put the values into a domain class  and a privat ekey variable
# -> call eccGenPublic( domain, private key)
# or
# -> parse the command entered and put the values into domain object, private key, and public key CurvePoint object
# -> call eccGenShared(domain, private, public)

# eccGenPublic(Domain, private (int) ) -> returns CurvePoiint
# eccGenShared(domain, private (int), public(CurvePoint)) -> returns CurvePoint
# assume that we have this interface above


import argparse
from eccMath import CurvePoint, Domain, EllipticCurve
from ecc_func import *

def read_domain_file(filename):
    domain_data = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    key, value = line.split(':', 1)
                    domain_data[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Error: File not found - {filename}")
        return None
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None
    return domain_data

def read_private_key_file(filename):
    try:
        with open(filename, 'r') as g:
            content = g.read().strip()
            return int(content)
    except FileNotFoundError:
        print(f"Error: File not found - {filename}")
        return None
    except ValueError:
        print(f"Error: Invalid integer format in file '{filename}'")
        return None
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None

def create_domain_object(data):
    try:
        field_str = data.get('Field', None)
        field = 99999999999999 if field_str.lower() == 'none' else int(field_str)
        a = int(data.get('a', None))
        b = int(data.get('b', None))
        generator_x = int(data.get('Generatorx', None))
        generator_y = int(data.get('Generatory', None))
        order = int(data.get('Order', None))
        cofactor = int(data.get('Cofactor', None))

        if field_str is None or a is None or b is None or generator_x is None or generator_y is None or order is None or cofactor is None:
            print("Error: Missing required parameters in domain file.")
            return None

        curve = EllipticCurve(a, b)
        generator = CurvePoint(generator_x, generator_y)
        domain = Domain(field_str, curve, generator, order, cofactor)
        return domain

    except ValueError:
        print("Error: Invalid integer format in domain file.")
        return None
    except Exception as e:
        print(f"Error creating domain object: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read domain parameters from a file and create a Domain object and obtain a private key.",)
    parser.add_argument("domain_file", help="Path to the domain parameter file.")
    parser.add_argument("second_file", help = "Path to the private key parameter file.")
    args = parser.parse_args()

    domain_data = read_domain_file(args.domain_file)
    private_key = read_private_key_file(args.second_file)

    if domain_data and private_key is not None:
        domain_object = create_domain_object(domain_data)
        if domain_object:
            print("Domain objected created successfully")
            print(f"Integer from second file: {private_key}")


        # Program logic goes here

        public_key = eccGenPublic(private_key, domain_object)

    else:
        print("Failed to read data from one or both files.")
