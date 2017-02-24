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

print "\nYour text file has " + str(numlines) + " lines, and you want to extract lines " + str(sys.argv[2]) + " and write it to the file with name " + str(sys.argv[3])

numtorem = sys.argv[2]

keeplines = lines[int(numtorem):]

keepstring = ""
for line in keeplines:
    keepstring += line + "\n"

outfile = open(sys.argv[3], "w")
outfile.write(keepstring)
outfile.close
