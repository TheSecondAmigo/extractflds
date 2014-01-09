extractflds
===========

Extract fields and generate PNG files from a CVS-like file

This script allows a user to generate PNG files from a Csv-like file


Usage:

    Usage: python extractflds.py [-h|--help] [--xaxis=<column number>] [--fieldcol<field number>]
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


Options:
  -h, --help         show this help message and exit
  --xaxis=XCOL
  --col=YCOL
  --colsep=COLSEP
  --fieldsep=FLDSEP
  --fieldcol=FLDCOL
  --ignorefirst
  
