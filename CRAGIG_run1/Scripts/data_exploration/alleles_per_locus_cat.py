# 20170313 Natalie Lowell
# takes a catalog alleles file and makes a boxplot showing the distributin of number of alleles
# only input is the catalog file

import sys
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Makes a boxplot per population showing the number of alleles per locus")
parser.add_argument("-c", "--catalog", help="Catalog file from Stacks pipeline", type=str, required = True)
args = parser.parse_args()

catalog = open(args.catalog, "r")

lines = catalog.readlines()
lines = lines[1:]

dnary = {}

for line in lines:
    linelist = line.strip().split()
    tag = linelist[2]
    if tag not in dnary:
        dnary[tag] = 1 # first allele
    else:
        value = dnary[tag]
        newval = value + 1 # add allele count for every occurrence of locus in alleles file
        dnary[tag] = newval

values_list = dnary.values()


plt.hist(values_list, bins = range(0,100))
plt.xlim([0,50])
plt.xlabel('Number of alleles')
plt.ylabel('Frequency of loci')
plt.suptitle('Alleles per locus from catalog file')
plt.show()
