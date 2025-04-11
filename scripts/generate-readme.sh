#!/usr/bin/env bash

INPUT_FILE="packages.md"
HEADER_LINES=2

# Extract header (first 2 lines), body (after that), sort body, then reassemble
{
  head -n "$HEADER_LINES" "$INPUT_FILE"
  tail -n +$((HEADER_LINES + 1)) "$INPUT_FILE" | sort
} > sorted.md

gawk '
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
