#!/bin/bash

function multi_encrypt {
    local nb_of_parts="$1"

    mkdir "tmp$(LC_ALL=C tr -dc A-Za-z0-9 </dev/urandom | head -c 8)"
    tmpdir="$_"
    cd "$tmpdir"
    split -n "$nb_of_parts" - # takes STDIN here
    cmd="$(ls | perl -pe 's/(.+)\n/<(python3 ..\/encrypt.py -n < $1) /gm')"
    eval "cat $cmd"
    echo
    cd ..
    rm -rf "$tmpdir"
}

# if not sourced, run it
[ "${BASH_SOURCE[0]}" == "${0}" ] && {
    multi_encrypt $@
}
