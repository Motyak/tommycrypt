#!/usr/bin/env python3
import itertools
import random
import gzip

B32_ALPHABET = "0123456789abcdefghikmnpqrstuwxyz" # removed J, L, O, V
#B32_ALPHABET = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" # ascii symbols only
SECRET: bytes

def __slurp_as_bytes(file):
    with open(file, "rb") as f:
        return f.read()
SECRET = __slurp_as_bytes(__file__)
#SECRET = b"secret"
del __slurp_as_bytes

class TommyExcept(Exception):
    pass

def b32encode(input) -> str:
    global SECRET
    global B32_ALPHABET
    assert isinstance(B32_ALPHABET, str)
    assert len(B32_ALPHABET) == 32
    assert len(set(B32_ALPHABET)) == 32
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
    assert len(set(B32_ALPHABET)) == 32
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
    consume = lambda it, n: [next(it) for i in range(n)]

    iterator_key = itertools.cycle(key)
    consume(iterator_key, key_offset)
    pairs = zip(iterator_key, input)
    return bytes(map(lambda x: x[0] ^ x[1], pairs))

def hashfn(input) -> str:
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

    #return md5ify(hash)
    global B32_ALPHABET
    return B32_ALPHABET[hash % 22 + 10] + \
           B32_ALPHABET[hash // 8     ] + \
           B32_ALPHABET[hash % 32     ] + \
           B32_ALPHABET[hash % 10]

def tommycrypt(input) -> bytes:
    def encrypt(input: bytes) -> bytes:
        global SECRET
        if len(input) == 0:
            return ""
        compressed = gzip.compress(input)
        if len(compressed) > len(input):
            compressed = input
        xored = xor(SECRET, compressed, key_offset=int(len(SECRET) / 2))
        return (hashfn(input) + b32encode(xored)).encode("utf-8")

    def decrypt(input) -> bytes:
        global SECRET
        if len(input) == 0:
            return bytes()
        if len(input) < 6:
            raise TommyExcept("invalid input")
        try:
            input = input.decode("utf-8")
        except:
            raise TommyExcept("invalid input")
        hash = input[0:4]
        decoded_payload = b32decode(input[4:])
        decrypted = xor(SECRET, decoded_payload, key_offset=int(len(SECRET) / 2))
        try:
            decompressed = gzip.decompress(decrypted)
        except:
            decompressed = decrypted
        if hashfn(decompressed) != hash:
            raise TommyExcept("invalid input")
        return decompressed

    # return encrypt(input) #debug
    # return decrypt(input) #debug

    try:
        return decrypt(input)
    except TommyExcept:
        return encrypt(input)

if __name__ == "__main__":
    import sys
    input = sys.stdin.buffer.read()
    res = tommycrypt(input)
    sys.stdout.buffer.write(res)
