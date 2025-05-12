# ECC-PY

### Project for CS166 Information security

Implementation of Elliptic Curve Cryptoraphy in python. Used for public key assymetric encription of data between two individuals.



Running `python main.py` will display the help information. The primary operations are public key generation `genpublic` and shared key generation `genshared`. There is also functionality for creating a domain file from stored curves through the `getcurve` operation. 

The demo folders contain example setups with shell scripts that walk through the process of operating our software.

Running the software with a domain of `None` will display an interactive graph of the operation being performed. Using the next and previous buttons you can step through the operations of the key generation process. There is also a hide button that is usefull when stepping through longer operations. Pressing this button will hide all of the points and lines aside from the generator point and possible input point.

### Note:
While we implement the needed math to theoretically perform key sharing with ecc, we do not perform the necessary optimizations to make realistic key sizes feasable. Our algorithm performs a brute force of using repeated addition to represent multiplication, rather than the necessary combination of point doubling and addition operations. 