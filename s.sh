#!/bin/bash
input="$(< /dev/stdin)"
if [[ "$input" =~ ^'#//' ]]; then
    # multiline to monoline
    echo -n "$input" | cut -c 4- | tr -d '\n' 
else
    # monoline to multiline
    echo -n "$input" | fold -w77 | awk '{print "#//"$0}'
fi
