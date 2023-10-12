#!/bin/bash


output_file="changes.txt"

> "$output_file"

files=$(find . -type f ! -path './.git/*' ! -path './idea/*' ! -path './venv/*' ! -path './.idea/*')

for file in $files; do
    filename="$file"
    commit=$(git log --pretty=format:%h -1 -- "$file")
    if [[ $commit ]]; then
      echo "$filename = $commit" >> "$output_file"
    else
      echo "$filename = No commit" >> "$output_file"
    fi
done
