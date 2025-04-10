#!/usr/bin/env bash

awk '
  match($0, /<!-- INCLUDE:([^ ]+) -->/, arr) {
    include_file = arr[1]
    while (( "cat " include_file | getline line ) > 0 ) {
      print line
    }
    close("cat " include_file)
    next
  }
  { print }
' README.tmpl.md > README.md
