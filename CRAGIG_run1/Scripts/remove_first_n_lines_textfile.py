# purpose: to extract set lines from a text file
# 20170224 NL
# my use is to remove the first line from the catalog snps file

# INPUTS
# arg 1 = file to remove lines from
# arg 2 = number of lines
# arg 3 = new name for file

import sys

infile = open(sys.argv[1], "r")
lines = infile.readlines()
numlines = len(lines)
infile.close()

numtorem = sys.argv[2]

keeplines = [int(numtorem):]

outfile = open(sys.argv[3], "w")
outfile.write(keeplines)
outfile.close
