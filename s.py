import functools
import itertools
import sys

B64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def slurp_as_bytes(file):
    with open(file, encoding="utf-8") as f:
        return f.read()

def bytes_to_utf8(input):
    assert isinstance(input, bytes)
    return input.decode("utf-8")

def utf8_to_bytes(input):
    assert isinstance(input, str)
    return input.encode("utf-8")

def byte_to_bin_str(byte):
    return bin(byte)[2:].rjust(8, "0")

def sextet_to_bin_str(sextet):
    return bin(sextet)[2:].rjust(6, "0")

def bin_str_to_int(bin_str):
    return int(bin_str, 2)

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
    indices = [*map(lambda c: B64_ALPHABET.index(c), input)]
    sextets = [*map(lambda i: sextet_to_bin_str(i), indices)]
    bin_str = "".join(sextets)
    if len(bin_str) % 8 != 0:
        bin_str = bin_str[:-(len(bin_str) % 8)] # drop useless bits
    return bytes(int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8))

def xor(secret, input) -> bytes:
    if isinstance(secret, str):
        secret = utf8_to_bytes(secret)
    if isinstance(input, str):
        input = utf8_to_bytes(input)

    iterator_secret = itertools.cycle(secret)
    pairs = zip(iterator_secret, input)
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

def encrypt(secret, input) -> str:
    return hashfn(input) + b64encode(xor(secret, input))

def decrypt(secret, input_str) -> bytes:
    if isinstance(input_str, bytes):
        input_str = bytes_to_utf8(input_str)
    if len(input_str) < 4:
        raise Exception("invalid input")       
    hash = input_str[0:4]
    decoded_payload = b64decode(input_str[4:])
    decrypted = xor(secret, decoded_payload)
    if hashfn(decrypted) != hash:
        raise Exception("invalid input")
    return decrypted

if __name__ == "__main__":
    secret = slurp_as_bytes(__file__)

    input = sys.stdin.read()
    print(input)

    encrypted = encrypt(secret, input)
    # encrypted = "d2a8EwkDZQ" # will not work => invalid input
    # encrypted = "fdsfds" # will not work either
    print(encrypted)

    decrypted = decrypt(secret, encrypted)
    print(bytes_to_utf8(decrypted))
