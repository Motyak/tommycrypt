from common import SECRET, b32decode, b64decode, xor, hashfn, bytes_to_utf8
import sys
from functools import reduce as reduce

def multipart_decrypt(secret, input_str) -> bytes:
    if input_str[0] == "_":
        input_str = input_str[1:]
    split_input = input_str.split("_")
    split_input = [*map(lambda x: decrypt(secret, x), split_input)]
    output = reduce(lambda a, b: a + b, split_input)
    return output

def decrypt(secret, input_str) -> bytes:
    if len(input_str) == 0:
        return bytes()
    if isinstance(input_str, bytes):
        input_str = bytes_to_utf8(input_str)
    if len(input_str) < 4:
        raise Exception("invalid input")
    hash = input_str[0:4]
    decoded_payload = b32decode(input_str[4:])
    decrypted = xor(secret, decoded_payload)
    if hashfn(decrypted) != hash:
        raise Exception("invalid input")
    return decrypted

if __name__ == "__main__":
    input = sys.stdin.read()
    if len(input) > 0 and input[-1] == "\n":
        input = input[:-1] # remove trailing newline
    decrypted = multipart_decrypt(SECRET, input)
    print(bytes_to_utf8(decrypted), end="\n" if len(sys.argv) == 1 else "")
