# 20170306 NL
# PURPOSE: take genepop file from populations and reformat to csv genepop file like format for eleni's filtering MAF

import sys
import argparse
import numpy as np

parser = argparse.ArgumentParser(description="Takes a populations genepop file from Stacks and reformats it to a CSV with sample names as column headers, and loci listed down column one, genoypes in cells, and the top left cell with the word 'sample'")
parser.add_argument("-i", "--infile", help="Genepop file to reformat", type=str, required = True)
parser.add_argument("-o", "--outfile", help="Relative path to output file", type=str, required = True)
args = parser.parse_args()

infile = open(args.infile, "r") # read in genepop file
lines = infile.readlines() # break on lines and strip white space off ends

stripped_lines = []
for line in lines:
    stripped_line = line.strip()
    stripped_lines.append(stripped_line)

mylines = stripped_lines[1:] # ditch the first line (just says Stacks version and genepop version, and date)


# make a list of lists to format into an array, much like original genepop, then transpose

# first line will be made from a list with ["sample", locus1, locus2, etc.]

list1 = []
list1.append("sample")
locinames = mylines[0].split(",")

for name in locinames:
    list1.append(name)

biglist = [] # make list of lists that we will make into a numpy array soon
biglist.append(list1) # add first list for line 1

counter = 0
for line in mylines[2:]:
    length = len(line.strip().split())
    nextlist = []
    if length > 1:
        linelist = line.strip().split()
        trm_name = linelist[0][:-1]
        nextlist.append(trm_name)
        for genotype in linelist[1:]:
            nextlist.append(genotype)
        biglist.append(nextlist)
    elif length == 1:
        counter += 1 # trying to tell it what population the script was working on, but didn't get there, left it in to hold loop up
    else:
        print "Something funky is happening in the length of the lines in your original genepop file. Quitting the script."
        sys.exit()

myarray = np.array(biglist)
t_array = myarray.transpose()
np.savetxt("transposed_genepop.csv", t_array, delimiter=",", fmt = "%s")
