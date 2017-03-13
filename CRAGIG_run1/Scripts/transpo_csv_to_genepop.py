# 20170313 Natalie Lowell
# PURPOSE: convert a transposed genepop CSV file to genepop format
# INPUTS: managed by argparse below, include:
# - transposed genepop CSV to convert to regular genepop
# OUTPUT: Genepop file
# -----------------------------------------------------------------------------

import argparse
import numpy as np
from datetime import date
import datetime

parser = argparse.ArgumentParser(description="Converts a transposed genepop CSV, where genotypes are coded in integers, and converts back to regular Genepop format")
parser.add_argument("-i", "--infile", help="Genotypes file, CSV transposed genepop file", type=str, required = True)
parser.add_argument("-o", "--outfile", help="New Genepop filepath", type=str, required = True)
parser.add_argument("-p", "--popmap", help="Popmap filepath from Stacks", type=str, required = True)
args = parser.parse_args()

popmap = open(args.popmap, "r")
infile = open(args.infile, "r") # open transposed genepop CSV for reading
outfile = open(args.outfile, "w") # open new file for writing genepop file

list_of_lines = infile.readlines() # get lines of file into list
infile.close()
header = list_of_lines[0] # take out first line as header
myarray = np.array(list_of_lines)
t_array = myarray.transpose()

cleanheader = header.strip().split(",")
header_sample_list = cleanheader[1:] # get rid of word "sample," rest is list of sample names in order of genepop file

pm_dict = {}
sampnames = []
all_popnames = []

# extract info from popmap
for line in popmap:
	popname = line.strip().split()[1]
	sampname = line.strip().split()[0]
	all_popnames.append(popname)
	sampnames.append(sampname)
samp_array = np.array(sampnames)
unique_pops = list(set(all_popnames))

# make dictionary where keys are populations and values are sample names in each population
for pop in unique_pops:
    pm_dict[pop] = []
for sample in sampnames:
        index = sampnames.index(sample)
        popmatch = all_popnames[index]
        pm_dict[popmatch].append(sample)

# in header of genotype file, what index_list
index_list = []
for pop in unique_pops:
    pop_indeces = [i for i, x in enumerate(header_sample_list) if x in pm_dict[pop]]
    index_list.append(pop_indeces)

# write date as header for first line of output file
today = str(date.today())
time = str(datetime)
outfile.write(today + "\n") # genepop header line, here will have only date
# IF YOU WANT ANYTHING ELSE IN THE FIRST LINE, HERE'S WHERE YOU COULD ADD IT

# write list of loci separated by commas for second line
list_for_array = []
for line in list_of_lines:
    newlinelist = line.strip().split(",")
    list_for_array.append(newlinelist)
myarray = np.array(list_for_array)
t_array = myarray.transpose()
loci_list = list(t_array[0][1:])
numloci = len(loci_list)

loci_string = "" # initiate loci string for second line of genepop file
for locus in loci_list:
    substring = locus + ","
    loci_string += substring
loci_string = loci_string[:-1] # get rid of last comma
outfile.write(loci_string + "\n") # write second line, locus names separated by comas

gen_array = t_array[1:]

numpops = len(unique_pops)
for i in range(0,numpops):
    outfile.write("pop" + "\n")
    pop_indeces = index_list[i]
    mini_array = gen_array[pop_indeces]
    mini_array_list = mini_array.tolist()
    for line in mini_array_list:
        substr = ""
        comma_name = line[0] + ","
        substr += comma_name
        for genotype in line[1:]:
            substr += "\t" + genotype
        outfile.write(substr + "\n")
outfile.close()







# t_array = transposed array


# get lines with these indeces from array, write in loop separated by "pop"
