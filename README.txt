only works with utf-8 text,
we expect trailing newline in input

# execute from shell #
./tommycrypt.py <<< "salut à tous"
./tommycrypt.py <<< "a921a1046007abpc4i8t8081t"
echo "salut à tous" | ./tommycrypt.py | ./tommycrypt.py

# import from python #
from tommycrypt import tommycrypt
tommycrypt("c'est l'éclate")
tommycrypt("c6be8034m1g7a91mbap79g4gy0i5")
tommycrypt(tommycrypt("c'est l'éclate"))
