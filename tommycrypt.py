#!/usr/bin/env python3
import itertools

B32_ALPHABET = "0123456789abcdefghikmnpqrstuwxyz" # removed J, L, O, V

class TommyExcept(Exception):
    pass

def b32encode(input) -> str:
    global B32_ALPHABET
    assert isinstance(B32_ALPHABET, str)
    assert len(B32_ALPHABET) == 32
    byte_to_bin_str = lambda byte: bin(byte)[2:].rjust(8, "0")
    bin_str_to_int = lambda bin_str: int(bin_str, 2)

    if len(input) == 0:
        return ""
    if isinstance(input, str):
        input = input.encode("utf-8")
    bin_str = ""
    for b in input:
        bin_str += byte_to_bin_str(b)
    quintets = [bin_str[i:i+5] for i in range(0, len(bin_str), 5)]
    quintets[-1] = quintets[-1].ljust(5, "0") # potential padding
    indices = [*map(bin_str_to_int, quintets)]
    base32 = "".join([*map(lambda i: B32_ALPHABET[i], indices)])
    return base32

def b32decode(input_str) -> bytes:
    global B32_ALPHABET
    assert isinstance(B32_ALPHABET, str)
    assert len(B32_ALPHABET) == 32
    for c in input_str:
        if c not in B32_ALPHABET:
            raise TommyExcept(f"character `{c}` is not in base32 alphabet ({B32_ALPHABET})")
    quintet_to_bin_str = lambda quintet: bin(quintet)[2:].rjust(5, "0")

    indices = [*map(lambda c: B32_ALPHABET.index(c), input_str)]
    quintets = [*map(lambda i: quintet_to_bin_str(i), indices)]
    bin_str = "".join(quintets)
    if len(bin_str) % 8 != 0:
        bin_str = bin_str[:-(len(bin_str) % 8)] # drop useless bits
    return bytes(int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8))

def xor(secret, input) -> bytes:
    if isinstance(secret, str):
        secret = secret.encode("utf-8")
    if isinstance(input, str):
        input = input.encode("utf-8")

    iterator_secret = itertools.cycle(secret)
    pairs = zip(iterator_secret, input)
    return bytes(map(lambda x: x[0] ^ x[1], pairs))

def hashfn(input) -> str:
    if isinstance(input, str):
        input = input.encode("utf-8")

    def md5ify(hash):
        assert isinstance(hash, int)
        assert 0 <= hash and hash <= 255
        str_hash = hex(43210 + int(hash * (22222 / 255)))[2:]
        return str_hash

    T = [i for i in range(0, 256)]
    hash = 0
    for b in input:
        hash = T[hash ^ b]
    return md5ify(hash)

def tommycrypt(input_str) -> str:
    def slurp_as_bytes(file):
        with open(file, encoding="utf-8") as f:
            return f.read()
    secret = slurp_as_bytes(__file__)

    def encrypt(input_str) -> str:
        nonlocal secret
        if len(input_str) == 0:
            return ""
        return hashfn(input_str) + b32encode(xor(secret, input_str))

    def decrypt(input_str) -> str:
        nonlocal secret
        if len(input_str) == 0:
            return ""
        if len(input_str) < 6:
            raise TommyExcept("invalid input")
        hash = input_str[0:4]
        decoded_payload = b32decode(input_str[4:])
        decrypted = xor(secret, decoded_payload)
        if hashfn(decrypted) != hash:
            raise TommyExcept("invalid input")
        return decrypted.decode("utf-8") # at this point WE know its utf8

    try:
        return decrypt(input_str)
    except TommyExcept:
        return encrypt(input_str)

if __name__ == "__main__":
    import sys
    input_str = sys.stdin.read()
    res = tommycrypt(input_str[:-1]) # remove trailing newline
    print(res)
