#
# Implementation based off
# www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/
#

# Not used in ECC encription
# TODO: delete from project

import random

MILLER_RABIN_ROUNDS = 20

first_primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103,
        107, 109, 113, 127, 131, 137, 139,
        149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223,
        227, 229, 233, 239, 241, 251, 257,
        263, 269, 271, 277, 281, 283, 293,
        307, 311, 313, 317, 331, 337, 347, 349
        ]


def lowLevelPrime(n):

    while True:

        # random number that is n bits in length
        potentialPrime = random.randrange(2**(n-1)+1, 2**n - 1)

        # check if number is divisible by any of the first 100 primes
        for divisor in first_primes:
            if potentialPrime % divisor == 0 and divisor**2 <= potentialPrime:
                break
        else:
            # prime has not been divisible by any of the first 100 primes
            return potentialPrime


def millerRabin(candidate):
    # running rabin miller pirmality test on potential prime

    maxDivisionsByTwo = 0
    evenComponent = candidate - 1
    while evenComponent % 2 == 0:
        evenComponent >>= 1
        maxDivisionsByTwo += 1
    # assert(2**maxDivisionsByTwo * evenComponent == candidate - 1)

    def trialComposite(round_tester):
        if pow(round_tester, evenComponent, candidate) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            testPow = pow(round_tester, 2**i * evenComponent, candidate)
            if testPow == candidate - 1:
                return False
        return True

    for i in range(MILLER_RABIN_ROUNDS):
        round_tester = random.randrange(2, candidate)
        if trialComposite(round_tester):
            return False
    return True


def genPrime(bits):
    while True:
        prime_candidate = lowLevelPrime(bits)
        if not millerRabin(prime_candidate):
            continue
        else:
            return prime_candidate