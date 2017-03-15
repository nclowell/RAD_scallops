# 20170314 Natalie Lowell
# PURPOSE: build a Genepop file by tag instead of by SNP using populations haplotypes file
# INPUTS: populations haplotypes file
# OUTPUTS: Genepop file by tags
# ------------------------------------------------------------------------------
import argparse
import numpy as np
from datetime import date
import sys

# manage inputs w argparse below, inputs:
parser = argparse.ArgumentParser(description="Parses the populations haplotypes file to make a Genepop file based on tags instead of SNPs (default to populations program)")
parser.add_argument("-f", "--hapfile", help="Genotypes file, CSV transposed genepop file", type=str, required = True)
parser.add_argument("-p", "--popmap", help="Population map used in Stacks populations", type=str, required=True)
parser.add_argument("-o", "--output", help="Output filepath for new tags Genepop file", type=str, required=True)
args = parser.parse_args()

hapfile = open(args.hapfile, "r") # read in file
lines_list = hapfile.readlines() # get lines of file into list
hapfile.close()

header_line = lines_list[0] # get header line from file
header_list = header_line.strip().split()
header_sample_list = header_list[3:] # list with sample names in order of header_list

locus_lines_list = lines_list[1:] # get list of lines of genotypes, all but header_list

# for loop that stores a unique ordered set of alleles (value) per locus (key) in a dictionary
gp_dict = {} # initiate dictionary
for genotypeline in locus_lines_list:
    linelist = genotypeline.strip().split()
    tagID = linelist[0] # get tag ID from line, will be key in dictionary
    linelist = linelist[2:] # starting from alleles, excluding catalog
    allele_list = [] # initiate list to store all alleles, including redundant ones
    for genotype in linelist: # get both alleles from heterozygotes and remove "-"
        alleles = genotype.split("/")
        for allele in alleles:
            allele_list.append(allele)
    unique_alleles = list(set(allele_list))
    if "-" in unique_alleles:
        unique_alleles.remove("-")
    unique_alleles.sort()
    gp_dict[tagID] = unique_alleles

# because dict not sorted by key, get catalog locus IDs in order
list_of_list = []
for line in lines_list:
    sublist = line.strip().split("\t")
    list_of_list.append(sublist)
file_array = np.array(list_of_list)
trans_array = file_array.transpose()
tags_in_fileorder = trans_array[0][1:] # catalog locus IDs in ordered list

# get array of only genotypes from haplotypes file, and num rows and cols
loop_array = file_array[1:,2:]
num_rows_in_array = loop_array.shape[0] # get number of rows
num_cols_in_array = loop_array.shape[1] # get number of columns

# first, just get replace "-" with "0000" for missing values
for i in range(0,num_rows_in_array):
    for x in range(0,num_cols_in_array):
        if loop_array[i][x]=="-":
            loop_array[i][x]="0000"

# GET NUMERIC GENOTYPES  BY USING INDEX IN DICTIONARY + 1
tripcount = 0 # count genotypes with more than two alleles at a locus - contamination or paralogous genes?
for i in range(0,num_rows_in_array):
    poss_alleles = gp_dict[tags_in_fileorder[i]]
    for x in range(0,num_cols_in_array):
        if loop_array[i][x] != "0000":
            genotype = loop_array[i][x]
            split_gen = genotype.split("/")
            if len(split_gen) == 1: # FOR HOMOZYGOTES
                num_allele = str(poss_alleles.index(genotype) + 1)
                if len(num_allele) == 1:
                    num_allele = "0" + num_allele # add leading zeros where appropriate
                elif len(num_allele) > 2: # the most alleles at one of my loci is 45, but regardless, thought I'd add this check
                    print "This script noticed that at some point you had more than 99 alleles, and can't support this number of alleles. Abort!"
                    sys.exit()
                num_genotype = num_allele + num_allele
                loop_array[i][x] = num_genotype
            elif len(split_gen) == 2: # FOR HETEROZYGOTES
                char_allele_1 = split_gen[0]
                char_allele_2 = split_gen[1]
                num_allele_1 = str(poss_alleles.index(char_allele_1) + 1)
                num_allele_2 = str(poss_alleles.index(char_allele_2) + 1)
                if len(num_allele_1) == 1:
                    num_allele_1 = "0" + num_allele_1 # add leading zeros where appropriate
                elif len(num_allele_1) > 2: # the most alleles at one of my loci is 45, but regardless, thought I'd add this check
                    print "This script noticed that at some point you had more than 99 alleles, and can't support this number of alleles. Abort!"
                    sys.exit()
                if len(num_allele_2) == 1:
                    num_allele_2 = "0" + num_allele_2 # add leading zeros where appropriate
                elif len(num_allele_2) > 2: # the most alleles at one of my loci is 45, but regardless, thought I'd add this check
                    print "This script noticed that at some point you had more than 99 alleles, and can't support this number of alleles. Abort!"
                    sys.exit()
                num_genotype = num_allele_1 + num_allele_2
                loop_array[i][x] = num_genotype
            else:
                tripcount += 1
                num_genotype = "0000" # replacing genotype with more than two alleles as missing data
                loop_array[i][x] = num_genotype

# open file for writing output
output = open(args.output, "w")

# FIRST LINE OF OUTPUT GENEPOP FILE
# write date as header for first line of output file
today = str(date.today())
output.write(today + "\n") # genepop header line, here will have only date

# SECOND LINE OF OUTPUT GENEPOP FILE
tags_str = ""
for tag in tags_in_fileorder:
    tags_str += tag + ","
tags_str = tags_str[:-1] # get rid of final comma
output.write(tags_str + "\n") # add locus names line, seprated by commas

# GET UNIQUE POPS AND MATCHING INDECES IN HAPLOTYPES FILE
popmap = open(args.popmap,"r")
pm_dict = {}
sampnames = []
all_popnames = []
for line in popmap: # extract info from popmap & store in dictionary
	popname = line.strip().split()[1]
	sampname = line.strip().split()[0]
	all_popnames.append(popname)
	sampnames.append(sampname)
samp_array = np.array(sampnames)
def ord_unique_set(list): # get ordered unique set of populations, to keep order in original genepop
    seen = set()
    seen_add = seen.add
    return [x for x in list if not (x in seen or seen_add(x))]
unique_pops = ord_unique_set(all_popnames)
for pop in unique_pops:
    pm_dict[pop] = []
for sample in sampnames:
        index = sampnames.index(sample)
        popmatch = all_popnames[index]
        pm_dict[popmatch].append(sample)
index_list = [] # initiate list to store lists of indeces of each population's samples in the haplotypes header sample list
for pop in unique_pops:
    samps_in_pop = pm_dict[pop]
    pop_indeces = []
    for samp in samps_in_pop:
        if samp in header_sample_list: # some samples in popmap may have been excluded in running populations
            index = header_sample_list.index(samp)
            pop_indeces.append(index)
            pop_indeces.sort()
    index_list.append(pop_indeces)
popmap.close()


for pop in unique_pops:
    output.write("pop" + "\n")
    samples = pm_dict[pop]
    samples.sort()
    popindex = unique_pops.index(pop)
    popgenrows = loop_array[index_list[popindex]]
    print popgenrows.shape[0]
    print popgenrows.shape[1]
    substring = ""
    for i in range(0,len(popgenrows)):
        row = popgenrows[i]
        namestring = samples[i] + ","
        genstring = ""
        for genotype in row:
            genstring += "\t" + genotype
        output.write(namestring + genstring + "\n")

output.close()
print "This script found " + str(tripcount) + " genotypes to have more than two alleles, and replaced them with missing values, 0000"
