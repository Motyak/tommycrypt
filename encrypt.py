from common import slurp_as_bytes, hashfn, b32encode, b64encode, xor
import sys

def encrypt(secret, input) -> str:
    if len(input) == 0:
        return ""
    return hashfn(input) + b32encode(xor(secret, input))

if __name__ == "__main__":
    secret = slurp_as_bytes(__file__)
    input = sys.stdin.read()
    if len(input) > 0 and input[-1] == "\n":
        input = input[:-1] # remove trailing newline
    encrypted = encrypt(secret, input)
    print(encrypted)
