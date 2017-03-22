# 20170322 Natalie Lowell
# PURPOSE: Plot the distribution of position of SNPs in tags
# INPUT: SNP Genepop file from Stacks, output file name for plot
# OUTPUT: Histogram plot of position in tag
# -----------------------------------------------------------------------------
import argparse
import numpy as np
import matplotlib.pyplot as plt

# manage inputs
parser = argparse.ArgumentParser(description="Plots distribution of SNP position in tag based on SNP Genepop file.")
parser.add_argument("-g", "--genepop", help="SNP Genepop file, e.g., output from populations in Stacks", type=str, required = True)
parser.add_argument("-t", "--plot", help="Text to add to plot file name. Date suggested. Plot name will be 'dist_snp_pos_in_tag' + your text.", type=str, required=False)
args = parser.parse_args()

addtext = ""
if args.plot != None:
    addtext += args.plot

# open file, get line with locus names
gpfile = open(args.genepop,"r")
lines = gpfile.readlines()
loci_header = lines[1] # get line with snp names

loci_list = loci_header.strip().split(",")

pos_list = []
for locus in loci_list: # loop to get positions and append to list
    locus_list = locus.split("_")
    pos_list.append(int(locus_list[1]))

plt.hist(pos_list, bins=np.arange(139)-0.5)
plt.xlabel("SNP position in tag")
plt.ylabel("Frequency")
plt.savefig("dist_snp_pos_in_tag" + addtext + ".png")
plt.close()
