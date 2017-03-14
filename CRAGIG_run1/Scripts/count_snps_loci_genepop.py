# Natalie Lowell 20161214
# Purpose: Count the number of columns of genotypes in a popgen file.
# command line argument 1 = genepop file
# assumes line 3 is your first sample

import sys

popgenfile = open(sys.argv[1], "r")
lines = popgenfile.readlines()
popgenfile.close()

loci_header_line = lines[1]
header_list = loci_header_line.strip().split(",")
num_snps = len(header_list)
tags = []
for locus in header_list:
    locus_list = locus.split("_")
    tags.append(locus_list[0])
unique_tags = list(set(tags))
num_tags = len(unique_tags)

if num_snps == num_tags:
    print "Your Genepop file has " + str(num_snps) + " SNPs."
else:
    print "Your Genepop file has " + str(num_tags) + " loci with " + str(num_snps) + " SNPs."
