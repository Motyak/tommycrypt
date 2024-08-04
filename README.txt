works with both utf-8 text and raw binary

## simple examples ##
python3 encrypt.py <<< "my message"
python3 decrypt.py <<< "_c9200ga500gq0x9gg4r0"
echo "my message" | python3 encrypt.py | python3 decrypt.py

## multi-process (16 here) with binary file ##
./multi_encrypt.sh 16 < a.out > b.out.cipher
./multi_decrypt.sh < b.out.cipher > b.out
./multi_encrypt.sh 16 < a.out | ./multi_decrypt.sh > b.out

## web application frontend ##
# start the server
php -S localhost:55555 unepage.php
# server is now available under http://localhost:55555
