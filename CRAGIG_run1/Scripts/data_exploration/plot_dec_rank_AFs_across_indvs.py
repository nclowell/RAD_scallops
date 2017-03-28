# 20170318 Natalie Lowell
# PURPOSE: make plots of rank decreasing allele frequencies of genotypes with N alleles, across a range of 2:N, from a set of samples
# INPUT: managed by argparse below, includes:
# - sample file
# - directory with individual .alleles files
# - largest number of alleles in genotype that you're interested in
# - filepath to directory to store plots
# OUPUT: plots of rank order allele frequency by number of alleles
# -----------------------------------------------------------------------------

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt

# manage args with argparse
parser = argparse.ArgumentParser(description="Takes a set of samples, calls individual alleles files, and plots rank decreasing order of allele frequencies for sets of genotypes according to number of alleles within a genotype.")
parser.add_argument("-s", "--samples", help="Text file with name of the samples to include, excluding any filepaths", type=str, required = True)
parser.add_argument("-i", "--indir", help="Path to directory with individual alleles files", type=str, required=True)
parser.add_argument("-n", "--numalls", help="Largest number of alleles you are interested in investigated, e.g., genotypes with 5 alleles in an individual. 10 is hightest number.", type=int, required=True)
parser.add_argument("-o", "--outfile", help="Directory to store plots.", type=str, required=True)
args = parser.parse_args()

# get number of alleles of interest
poss_num_alls = range(2,11)
num_alls = poss_num_alls[0:(args.numalls-1)]

# use num alleles to set bounds for xaxis on final plots
xaxis_poss_list = ['Major allele', '1st Minor allele', '2nd Minor allele', '3rd Minor allele','4th Minor allele', '5th Minor allele','6th Minor allele','7th Minor allele','8th Minor allele','9th Minor allele','10th Minor allele']
xaxis_list = xaxis_poss_list[0:args.numalls]

# get filenames from samples file
samplefile = open(args.samples,"r")
files_to_open = [] # initiate list of files to open
for line in samplefile:
    sample = line.strip()
    openfile = sample + ".alleles.tsv"
    files_to_open.append(openfile) # CHECKED BLOCK

# loop that gets name of tag and decreasing allele frequencies from set of populations
for numall in num_alls: # iterate over set of N alleles in ind genotypes; numall is type 'int'
    list_of_locus_and_afs = [] # make sublist with tag name, then rank decreasing AFs
    for filename in files_to_open:
        thisfile = open(args.indir + "/" + filename,"r")
        lines = thisfile.readlines() # get lines
        thisfile.close()
        header = lines[0]
        restlines = lines[1:]
        biglist_for_array = []
        for line in restlines:
            linelist = line.strip().split()[2:] # exclude first two columns, not useful info
            biglist_for_array.append(linelist) # make list of lists for array
        r = np.array(biglist_for_array)
        all_locus_names = [] # get locus names, incl redundant
        for row in r:
            locus_name = row[0]
            all_locus_names.append(locus_name)
        unique_locus_names = [] # just unique locus names in order
        for name in all_locus_names:
            if name not in unique_locus_names:
                unique_locus_names.append(name)
        num_loci = len(unique_locus_names) # get number unique loci
        index_list = []
        for locus in unique_locus_names:
            indeces = [i for i, x in enumerate(all_locus_names) if x == locus] # get indeces for tags to make mini arrays
            index_list.append(indeces)
        list_arrays_bytag = []
        for indeces in index_list: # make list of mini arrays by tag
            miniarray = r[indeces]
            list_arrays_bytag.append(miniarray)
        allele_counts = []
        for array in list_arrays_bytag:
            count = array.shape[0]
            allele_counts.append(count) # get allele counts
        al_inds = [i for i, x in enumerate(allele_counts) if x == int(numall)] # get indeces where allele matches this iteration of numall
        names_array = np.array(unique_locus_names)
        tags_w_numall = names_array[al_inds] # get tags with spec  numall
        for index in al_inds:
            tag_array = list_arrays_bytag[index]
            tag_list = []
            tagname = tag_array[0,0]
            tag_list.append(tagname)
            af_list = []
            for row in tag_array:
                af = float(row[2])/float(100)
                af_list.append(af)
            af_list = sorted(af_list, reverse = True) # sort in decreasing
            for af in af_list:
                tag_list.append(af)
            list_of_locus_and_afs.append(tag_list)
    array_afs = np.array(list_of_locus_and_afs)
    tarray_afs = array_afs.transpose()
    array_subset = tarray_afs[1:]
    array_subset_float = array_subset.astype(np.float)
    plotlist = []
    for row in array_subset_float:
        sublist = []
        newrow = row.astype(np.float)
        plotlist.append(list(newrow))
    if len(plotlist) >= 1: # make sure doesn't try to plot things that are empty
        # plot with matplotlib pyplot
        plt.boxplot(plotlist) # multiple box plots with list of lists
        num_rows = tarray_afs.shape[0]
        plt.xticks(range(1,num_rows),xaxis_list[0:numall]) # label x axis with population names
        plt.ylabel('Allele frequency') # axis label
        plt.suptitle('Rank decreasing allele frequencies for genotypes with ' + str(numall) + ' alleles')# title
        plt.savefig(args.outfile + "/" + "rank_dec_afs_w_" + str(numall) + "_alls" + ".png")
        plt.close()
    else:
        print "Ruh-roh. Something didn't work out, your lists for plotting don't exist. Quitting program."
        sys.exit()
