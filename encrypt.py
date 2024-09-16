from common import SECRET, hashfn, b32encode, b64encode, xor
import sys

def encrypt(secret, input) -> str:
    if len(input) == 0:
        return ""
    xored = xor(secret, input, key_offset=int(len(secret) / 2))
    return "_" + hashfn(input) + b32encode(xored)

if __name__ == "__main__":
    input = sys.stdin.buffer.read()
    LF = 10
    if len(sys.argv) == 2 and len(input) > 0 and input[-1] == LF:
        input = input[:-1] # remove trailing newline
    encrypted = encrypt(SECRET, input)
    print(encrypted, end="" if len(sys.argv) == 2 else "\n")
