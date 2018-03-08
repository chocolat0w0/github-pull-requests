#!/bin/bash

git fetch --prune > /dev/null 2>&1
git checkout dev > /dev/null 2>&1
git branch -D reviewing > /dev/null 2>&1

script=$(dirname ${0})/prfetch.py

number=`${script} | percol | sed 's/,/_/g' | sed -E 's/[\t ]+/,/g' | cut -d, -f2`

git fetch origin pull/${number}/head:reviewing
git checkout reviewing
