# 20170313 Natalie Lowell
# based on Eleni's script for filtering missing values, but restructured to use the population map
# to pull out what samples are in each population, and then using these indeces to iterate
# over populations and filter out any loci where missing value frequency goes above the cutoff in
# any population

# PURPOSE: filter transposed genepop file for missing values using a threshold, often .5
# INPUTS: managed by argparse below, include:
# - transposed genepop file
# - population map for Stacks
# - name for text file with kept loci
# - name for text file with lostloci
# - threshold fraction setting boundary for filtering cutoff
# -----------------------------------------------------------------------------
import sys
import argparse
import numpy as np
from operator import itemgetter

# manage args with argparse
parser = argparse.ArgumentParser(description="Takes a populations genepop file from Stacks and reformats it to a CSV with sample names as column headers, and loci listed down column one, genoypes in cells, and the top left cell with the word 'sample'")
parser.add_argument("-g", "--genfile", help="Genotypes file, CSV transposed genepop file", type=str, required = True)
parser.add_argument("-p", "--popmap", help="Population map used in Stacks populations", type=str, required=True)
parser.add_argument("-k", "--keptloci", help="Output file with kept loci, CSV", type=str, required = True)
parser.add_argument("-l", "--lostloci", help="Output file with lost loci, CSV", type=str, required = True)
parser.add_argument("-t", "--threshold", help="Threshold cutoff for missing data, e.g., .5 for less than 50 percent missing data", type=int, required = True)
args = parser.parse_args()

# get col indeces for each pop, by first getting unique pop name
# get pop names
popmap = open(args.popmap, "r")
all_popnames = [] # list to store names of all populations
sampnames = [] # iniate list to store sample names in same order as pop map order
for line in popmap:
	popname = line.strip().split()[1]
	sampname = line.strip().split()[0]
	all_popnames.append(popname)
	sampnames.append(sampname)
unique_popnames = list(set(all_popnames))
popmap.close()


# open files for storing output
lostloci = open(args.lostloci, "w")
keptloci = open(args.keptloci, "w")

# ---
genfile = open(args.genfile, "r") # open genotypes file for reading
gen_header = genfile.readline() # get first line, header
keptloci.write(gen_header) # write genfile header to output files
lostloci.write(gen_header)

# get indeces
samp_array = np.array(sampnames)
index_list = [] # list with sublists that contain the indeces of the samples within a population from the order they're presented in the popmap
sampsets = [] # list with sublists that contain all the samples within a population
header_indeces_list = []
for population in unique_popnames:
	indeces = [i for i, x in enumerate(all_popnames) if x == population]
	index_list.append(indeces)
	sampset = list(samp_array[indeces])
	sampsets.append(sampset)
	gen_header_list = gen_header.split(",")
	header_indeces = [i for i, x in enumerate(gen_header_list) if x in sampset]
	header_indeces_list.append(header_indeces)

genfile_lines = genfile.readlines()
genotype_lines = genfile_lines[1:] # skip first line to get to exclude header

numpop_range = range(0,len(unique_popnames)) # make list to iterate over within loop, prior to loop
for locus_row in genotype_lines:
	stripped_row = locus_row.strip()
	missdata_freq_list = [] # initiate list that will store frequency of missing data by population within a locus
	split_row = stripped_row.split(",")
	row_array = np.array(split_row)
	for population_num in numpop_range:
		thispop = unique_popnames[int(population_num)]
		pop_genotypes = list(row_array[header_indeces_list[population_num]])
		miss_gen_by_locus = float(pop_genotypes.count("0000"))
		num_ind_thispop = float(len(thispop))
		percent_miss_data_thispop = float(miss_gen_by_locus/num_ind_thispop)
		missdata_freq_list.append(percent_miss_data_thispop)
	if all(x < args.threshold for x in missdata_freq_list):
		keptloci.write(locus_row)
	else:
		lostloci.write(locus_row)

# Close files
genfile.close()
keptloci.close()
lostloci.close()
