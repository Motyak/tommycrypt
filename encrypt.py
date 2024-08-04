from common import SECRET, hashfn, b32encode, b64encode, xor
import sys

def encrypt(secret, input) -> str:
    if len(input) == 0:
        return ""
    return "_" + hashfn(input) + b32encode(xor(secret, input))

if __name__ == "__main__":
    input = sys.stdin.read()
    if len(sys.argv) == 1 and len(input) > 0 and input[-1] == "\n":
        input = input[:-1] # remove trailing newline
    encrypted = encrypt(SECRET, input)
    print(encrypted, end="\n" if len(sys.argv) == 1 else "")
