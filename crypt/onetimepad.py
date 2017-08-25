from random import choice
import string


def convert_to_bits(s):
    """Converts string s to a string containing only 0s or 1s,
    representing the original string."""
    return "".join(format(ord(x), 'b') for x in s)


def gen_random_key(n):
    """Generates a random key of bits (with 0s or 1s) of length n"""
    k = []
    for i in range(n):
        k.append(choice(["0", "1"]))
    return "".join(k)


def xor(m, k):
    """Given strings m and k of characters 0 or 1,
    it returns the string representing the XOR
    between each character in the same position.
    This means that m and k should be of the same length.

    Use this function both for encrypting and decrypting!"""
    r = []
    for i, j in zip(m, k):
        r.append(str(int(i) ^ int(j)))  # xor between bits i and j
    return "".join(r)


if __name__ == "__main__":
    ls = []

    for i in range(100):
        for i in range(100):
            ls.append(choice(string.ascii_letters))

        s = "".join(ls)

        bits = convert_to_bits(s)
        key = gen_random_key(len(bits))
        cipher = xor(bits, key)
        original = xor(key, cipher)

        if original != bits:
            raise Exception("Something wrong with the implementation...")
