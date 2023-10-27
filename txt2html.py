#!/usr/bin/python3
#
# @(!--#) @(#) txt2html.py, sversion 0.1.0, fversion 001, 27-october-2023
#
# very basic text (.txt) to HTML converter
#

# ############################################################### #

#
# imports
#

import sys
import os
import argparse

# ############################################################### #

#
# defines
#

# css
CSS = '''
body {
  font-family: Arial, Verdana, Helvectica, sans-serif;
  background-color: white;
  color: black;
}

h1, h2, h3, h4, h5, h6 {
  border-bottom-style: solid;
  border-color: lightgrey;
  border-width: thin;
}

pre {
  font-family: "Lucinda Console", monospace;
  background-color: linen;
  color: black;
  margin-left: 30px;
  margin-right: 30px;
  padding: 5px;
}
'''

# 'in' statuses
MARK_DOWN    = 0
CODE_SEGMENT = 1

# 'last doing' modes
BLANK_LINE      = 0
HEADING         = 1
PARAGRAPH       = 2
LIST_ITEM       = 3
CODE_LINE       = 4

# ############################################################### #

def htmlescape(c):
    if c == '&':
        h = '&amp;'
    elif c == '<':
        h = '&lt;'
    elif c == '>':
        h = '&gt;'
    else:
        h = c

    return h

# ############################################################### #

def oneword(word):
    highlight = False

    if len(word) >= 3:
        if word[0] == '`':
            highlight = True
            word = word[1:]

    if highlight:
        print('<b>', end='')

    for c in word:
        if c == '`':
            if highlight:
                print('</b>', end='')
        else:
            print(htmlescape(c), end='')

    return

# ############################################################### #

def lineofwords(words):
    count = 0

    for word in words:
        count += 1

        if count > 1:
            print(' ', end='')

        oneword(word)

    return

# ############################################################### #

def lineofcode(line):
    for c in line:
        print(htmlescape(c), end='')

# ############################################################### #

def heading(line):
    words = line.split()

    headingsize = len(words[0])

    if headingsize > 6:
        headingsize = 6

    print('<h{}>'.format(headingsize), end='')

    lineofwords(words[1:])

    print('</h{}>'.format(headingsize))

    return

# ############################################################### #
            
def listitem(line):
    print('<li>', end='')

    lineofwords(line.split())

    print('</li>')

    return

# ############################################################### #

def alldashes(line):
    if len(line) <= 8:
        rc = False
    else:
        rc = True
        for c in line:
            if c != '-':
                rc = False
                break

    return rc

# ############################################################### #

def suggesttitle(lines):
    title = ''

    for line in lines:
        if len(line) > 0:
            title = line
            break

    return title

# ############################################################### #

#
# Main
#

def main():
    global progname

    parser = argparse.ArgumentParser()

    parser.add_argument('infile',  help='name of file to preprocess', nargs=1)

    args = parser.parse_args()

    try:
        infile = open(args.infile[0], 'r', encoding='utf-8')
    except IOError:
        print('{}: unable to open file "{}" for reading'.format(progname, args.infile[0]), file=sys.stderr)
        sys.exit(1)

    lines = []

    for line in infile:
        line = line.rstrip()

        lines.append(line)

    infile.close()

    title = suggesttitle(lines)

    if title == '':
        title = args.infile[0]

        if title.endswith('.md'):
            title = title[:-3]

    print('<head>')

    print('<title>', end='')
    oneword(title)
    print('</title>')

    print('<style>')
    print(CSS)
    print('</style>')

    print('</head>')

    print('<body>')

    print('<pre>')

    for line in lines:
        lineofwords(line.split())
        print('')

    print('</pre>')

    print('</body>')

    return 1

# ############################################################### #

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file
