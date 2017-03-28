# PURPOSE: to plot the number of SNPs by number of haplotypes per locus
# INPUT: haplotype.tsv file that comes out of ``populations``, as first and only command line argument

import sys
import matplotlib.pyplot as plt

# first and only argument is the haplotype file
inputfile = sys.argv[1]
hapfile = open(inputfile, "r")
lines = hapfile.readlines()
lines = lines[1:] # exclude the header line

# initiate dictionary
mydict = {}

for line in lines:
    linelist = line.split() # split on white space
    key = linelist[0] # get catalog ID as key for each key value pair in dictionary
    hapcols = linelist[2:] # get a list of just the lines of columns that have haplotype information
    col_list = [] # iniatiate a list that will include all haplotypes in a line - later, I will use set() for just the unique haplotypes, and then use that to get a count of unique haplotypes
    for col in hapcols: # for each column within a row of the haplotype file, count SNPs and alleles
        cell_list = col.split("/") # for non-homozygotes
        for item in cell_list:
            col_list.append(item)
    unique_haps_in_locus = list(set(col_list))
    num_unique_haps = len(unique_haps_in_locus)
    lengths = []
    for un_hap in unique_haps_in_locus:
        length = len(un_hap)
        lengths.append(length)
    if len(list(set(lengths))) > 1:
        print "Uh-oh! The lengths of your haplotypes were unequal, and this script assumes within a locus all haplotypes are of the same length. Quitting the script."
        sys.exit()
    mydict[key] = [unique_haps_in_locus, num_unique_haps, lengths[0]] # each item in dictionary is set of unique haplotypes, number of unique haplotypes, number of SNPs in locus

snp_counts = []
hap_counts = []

# get list of values in dictionary
dict_list = list(mydict.values())

for value in dict_list:
    hap_count = value[1]
    hap_counts.append(hap_count)
    snp_count = value[2]
    snp_counts.append(snp_count)

# plot results# plot with matplotlib pyplot
plt.scatter(snp_counts,hap_counts) # multiple box plots with list of lists
plt.xlabel('Number of SNPs in a locus') # axis label
plt.ylabel('Number of haplotypes in a locus') # axis label
plt.suptitle('Number of SNPs by number of haplotypes across individuals') # title
plt.show() # show plot
