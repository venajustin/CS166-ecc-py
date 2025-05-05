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
from utility.eccMath import *
from utility.ecc_func import *

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
    
def read_public_key_file(filename):
    try:
        with open(filename, 'r') as f:


            content = f.read().strip()

            if content.startswith('(') and content.endswith(')'):
                content = content[1:-1]  # Remove parentheses    

            parts = content.split(',')

            if len(parts) != 2:
                raise ValueError(f"Expected two comma-separated values in '{filename}', but found {len(parts)}.")
            x = int(parts[0].strip())
            y = int(parts[1].strip())
            return x, y
    except FileNotFoundError:
        print(f"Error: File not found - {filename}")
        return None
    except ValueError as ve:
        print(f"Error: Invalid format in file '{filename}': {ve}")
        return None
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None

def create_domain_object(data):
    try:
        field_str = data.get('Field', None)
        field = None if field_str.lower() == 'none' else int(field_str)
        a = int(data.get('a', None))
        b = int(data.get('b', None))
        generator_str = data.get('Generator', None)
        order = int(data.get('Order', None))
        cofactor = int(data.get('Cofactor', None))

        if field_str is None or a is None or b is None or generator_str is None or order is None or cofactor is None:
            print("Error: Missing required parameters in domain file.")
            return None

        if generator_str.startswith('(') and generator_str.endswith(')'):
            generator_str = generator_str[1:-1]
            x_str, y_str = generator_str.split(',')
            generator_x = int(x_str.strip())
            generator_y = int(y_str.strip())
            generator = CurvePoint(generator_x, generator_y)
        else:
            print("Error: Invalid format for Generator.  Expected '(x, y)'.")
            return None
        
        curve = EllipticCurve(a, b)
        domain = Domain(field, curve, generator, order, cofactor)
        return domain

    except ValueError:
        print("Error: Invalid integer format in domain file.")
        return None
    except Exception as e:
        print(f"Error creating domain object: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read domain parameters from a file, create a Domain object, obtain a private key, and write the public key to a file.",
                                     formatter_class=argparse.RawTextHelpFormatter  # For multi-line help
    )
    
    subparsers = parser.add_subparsers(dest='mode', required=True,
                                     help='Mode of operation:\n'
                                          '  genpublic: Generate public key from private key and domain file.\n'
                                          '  genshared: Generate shared secret from private key, domain file, and public key file.\n'
                                          '  getcurve: List recommended curves or export a specific curve parameters\n')
    
    # Subparser for genpublic mode
    genpublic_parser = subparsers.add_parser('genpublic', help='Generate public key.')
    genpublic_parser.add_argument("domain_file", help="Path to the domain parameter file.")
    genpublic_parser.add_argument("private_key_file", help="Path to the private key file (containing an integer).")
    genpublic_parser.add_argument("output_file", help="Path to output file.")

    # Subparser for genshared mode
    genshared_parser = subparsers.add_parser('genshared', help='Generate shared secret.')
    genshared_parser.add_argument("domain_file", help="Path to the domain parameter file.")
    genshared_parser.add_argument("private_key_file", help="Path to the private key file.")
    genshared_parser.add_argument("public_key_file", help="Path to the public key file (containing x,y coordinates).")
    genshared_parser.add_argument("output_file", help="Path to output file.")
    
    # Subparser for getcurve mode
    getcurve_parser = subparsers.add_parser('getcurve', help='List or export recommended curves.')
    # optional curve identifier and output file; when neither provided, list all curves
    getcurve_parser.add_argument("curve_id", nargs="?", help="Optional: Identifier of the curve, e.g., secp256k1")
    getcurve_parser.add_argument("output_file", nargs="?", help="Optional: Output to a  file to export the curve parameters")


    args = parser.parse_args()

    if args.mode == 'genpublic' or args.mode == 'genshared':

        domain_data = read_domain_file(args.domain_file)
        private_key = read_private_key_file(args.private_key_file)
        domain_object = create_domain_object(domain_data)

        if not domain_data:
            print("Failed to read domain file.")
        elif not domain_object:
            print("Failed to create domain object.")
        elif private_key is None:
            print("Failed to read private key file.")
        else:
            print("Domain objected created successfully")
            print("Domain Object Attributes:")
            print(f"  Field: {domain_object.p}")
            print(f"  Curve: EllipticCurve(a={domain_object.curve.a},b={domain_object.curve.b})")
            print(f"  Generator: ({domain_object.g.x},{domain_object.g.y})")
            print(f"  Order: {domain_object.n}")
            print(f"  Cofactor: {domain_object.h}")
            print(f"Extracted Private Key: {private_key}")

        if args.mode == 'genpublic':
                public_key = eccGenPublic(private_key, domain_object)
                print(f"Public Key: ({public_key.x}, {public_key.y})")
                try:
                    with open(args.output_file, 'w') as outfile:
                        outfile.write(f"({int(public_key.x)},{int(public_key.y)})")
                        print(f"Public key written to {args.output_file}")
                except Exception as e:
                    print(f"Error writing to output file: {e}")

        elif args.mode == 'genshared':
            public_key_x, public_key_y = read_public_key_file(args.public_key_file) # Added function
            if public_key_x is not None and public_key_y is not None: 
                other_public_key = CurvePoint(public_key_x, public_key_y)
                shared_secret_key = eccGenShared(private_key, other_public_key, domain_object)
                print(f"Shared Secret Key: ({shared_secret_key.x},{shared_secret_key.y})")
                try:
                    with open(args.output_file, 'w') as outfile:
                        outfile.write(f"PrivateSharedKey: ({shared_secret_key.x},{shared_secret_key.y})")
                        print(f"Shared Secret Key written to {args.output_file}")
                except Exception as e:
                    print(f"Error writing to output file: {e}")

    elif args.mode == 'getcurve':
         # no parameters provided --> list all curves
        if args.curve_id is None and args.output_file is None:
            # check if recommendedCurves exist
            recommendedCurves = listCurves()
            if recommendedCurves is None:
                print("Error: No recommended curves found.")
                exit(1)
            curves = list(recommendedCurves.keys())
            print("Available recommended curves:")
            for curve in curves:
                print(f"  {curve}")

        # only curve_id provided --> not valid command interface format
        elif args.curve_id is not None and args.output_file is None:
            print("Error: When specifying a curve identifier, you must also provide an output file")

        # both curve_id and output_file provided -> export curve parameters to output_file
        elif args.curve_id is not None and args.output_file is not None:
                try:
                    # check if the supplied curve_id is listed in recommendedCurves
                    if args.curve_id not in recommendedCurves:
                        print(f"Error: Curve '{args.curve_id}' is not supported. Available curves are: {', '.join(recommendedCurves.keys())}")
                        exit(1)
                    # extract curve details from recommendedCurves
                    details = listCurves(args.curve_id)
                    # check if the curve_id is valid
                    if details is None:
                        print(f"Error: Curve '{args.curve_id}' not found.")
                        exit(1)
                    # format the extracted urve parameters to the output file
                    with open(args.output_file, 'w') as outfile:
                        outfile.write(f"Field:{details['field']}\n")
                        outfile.write(f"a:{details['curve_a']}\n")
                        outfile.write(f"b:{details['curve_b']}\n")
                        outfile.write(f"Generator:({details['generator_x']},{details['generator_y']})\n")
                        outfile.write(f"Order:{details['n']}\n")
                        outfile.write(f"Cofactor:{details['h']}\n")
                    print(f"Curve parameters for '{args.curve_id}' written to {args.output_file}")
                except Exception as e:
                    print(f"Error: {e}")
    else:
        print("Failed to read data from one or both files.")
