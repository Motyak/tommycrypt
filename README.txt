works with both utf-8 text and raw binary

## simple examples ##
python3 encrypt.py <<< "my message"
python3 decrypt.py <<< "_c5b90ga500gq0x9gg4r0f0"
echo "my message" | python3 encrypt.py | python3 decrypt.py

## multi-process (16 here) with binary file ##
./multi_encrypt.sh 16 < a.out > b.out.cipher
./multi_decrypt.sh < b.out.cipher > b.out
./multi_encrypt.sh 16 < a.out | ./multi_decrypt.sh > b.out

## web application frontend ##
# start the server
php -S 127.0.0.1:55555 unepage.php
# server is now available under http://127.0.0.1:55555
php -S localhost:0 unepage.php # another possibility
# support query params, e.g.: ?encrypt=message or ?decrypt=_c9cf0g40670k2d2p6

## web server outsourcing using CLI ##
curl -X POST http://127.0.0.1:55555 -d 'encrypt=my message'
curl -X POST http://127.0.0.1:55555 -d 'decrypt=_c5b90ga500gq0x9gg4r0f0'
curl -sS http://127.0.0.1:55555 -F encrypt=@a.out > b.out.cipher
curl -sS http://127.0.0.1:55555 -F decrypt=@b.out.cipher > b.out

---

=== HOW TO BENCH WITH `PERF` ===

sudo sysctl -w kernel.perf_event_paranoid=-1

alias python3='../../cpython/MYPYTHON/bin/python3 -X perf'
#export PYTHONPERFSUPPORT=1 # either this or the `-X perf` python3 option

perf record -F 99 -ag -- python3 encrypt.py < ../../monlang/bin/test/sbg.elf > sbg.elf.b32
perf script | ../../FlameGraph/stackcollapse-perf.pl > out.perf-folded
cat out.perf-folded | ../../FlameGraph/flamegraph.pl > perf-kernel.svg
