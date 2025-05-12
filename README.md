# ECC-PY

### Project for CS166 Information security

Implementation of Elliptic Curve Cryptoraphy in python. Used for distribution of a shared key between two parties.



Running `python main.py` will display the help information. The primary operations are public key generation `genpublic` and shared key generation `genshared`. There is also functionality for creating a domain file from stored curves through the `getcurve` operation. 

### Usage

Basic command syntax
```bash
python main.py <operation> [params...]
```

The curve domain, private and public keys are all stored within text files. The locations of these files are passed into the program along with the location to store program output.

Generating a public key from a private key
```
python main.py genpublic <domain_file> <private_key_file> <output_file>
```

Generating a shared key from a private key and public key
```
python main.py genshared <domain_file> <private_key_file> <public_key_file> <output_file>
```

Outputing a predefined curve domain
```
python main.py getcurve <curve_name> <output_file>
```
The curves available are:
- secp192k1
- secp256k1

The demo folders contain example setups with shell scripts that walk through the process of operating our software.

Running the software with a domain field of `None` will display an interactive graph of the operation being performed. Using the next and previous buttons you can step through the operations of the key generation process. There is also a hide button that is usefull when stepping through longer operations. Pressing this button will hide all of the points and lines aside from the generator point and possible input point.

### Note:
While we implement the needed math to theoretically perform key sharing with ecc, we do not perform the necessary optimizations to make realistic key sizes feasable. Our algorithm performs a brute force of using repeated addition to represent multiplication, rather than the necessary combination of point doubling and addition operations. 