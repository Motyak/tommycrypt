#!/bin/bash

function multi_decrypt {
    mkdir "tmp$(date '+%s')"
    tmpdir="$_"
    cd "$tmpdir"
    # takes STDIN here
    cmd="$(perl -pe 's/_?([^\/_]+?)(?:_|\n)/<(python3 ..\/decrypt.py -n <<< "$1") /gm')"
    eval "cat $cmd"
    cd ..
    rm -rf "$tmpdir"
}

# if not sourced, run it
[ "${BASH_SOURCE[0]}" == "${0}" ] && {
    multi_decrypt
}
