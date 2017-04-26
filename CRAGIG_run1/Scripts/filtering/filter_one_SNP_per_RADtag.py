######################### one_SNP_per_RADtag.py ################################
# 20170425 Natalie Lowell
# PURPOSE: to filter out any additional SNPs per RAD tag, and produce a Genepop
# with only one SNP per RAD tag
# INPUT: Genepop file, with potentially more than one SNP per RAD tag
# OUTPUT: filtered Genepop file, with only one SNP per RAD tag
################################################################################

from datetime import date
import argparse
import sys
import numpy as np

# manage args with argparse
parser = argparse.ArgumentParser(description="Takes a Genepop file and filters out SNPs so that there is only one SNP per RAD tag")
parser.add_argument("-i", "--infile", help="Genepop file to filter", type=str, required = True)
parser.add_argument("-o", "--outfile", help="Relative path to output Genepop file with only one SNP per RAD tag", type=str, required = True)
args = parser.parse_args()

### REFORMAT GENEPOP TO TRANSPOSED ARRAY

# read in genepop file
infile = open(args.infile, "r")
lines = infile.readlines() # break on lines and strip white space off ends
stripped_lines = [] # initiate list to store lines stripped of white space
for line in lines: # loop to strip white space
    stripped_line = line.strip()
    stripped_lines.append(stripped_line)
mylines = stripped_lines[1:] # ditch the first line for iteration below
headerline = stripped_lines[0] # keep header for output Genepop file

# first line of transposed Genepop will be made from a list with ["sample", locus1, locus2, etc.]
list1 = []
list1.append("sample")
locinames = mylines[0].split(",")

# rest of lines
for name in locinames:
    list1.append(name)
biglist = [] # make list of lists that we will make into a numpy array soon
biglist.append(list1) # add first list for line 1
popcount = 1 # start pop counter at 1 because "pop" before first block of genotypes
samplecount = 0
perpop_numlines = []
for line in mylines[2:]: # starting with genotype lines
    length = len(line.strip().split())
    nextlist = []
    if length > 1: # should omit any "pop" lines
        linelist = line.strip().split()
        trm_name = linelist[0][:-1] # get rid of comma in sample names
        nextlist.append(trm_name)
        samplecount += 1
        for genotype in linelist[1:]:
            nextlist.append(genotype)
        biglist.append(nextlist)
    elif length == 1: # counting "pop" lines
        popcount += 1
        perpop_numlines.append(samplecount)
        samplecount = 0
    else:
        print "Something funky is happening in the length of the lines in your original genepop file. Quitting the script."
        sys.exit() # will quit of a line is nothing long
perpop_numlines.append(samplecount) # because "pop" before chunks of genotypes, need to get last pop sample lines count

myarray = np.array(biglist) # write list of lists into numpy array
t_array = myarray.transpose() # transpose array

# build dictionary with RAD tag name as key, and SNP positions as values
# and get list of RAD tag names in order
rad_dict = {}
radtag_names = []
for locus in locinames:
    locus_name_list = locus.split("_")
    radtag_name = int(locus_name_list[0])
    snp_position = locus_name_list[1]
    if radtag_name not in radtag_names:
        radtag_names.append(radtag_name)
    if radtag_name not in rad_dict:
        rad_dict[radtag_name] = [int(snp_position)]
    elif radtag_name in rad_dict:
        pos_list = rad_dict[radtag_name]
        pos_list.append(int(snp_position))
        pos_list.sort()
        rad_dict[radtag_name] = pos_list

# get list of SNPs to keep
first_snps_names = []
for radtag in radtag_names:
    snp_position_list = rad_dict[radtag]
    first_snp = str(radtag) + "_" + str(snp_position_list[0])
    first_snps_names.append(first_snp)

only_first_snp_rows_list = []
only_first_snp_rows_list.append(list(t_array[0,])) # add "sample" + sample names list for top of file
count2 = 0
for row in t_array:
    row_as_list = list(row)
    if row_as_list[0] in first_snps_names:
        count2 += 1
        only_first_snp_rows_list.append(row_as_list)

### TRANSPOSED ARRAY WITH ONLY FIRST SNPS
new_array = np.array(only_first_snp_rows_list)

### REFORMAT TO REGULAR GENEPOP

# open file for writing
outfile = open(args.outfile, "w") # open new file for writing genepop file

# get date to write to header
today = str(date.today())

# write header line to file
outfile.write(headerline + ", Filtered_one_SNP_per_RADtag on " + today + "\n") # make new header w old Genepop header, plus date, plus comment about filtering for one SNP

# transpose back
new_t_array = new_array.transpose()
numrows = new_t_array.shape[0]

SNP_header = new_t_array[0,][1:]
SNP_string = ""
for SNP in SNP_header:
    SNP_string += SNP + ","
SNP_string = SNP_string[:-1] # remove final comma

# write SNP name line to file
outfile.write(SNP_string + "\n")

# write rest of lines of file
genotypes_string = ""
start_index = 1
end_index = 1
for i in range(0,popcount):
    genotypes_string += "pop" + "\n"
    end_index += perpop_numlines[i]
    this_pop_rows = new_t_array[start_index:end_index,]
    start_index += perpop_numlines[i]
    for row in this_pop_rows:
        row_as_list = list(row)
        new_row_string = row_as_list[0] + ","
        for genotype in row[1:]:
            new_row_string += "\t" + genotype
        genotypes_string += new_row_string + "\n"
outfile.write(genotypes_string)
outfile.close()

###############################################################################
