import itertools
import sys

def slurp_as_bytes(file):
    with open(file, encoding="utf-8") as f:
        return f.read()

def bytes_to_utf8(input):
    assert isinstance(input, bytes)
    return input.decode("utf-8")

def utf8_to_bytes(input):
    assert isinstance(input, str)
    return input.encode("utf-8")

def xor(secret, input) -> bytes:
    if isinstance(secret, str):
        secret = utf8_to_bytes(secret)
    if isinstance(input, str):
        input = utf8_to_bytes(input)

    iterator_secret = itertools.cycle(secret)
    pairs = zip(iterator_secret, input)
    return bytes(map(lambda x: x[0] ^ x[1], pairs))

def hashfn(input) -> bytes:
    if isinstance(input, str):
        input = utf8_to_bytes(input)

    def md5ify(hash):
        assert isinstance(hash, int)
        assert 0 <= hash and hash <= 255
        str_hash = hex(43210 + int(hash * (22222 / 255)))[2:]
        return utf8_to_bytes(str_hash)
    
    T = [i for i in range(0, 256)]
    hash = 0
    for b in input:
        hash = T[hash ^ b]
    return md5ify(hash)

def encrypt(secret, input) -> bytes:
    return hashfn(input) + b'\n' + xor(secret, input)

def decrypt(secret, input_str) -> bytes:
    if isinstance(input_str, bytes):
        input_str = bytes_to_utf8(input_str)
    inputs = input_str.split("\n", 1)
    if len(inputs) != 2:
        raise Exception("invalid input")
    hash, payload = inputs
    decrypted_payload = xor(secret, payload)
    if hashfn(decrypted_payload) != utf8_to_bytes(hash):
        raise Exception("invalid input")
    return decrypted_payload

if __name__ == "__main__":
    secret = slurp_as_bytes(__file__)

    input = sys.stdin.read()
    print(input)

    encrypted = encrypt(secret, input)
    # encrypted = b'd2a8\n\x0e\t\x03e' # will not work => invalid input
    # encrypted = b'fdsfds' # will not work either
    print(encrypted)

    decrypted = decrypt(secret, encrypted)
    print(bytes_to_utf8(decrypted))
