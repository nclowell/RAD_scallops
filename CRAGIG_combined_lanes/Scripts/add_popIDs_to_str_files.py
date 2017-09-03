################## ADD POPULATION IDS TO STRUCTURE FILES ######################
# 20170619 Natalie Lowell
# PURPOSE: to add population numbers to structure files from ipyrad using
#   population assignment files. Currently, it appears ipyrad assigns population
#   number 1 to all individuals despite the population assignment file
# INPUTS: managed by argparse below, include:
# - structure file to add population numbers to
# - population assignment file
# - output filepath
# OUTPUT: structure file with population numbers in second column
###############################################################################

import argparse

# organize parameter inputs with argparse
parser = argparse.ArgumentParser(description="Add population numbers to structure files from ipyrad")
parser.add_argument("-i", "--infile", help="input structure file that needs population numbers intsead of arbitrary 1s in second column", type=str, required=True)
parser.add_argument("-p", "--popfile", help="population assignment file from ipyrad", type=str, required=True)
parser.add_argument("-o", "--outfile", help="new structure file with population numbers in second column", type=str, required=True)
args = parser.parse_args()

# get individual-population data into a dictionary from pop assignment file
pop_dict = {}
popfile = open(args.popfile, "r")
for line in popfile:
    if line != "":
        linelist = line.strip().split()
        individual = linelist[0]
        population = linelist[1][3:]
        pop_dict[individual] = population
popfile.close()

# add population ID number to rows in structure file
outstrfile = open(args.outfile, "w")

instrfile = open(args.infile, "r")
instrfile_lines = instrfile.readlines()

outstrfile.write(instrfile_lines[0]) # write old header to new structure file

for line in instrfile_lines[1:]:
    linelist = line.strip().split()
    newline = linelist[0] + "\t" + str(pop_dict[linelist[0]]) + "\t"
    for thing in linelist[2:]:
        newline += thing + " "
    newline = newline[:-1]
    newline += "\n"
    outstrfile.write(newline)

outstrfile.close()
instrfile.close()
