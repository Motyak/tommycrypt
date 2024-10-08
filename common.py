import itertools
import sys #debug

B32_ALPHABET = "0123456789abcdefghikmnpqrstuwxyz" # removed J, L, O, V
B64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def slurp_as_bytes(file):
    with open(file, encoding="utf-8") as f:
        return f.read()

SECRET = slurp_as_bytes(__file__)

def bytes_to_utf8(input):
    assert isinstance(input, bytes)
    return input.decode("utf-8")

def utf8_to_bytes(input):
    assert isinstance(input, str)
    return input.encode("utf-8")

def byte_to_bin_str(byte):
    return bin(byte)[2:].rjust(8, "0")

def quintet_to_bin_str(quintet):
    return bin(quintet)[2:].rjust(5, "0")

def sextet_to_bin_str(sextet):
    return bin(sextet)[2:].rjust(6, "0")

def bin_str_to_int(bin_str):
    return int(bin_str, 2)

def b32encode(input) -> str:
    global B32_ALPHABET
    assert isinstance(B32_ALPHABET, str)
    assert len(B32_ALPHABET) == 32
    if len(input) == 0:
        return ""
    if isinstance(input, str):
        input = utf8_to_bytes(input)
    bin_str = ""
    for b in input:
        bin_str += byte_to_bin_str(b)
    quintets = [bin_str[i:i+5] for i in range(0, len(bin_str), 5)]
    quintets[-1] = quintets[-1].ljust(5, "0") # potential padding
    indices = [*map(bin_str_to_int, quintets)]
    base32 = "".join([*map(lambda i: B32_ALPHABET[i], indices)])
    return base32

def b32decode(input) -> bytes:
    global B32_ALPHABET
    assert isinstance(B32_ALPHABET, str)
    assert len(B32_ALPHABET) == 32
    for c in input:
        if c not in B32_ALPHABET:
            raise Exception(f"character `{c}` is not in base32 alphabet ({B32_ALPHABET})")

    indices = [*map(lambda c: B32_ALPHABET.index(c), input)]
    quintets = [*map(lambda i: quintet_to_bin_str(i), indices)]
    bin_str = "".join(quintets)
    if len(bin_str) % 8 != 0:
        bin_str = bin_str[:-(len(bin_str) % 8)] # drop useless bits
    return bytes(int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8))

def b64encode(input) -> str:
    global B64_ALPHABET
    assert isinstance(B64_ALPHABET, str)
    assert len(B64_ALPHABET) == 64
    if len(input) == 0:
        return ""
    if isinstance(input, str):
        input = utf8_to_bytes(input)

    reducer = lambda acc, c: acc + byte_to_bin_str(c)
    bin_str = functools.reduce(reducer, input, "")
    sextets = [bin_str[i:i+6] for i in range(0, len(bin_str), 6)]
    sextets[-1] = sextets[-1].ljust(6, "0") # potential padding
    indices = [*map(bin_str_to_int, sextets)]
    base64 = "".join([*map(lambda i: B64_ALPHABET[i], indices)])
    return base64

def b64decode(input) -> bytes:
    global B64_ALPHABET
    assert isinstance(B64_ALPHABET, str)
    assert len(B64_ALPHABET) == 64
    for c in input:
        if c not in B64_ALPHABET:
            raise Exception(f"character `{c}` is not in base32 alphabet ({B64_ALPHABET})")

    indices = [*map(lambda c: B64_ALPHABET.index(c), input)]
    sextets = [*map(lambda i: sextet_to_bin_str(i), indices)]
    bin_str = "".join(sextets)
    if len(bin_str) % 8 != 0:
        bin_str = bin_str[:-(len(bin_str) % 8)] # drop useless bits
    return bytes(int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8))
    
def xor(key, input, key_offset=0) -> bytes:
    if isinstance(key, str):
        key = utf8_to_bytes(key)
    if isinstance(input, str):
        input = utf8_to_bytes(input)
    consume = lambda it, n: [next(it) for i in range(n)]

    iterator_key = itertools.cycle(key)
    consume(iterator_key, key_offset)
    pairs = zip(iterator_key, input)
    return bytes(map(lambda x: x[0] ^ x[1], pairs))

def hashfn(input) -> str:
    if isinstance(input, str):
        input = utf8_to_bytes(input)

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
