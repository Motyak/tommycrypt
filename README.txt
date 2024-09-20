only works with utf-8 text,
trailing newline is not considered part of the input

## execute from shell ##
./tommycrypt.py <<< "salut à tous"
./tommycrypt.py <<< "a921a1046007abpc4i8t8081t"
echo "salut à tous" | ./tommycrypt.py | ./tommycrypt.py

## import from python ##
from tommycrypt import tommycrypt
tommycrypt("c'est l'éclate")
tommycrypt("c6be8034m1g7a91mbap79g4gy0i5")
tommycrypt(tommycrypt("c'est l'éclate"))

## communicate through encrypted tunnel with netcat ##
# run server (terminal #1)
./tommycrypt.py | nc -k -l 127.0.0.1 55555 | ./tommycrypt.py
# initiate interactive session with server (terminal #2)
./tommycrypt.py | nc 127.0.0.1 55555 | ./tommycrypt.py
# now you can communicate from client to server and vice versa,..
# ..messages are seemlessly encrypted when sent..
# ..and decrypted when received, on both side

BONUS:
- you can pass the `-m` option to toggle multiline mode on utf8 input
- now support non-utf8 input by executing `./tommycrypt-bin.py` instead

cat tommycrypt-bin.py | gzip -cf | ./tommycrypt-bin.py > cipher.txt
cat cipher.txt | ./tommycrypt-bin.py | gzip -cfd
wc -c cipher.txt tommycrypt-bin.py # cipher.txt smaller than original

---

caveat: the hash function is simple, with 1/256 chance of collision..
..therefore having a matching hash barely guarantee the cipher was produced..
..by our encryption process.
Our decrypt function decode decrypted bytes as utf8 but if the input wasn't produce..
..by ourselves, then it could contain non-utf8 bytes and the program would crash.

Here is a way to search for bad inputs (that will cause the program to crash):
1- call `xor(secret, b32decode(<str>))`..
   ..where <str> is any str containing at least two characters.
2- if it prints invalid utf8 bytes (in the form of hex bytes)..
   .., then we found a candidate, otherwise repeat previous step..
   ..with another input str
3- when you found a candidate, calculate its hash through the hashfn:..
   ..`hashfn(xor(secret, b32decode(<str>)))` and prefix the result to..
   ..the <str>.

e.g.:
Calling `xor(secret, b32decode("febb"))` produces the following bytes:..
..b'X\xb7' (invalid start byte in position 1)
Calling `hashfn(xor(secret, b32decode("febb")))` produces the following..
..hash: 'fa25'.
Prefixing the hash to the input str procuces `fa25febb`.
Calling tommycrypt("fa25febb") will therefore make the program crash.

another e.g.:
Calling `xor(secret, b32decode("1337"))` produces the following bytes:..
..b'+\xe7' (unexpected end of data in position 1)
Calling `hashfn(xor(secret, b32decode("1337")))` produces the following..
..hash: 'ee3b'.
Prefixing the hash to the input str procuces `ee3b1337`.
Calling tommycrypt("ee3b1337") will therefore make the program crash.

---

obfuscated http server through tcp relay (using netcat and named pipes):

## on server machine ##
# actual web server
php -S 127.0.0.1:55555 unepage.php
# decrypt nc (55556) tcp input, encrypt web server tcp output
nc -k -l 127.0.0.1 55556 < fifo1 \
    | ./tommycrypt.py | nc 127.0.0.1 55555 | ./tommycrypt.py > fifo1
# same command with verbose
nc -k -l 127.0.0.1 55556 < fifo1  \
    | tee >(./tommycrypt.py | nc 127.0.0.1 55555 | tee >(./tommycrypt.py > fifo1))

## on client machine ##
# encrypt nc (55557) tcp input, decrypt nc (55556) tcp output
nc -k -l 127.0.0.1 55557 < fifo2 \
    | ./tommycrypt.py | nc 127.0.0.1 55556 | ./tommycrypt.py > fifo2
# same command with verbose
nc -k -l 127.0.0.1 55557 < fifo2 \
    | tee >(./tommycrypt.py | nc 127.0.0.1 55556 | tee >(./tommycrypt.py > fifo2))

# the address 127.0.0.1:55557 can be used..
# ..from the client machine as if it was the PHP server itself

# all the traffic between the two machines appears..
# ..as encrypted data inside tcp packets

current bug with nc/php:
once the tcp connection gets closed by php, the netcat client..
..doesn't close/restart automatically (ideally the connection would get..
..renewed automatically once the php server closes the current tcp connection)
