#!/usr/bin/env python3
import itertools
import random

B32_ALPHABET = "0123456789abcdefghikmnpqrstuwxyz" # removed J, L, O, V
SECRET: bytes

def __slurp_as_bytes(file):
    with open(file, encoding="utf-8") as f:
        return f.read()
SECRET = __slurp_as_bytes(__file__)
del __slurp_as_bytes

class TommyExcept(Exception):
    pass

def b32encode(input) -> str:
    global SECRET
    global B32_ALPHABET
    assert isinstance(B32_ALPHABET, str)
    assert len(B32_ALPHABET) == 32
    byte_to_bin_str = lambda byte: bin(byte)[2:].rjust(8, "0")
    bin_str_to_int = lambda bin_str: int(bin_str, 2)
    b32_alphabet = B32_ALPHABET

    ## spice it up ##
    __seed = len(SECRET)
    __tmp_list = list(b32_alphabet)
    random.Random(__seed).shuffle(__tmp_list)
    b32_alphabet = "".join(__tmp_list)

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
    base32 = "".join([*map(lambda i: b32_alphabet[i], indices)])
    return base32

def b32decode(input_str) -> bytes:
    global SECRET
    global B32_ALPHABET
    assert isinstance(B32_ALPHABET, str)
    assert len(B32_ALPHABET) == 32
    for c in input_str:
        if c not in B32_ALPHABET:
            raise TommyExcept(f"character `{c}` is not in base32 alphabet ({B32_ALPHABET})")
    quintet_to_bin_str = lambda quintet: bin(quintet)[2:].rjust(5, "0")
    b32_alphabet = B32_ALPHABET

    ## spice it up ##
    __seed = len(SECRET)
    __tmp_list = list(b32_alphabet)
    random.Random(__seed).shuffle(__tmp_list)
    b32_alphabet = "".join(__tmp_list)

    indices = [*map(lambda c: b32_alphabet.index(c), input_str)]
    quintets = [*map(lambda i: quintet_to_bin_str(i), indices)]
    bin_str = "".join(quintets)
    if len(bin_str) % 8 != 0:
        bin_str = bin_str[:-(len(bin_str) % 8)] # drop useless bits
    return bytes(int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8))

def xor(key, input, key_offset=0) -> bytes:
    if isinstance(key, str):
        key = key.encode("utf-8")
    if isinstance(input, str):
        input = input.encode("utf-8")
    consume = lambda it, n: [next(it) for i in range(n)]

    iterator_key = itertools.cycle(key)
    consume(iterator_key, key_offset)
    pairs = zip(iterator_key, input)
    return bytes(map(lambda x: x[0] ^ x[1], pairs))

def hashfn(input) -> str:
    if isinstance(input, str):
        input = input.encode("utf-8")

    def md5ify(hash):
        assert isinstance(hash, int)
        assert 0 <= hash and hash <= 255
        str_hash = hex(43210 + int(hash * (22222 / 255)))[2:]
        return str_hash

    T = [i for i in range(256)]

    ## spice it up ##
    __seed = len(SECRET)
    random.Random(__seed).shuffle(T)

    hash = 0
    for b in input:
        hash = T[hash ^ b]
    return md5ify(hash)

def tommycrypt(input_str) -> str:
    def encrypt(input_str) -> str:
        global SECRET
        if len(input_str) == 0:
            return ""
        xored = xor(SECRET, input_str, key_offset=int(len(SECRET) / 2))
        return hashfn(input_str) + b32encode(xored)

    def decrypt(input_str) -> str:
        global SECRET
        if len(input_str) == 0:
            return ""
        if len(input_str) < 6:
            raise TommyExcept("invalid input")
        hash = input_str[0:4]
        decoded_payload = b32decode(input_str[4:])
        decrypted = xor(SECRET, decoded_payload, key_offset=int(len(SECRET) / 2))
        if hashfn(decrypted) != hash:
            raise TommyExcept("invalid input")
        return decrypted.decode("utf-8") # at this point WE know its utf8

    try:
        return decrypt(input_str)
    except TommyExcept:
        return encrypt(input_str)

if __name__ == "__main__":
    import sys
    # toggle multiline mode with arg `-m`
    stdin = lambda: sys.stdin.read() if len(sys.argv) > 1 else sys.stdin.readline()
    input_str = stdin()
    while input_str:
        if input_str[-1] == '\n':
            input_str = input_str[:-1] # remove trailing newline
        res = tommycrypt(input_str)
        print(res, flush=True)
        input_str = stdin()
