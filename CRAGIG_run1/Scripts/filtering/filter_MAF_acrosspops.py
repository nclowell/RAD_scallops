# 20170322 Natalie Lowell
#
# PURPOSE: This script filters out loci where any haplotype occurs less than a threshold frequency,
# and only keeps loci that occur in at least N individuals.
#
# INPUTS: managed by argparse below, include:
# - transposed genepop file
# - name for text file with kept loci
# - name for text file with lostloci
# - threshold fraction setting boundary for filtering cutoff
#
# OUTPUT: 2 transposed genepop CSV format files, one with loci that passed the cutoff, the others with those that didn't
# -----------------------------------------------------------------------------
from __future__ import division
import sys
import argparse
import numpy as np
from operator import itemgetter

# manage args with argparse
parser = argparse.ArgumentParser(description="Takes a populations genepop file from Stacks and reformats it to a CSV with sample names as column headers, and loci listed down column one, genoypes in cells, and the top left cell with the word 'sample'")
parser.add_argument("-g", "--genfile", help="Genotypes file, CSV transposed genepop file", type=str, required = True)
parser.add_argument("-k", "--keptloci", help="Output file with kept loci, CSV", type=str, required = True)
parser.add_argument("-l", "--lostloci", help="Output file with lost loci, CSV", type=str, required = True)
# parser.add_argument("-n", "--atleastN", help="Keep loci if minor allele occurs in at least N individuals", type=str, required = True)
parser.add_argument("-t", "--threshold", help="Threshold cutoff for minor allele frequency, e.g., .05 for a minor allele frequency of 5%", type=float, required = True)
args = parser.parse_args()

# open files for storing output
lostloci = open(args.lostloci, "w")
keptloci = open(args.keptloci, "w")

genfile = open(args.genfile, "r") # open genotypes file for reading
genfile_lines = genfile.readlines()
gen_header = genfile_lines[0] # get first line, header
keptloci.write(gen_header) # write genfile header to output files
lostloci.write(gen_header)
restlines = genfile_lines[1:] # skip first line to get to exclude header

# maf_dict is a temporary dictionary that stores alleles as keys and allele counts as values
# the script then uses the dictionary to calculate frequencies, for filtering

kept_count = 0
lost_count = 0

locus_list = []
for locusrow in restlines: # iterate across individual genotypes within a locus
    maf_dict = {} # initiate dictionary to store allele frequencies
    rowlist = locusrow.strip().split(",")
    locus = rowlist[0]
    locus_list.append(locus)
    genlist = rowlist[1:]
    gencount = 0 # initiate counter for number of genotypes that aren't missing data
    for genotype in genlist:
        if genotype != "0000":
            gencount += 1
            allele_list = [genotype[0:2],genotype[2:4]] # assumes your genotypes are two digit format
            for allele in allele_list:
                if allele not in maf_dict:
                    maf_dict[allele] = 1
                if allele in maf_dict:
                    oldcount = maf_dict[allele]
                    newcount = oldcount + 1
                    maf_dict[allele] = newcount
    allele_list = maf_dict.keys()
    allele_freq_list = []
    for allele in allele_list: # go through dict, get allele freq, and make dict value a list with freq then count
        allele_count = maf_dict[allele]-1 # not sure where my code is adding an extra 1, so deleting one here as a quick fix
        allele_freq = float(allele_count)/float(gencount*2)
        allele_freq_list.append(allele_freq)
        new_value_list = [allele_freq, allele_count]
        maf_dict[allele] = new_value_list
    if all(x > args.threshold for x in allele_freq_list):
        keptloci.write(locusrow) # write genfile header to output files
        kept_count += 1
    else:
        lostloci.write(locusrow)
        lost_count += 1

# Close files
genfile.close()
keptloci.close()
lostloci.close()

total_count = kept_count + lost_count
retained_perc = kept_count/total_count

# Report kept/lost to user
print "\nThis script filtered out " + str(lost_count) + " loci, out of a total of " + str(total_count) + " loci."
print "\nYour keptloci file should have " + str(kept_count) + " loci, and your lostloci file should have " + str(lost_count) + " loci."
print "\nYou retained " + str(retained_perc*100)[0:4] + "% of your loci after filtering for minor allele frequency with a threshold of " + str(args.threshold) + "."
