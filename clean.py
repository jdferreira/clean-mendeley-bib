#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import re

hyphen_re = r'---+'
accent_re = r'''
    (?<!\{)         # Not immediately inside a latex group
    (               # Start a regular expression grouping
      \\[A-Za-z]+   # A command made up of letters
    |               # ... or ...
      \\[^A-Za-z]   # A command made up of one non-letter
    )
    (               # The argument
        \{          # The start of a grouped argument
        [^\}]*      # The (possibly empty) argument
        \}          # The end of the argument
    |               # ... or ...
        \s+       # No argument -- a space
    )
'''
lowercase_re = r'\bd\''
firstword_re = r'\s*(\w+)'

hyphen_re = re.compile(hyphen_re)
accent_re = re.compile(accent_re, re.X)
lowercase_re = re.compile(lowercase_re, re.I)
firstword_re = re.compile(firstword_re)

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def accent_replace(match):
    command, argument = match.groups()
    
    if argument.strip():
        return '{%s%s}' % (command, argument)
    else:
        return '{%s}' % (command)


def lowercase_replace(match):
    return '{' + match.group(0).lower() + '}'


ignore_keywords = ('abstract', 'file', 'keywords', 'annote')
opened_braces = 0

if len(sys.argv) < 3 or sys.argv[2] == '-':
    output = sys.stdout
else:
    output = file(sys.argv[2], 'w')

for line in file(sys.argv[1]):
    line = line.rstrip('\n')
    
    if opened_braces > 0:
        opened_braces += line.count('{') - line.count('}')
        continue
    
    match = firstword_re.match(line)
    if match is not None:
        first_word = match.group(1)
        if first_word in ignore_keywords:
            # If the number of { and } is the same, assume
            # that the group is closed and stop the group
            opened_braces = line.count('{') - line.count('}')
            continue
    
    line = hyphen_re.sub('--', line)
    line = accent_re.sub(accent_replace, line)
    line = lowercase_re.sub(lowercase_replace, line)
    print >> output, line


output.close()