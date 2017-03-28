import argparse
import numpy as np

# manage args with argparse
parser = argparse.ArgumentParser(description="Takes haplotypes file from populations, measures frequency of each haplotype; if more than two at a genotype")
parser.add_argument("-i", "--hapfile", help="Haplotypes file from populations in Stacks", type=str, required = True)
args = parser.parse_args()

hapfile = open(args.hapfile,"r") # read file
lines = hapfile.readlines() # get lines
headerline = lines[0] # get header
headerlinelist = headerline.strip().split("\t") # get header as list; split on tab to not cut "Catalog ID" in two items
samples = headerlinelist[2:] # get sample names from header
numsamples = len(samples)

tag_list = []

genlines = lines[1:]
for line in genlines:
    linelist = line.strip().split()
    locus = linelist[0]
    locus_gens = linelist[2:]
    poss_split = locus_gens[0].split("/")
    haplength = len(poss_split[0])
    tag_dict = {}
