#!/usr/bin/python3
#
# @!--#) @(#) mkindex.py, sversion 0.1.0, fversion 002, 07-august-2023
#

# ######################################################################

#
# imports
#

import os
import sys

# ######################################################################

#
# constants
#

INDEX_FILENAME = 'index.html'
TITLE_FILENAME = 'index.title'
OVERWRITE_COMMENT = '<!-- OVERWRITE: It is ok to overwrite this file :-) -->'

# ######################################################################

def hsc(s):
    h = ''

    for c in s:
        if c == '<':
            h += '&lt;'
        elif c == '>':
            h += '&gt;'
        elif c == '&':
            h += '&amp;'
        else:
            h += c

    return h

# ######################################################################

def isreadable(filename):
    readable = False

    if os.path.isfile(filename):
        if os.access(filename, os.R_OK):
            readable = True

    return readable

# ######################################################################

def safetooverwrite(filename):
    try:
        file = open(filename, 'r', encoding='utf-8')
    except IOError:
        return True

    givepermission = False

    for line in file:
        line = line.rstrip()

        if line.startswith(OVERWRITE_COMMENT):
            givepermission = True
            break

    file.close()

    return givepermission

# ######################################################################

def readtitlefile(dir):
    titlefilename = dir + '/' + TITLE_FILENAME

    try:
        titlefile = open(titlefilename, 'r', encoding='utf-8')
    except IOError:
        return ''

    title = ''

    for line in titlefile:
        line = line.strip()

        if len(line) > 0:
            title = line
            break

    titlefile.close()

    return title

# ######################################################################

def extracttitle(fname):
    try:
        f = open(fname, 'r', encoding='utf-8')
    except IOError:
        return ''

    title = ''

    for line in f:
        line = line.rstrip()

        if (line.startswith('<title>')) and (line.endswith('</title>')):
            title = line[len('<title>'):-len('</title>')]
            break

    f.close()

    return title
        
# ######################################################################

#
# Main
#

def main():
    global progname

    if not safetooverwrite(INDEX_FILENAME):
        print('{}: looks like there is hand crafted "{}" file present - not overwriting'.format(progname, INDEX_FILENAME, file=sys.stderr))
        return 1

    filesandtitles = []
    dirsandtitles = []

    for file in os.listdir('.'):
        if os.path.isdir(file):
            title = readtitlefile(file)

            if title == '':
                title = file

            dirsandtitles.append(title + '~' + file)
        else:
            if file.endswith('.html'):
                if file != INDEX_FILENAME:
                    title = extracttitle(file)

                    if title == '':
                        title = file

                    filesandtitles.append(title + '~' + file)

    filesandtitles.sort()
    dirsandtitles.sort()

    indextitle = readtitlefile('.')

    if indextitle == '':
        indextitle = '<no title>'

    try:
        file = open(INDEX_FILENAME, 'w', encoding='utf-8')
    except IOError:
        print('{}: cannot open index file "{}" for writing'.format(progname, INDEX_FILENAME, file=sys.stderr))
        return 1

    print('<head>', file=file)
    print('<title>{}</title>'.format(hsc(indextitle)), file=file)
    print(OVERWRITE_COMMENT, file=file)
    print('</head>', file=file)
    print('<body>', file=file)

    print('<h1>{}</h1>'.format(hsc(indextitle)), file=file)

    print('<tt>', file=file)

    if isreadable('../index.html'):
        print('<a href="../index.html">Back</a>', file=file)

    print('</tt>', file=file)

    itemcount = 0

    print('<p>', file=file)

    for i in range(0, len(dirsandtitles)):
        itemcount += 1

        if itemcount > 1:
            print('<br>', file=file)

        words = dirsandtitles[i].split('~')

        title   = words[0]
        dirname = words[1]

        print('<tt>+&nbsp;</tt><a href="{}/index.html">{}</a>'.format(hsc(dirname), hsc(title)), file=file)

    for i in range(0, len(filesandtitles)):
        itemcount += 1

        if itemcount > 1:
            print('<br>', file=file)

        words = filesandtitles[i].split('~')

        title    = words[0]
        filename = words[1]

        print('<tt>&nbsp;&nbsp;</tt><a href="{}">{}</a>'.format(hsc(filename), hsc(title)), file=file)

    print('</p>', file=file)

    print('<hr>', file=file)

    print('</body>', file=file)

    file.flush()

    file.close()

    return 0

# ######################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file
