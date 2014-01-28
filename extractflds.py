#!/usr/bin/python

"""
"""

import os
import sys
from optparse import OptionParser
import csv

USAGE_MSG = """

    Usage: python %s [-h|--help] [--xaxis=<column number>] [--fieldcol<field number>]
                  [--fieldsep=<char>] [--colsep=<char>] [--ignorefirst]
                  --col=<column number> <file>

    Description of options:

    --xaxis         : this is the column used for the X-axis (default is 1 column)
    --fieldcol      : this the sub-field within a column.
                      For example, for A_B_C in a field, if you want to extract "B",
                      the fieldcol value is 2 (the default is 1, i.e., "A")
    --fieldsep      : the character used to separate the fields (default is "_")
    --colsep        : Column separator (default is assumed to be a CSV file, so the default
                      character is ","
    --ignorefirst   : use if you want to ignore the 1st line of a file (usually the header)


    -h|--help     : displays this help message
    """ % sys.argv[0]

def Usage():
    print "%s\n" % USAGE_MSG
    sys.exit(1)


if __name__ == '__main__':
    parser = OptionParser(usage=USAGE_MSG)
    parser.add_option('--xaxis', action='store', dest='xcol', type='int')
    parser.add_option('--col', dest='ycol', action='store', type='int')
    parser.add_option('--colsep', dest='colsep', action='store', type='str')
    parser.add_option('--fieldsep', dest='fldsep', action='store', type='str')
    parser.add_option('--fieldcol', dest='fldcol', action='store', type='int')
    parser.add_option('--ignorefirst', dest='ignorerow', action='store_true')

    (options, args) = parser.parse_args()

    if not options.xcol:
        options.xcol = 0
    else:
        options.xcol -= 1

    if not options.fldcol:
        options.fldcol = 0
    else:
        options.fldcol -= 1

    if not options.fldsep:
        options.fldsep = '_'
    if len(options.fldsep) != 1:
        print "Error, field separator must be a single character not %s\n" % options.fldsep
        usage()

    if not options.colsep:
        options.colsep = ","

    if len(options.colsep) != 1:
        print "Error, column separator must be a single character not %s\n" % options.colsep
        usage()

    if not options.ycol:
        print "Column to be extracted must be specified\n"
        Usage()
    else:
        options.ycol -= 1

    if len(args) != 1:
        print "File name must be specified\n"
        Usage()

    try:
        fd = open(args[0], "r")
    except IOError as e:
	    print "I/O error({0}): {1}".format(e.errno, e.strerror)
	    sys.exit(1)

    dname = os.path.realpath(args[0])
    gnuname = dname + '.gnu'
    pngname = dname + '.png'
    outname = dname + '.out'

    try:
        fdout = open(outname, "w")
    except IOError as e:
	    print "I/O error({0}): {1}".format(e.errno, e.strerror)

    csv_fd = csv.reader(fd, delimiter=options.colsep)

    lineno = 1
    if options.ignorerow:
        line = csv_fd.next()
        lineno +=1

    maxval = -1
    for line in csv_fd:
        try:
            xrow = line[options.xcol].strip()
            yl = line[options.ycol].strip().split(options.fldsep)
            ycol = yl[options.fldcol]
            # print "%s %s" % (xrow, ycol)
            fdout.write("%s %s\n" % (xrow, ycol))
            if maxval < float(ycol):
                maxval = float(ycol)
        except:
            print "Error in line[%d] %s\n" % (lineno, line)
            sys.exit(1)

        lineno +=1

    try:
        fdout = open(outname, "w")
    except IOError as e:
	    print "I/O error({0}): {1}".format(e.errno, e.strerror)

    fd.close()
    fdout.close()

    # now create the file for
    try:
        fdout = open(gnuname, "w")
    except IOError as e:
	    print "I/O error({0}): {1}".format(e.errno, e.strerror)


    # commands for gnu plotting

    gnustr = """
set terminal png
set output '%s'
set grid
set yrange [0: %d ]
set title 'Row:Col %s, from file %s'
set xlabel 'XLabel'
set ylabel 'YLabel'
set key right top  outside  title 'Resource' box 3
plot '%s'  index 0 using 1:2 smooth unique title 'fldname' with linespoints
    """ % (pngname, maxval + 100, str(options.xcol+1) + ":" + str(options.ycol+1), dname, outname)

    fdout.write(gnustr)
    fdout.write("\n")
    fdout.close()

    os.system("gnuplot %s 2>&1 " % (gnuname))

    print "\n\nFiles created:\n\t%s\n\t%s\n\t%s\n\n"  % (gnuname, outname, pngname)


