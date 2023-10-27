#!/usr/bin/python3
#
# @(!--#) @(#) md2html.py, sversion 0.1.0, fversion 010, 24-july-2023
#
# very basic markdown (.md) to HTML converter
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
        if line.startswith('#'):
            firstspace = line.find(' ')

            if firstspace != -1:
                title = line[firstspace+1:]
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

    lines.append('')

    infile.close()

    currentlyin = MARK_DOWN
    lastdoing = BLANK_LINE

    for line in lines:
        # in code segment
        if currentlyin == CODE_SEGMENT:
            if line == '```':
                print('</pre>')
                currentlyin = MARK_DOWN
                lastdoing = BLANK_LINE
            else:
                lineofcode(line)
                print('')
        # in markdown
        elif currentlyin == MARK_DOWN:
            if line == '```':
                print('<pre>')
                currentlyin = CODE_SEGMENT
            elif alldashes(line):
                print('<hr>')
            elif line.startswith('#'):
                heading(line)
                lastdoing = HEADING
            elif line.startswith('+ '):
                if lastdoing != LIST_ITEM:
                    print('<ul>')
                listitem(line[2:])
                lastdoing = LIST_ITEM
            elif len(line) == 0:
                if lastdoing == PARAGRAPH:
                    print('</p>')
                elif lastdoing == LIST_ITEM:
                    print('</ul>')
                print('')
                lastdoing = BLANK_LINE
            else:
                if lastdoing == BLANK_LINE:
                    print('<p>')
                lineofwords(line.split())
                print('')
                lastdoing = PARAGRAPH
        else:
            print('{}: bad "in" mode of {}'.format(progname, currentlyin), file=sys.stderr)
            sys.exit(1)

    print('</body>')

    return 1

# ############################################################### #

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file
