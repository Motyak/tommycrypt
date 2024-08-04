only works for utf-8 text, not raw binary

## simple examples ##
python3 encrypt.py <<< "my message"
python3 decrypt.py <<< "_c9200ga500gq0x9gg4r0"
echo "my message" | python3 encrypt.py | python3 decrypt.py

## multi-process examples ##
./multi_encrypt.sh 3 <<< $'test1\ntest2\ntest3'
./multi_decrypt.sh <<< "_b81b3m4066t3fr_b8723m4066t0fr_b8c93m4066t1fr"
echo $'test1\ntest2\ntest3' | ./multi_encrypt.sh 3 | ./multi_decrypt.sh

## web application frontend ##
# start the server
php -S localhost:55555 unepage.php
# server is now available under http://localhost:55555
