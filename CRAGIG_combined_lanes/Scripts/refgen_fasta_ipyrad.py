# 20170719 NL
# Purpose: to generate a fasta file with one summary sequence per locus
# Inputs managed by argparse, include:
# - path to ipyrad outfiles directory
# - name of .alleles.loci file for building fasta
# - name of new fasta file "reference genome"
# Output:
# - "reference genome" fasta file
##########################################################

# import modules
import argparse as ap
import pandas as pd
import numpy as np

# manage command line arguments
parser = ap.ArgumentParser(description="Make a fasta file of all loci, with one summary sequence per locus")
parser.add_argument("-i", "--indir", help = "Path to directory with input .alleles.loci file excluding final slash; default = working directory", required = False)
parser.add_argument("-o", "--outdir", help = "Path to directory to save output fasta file excluding final slash; default = same as input file directory", required = False)
parser.add_argument("-a", "--alleles", help = "Input .alleles.loci file from ipyrad output files", required = True)
parser.add_argument("-f", "--fasta", help = "Output fasta file", required = True)
args = parser.parse_args()

# set defaults and name variables
if args.indir == None:
    indir = ""
else:
    indir = args.indir + "/"
if args.outdir == None:
    outdir = indir
else:
    outdir = args.outdir + "/"
alleles = args.alleles
fasta = args.fasta

# get blocks of alleles separated by locus
infile = open(indir + alleles, "r")
blocks = []
b = []
for line in infile:
    if line.startswith('//'):
        if len(b) > 0:
            b.append(line)
            blocks.append(b)
        b = []
    else:
          b.append(line)
infile.close()

# open file for writing output
outfile = open(outdir + fasta,"w")

# make dataframe out of alignment, get most common base, remove gaps, write to file
for block in blocks:
    for_df = []
    for line in block[:-1]:
        for_df.append(list(line.strip().split()[1]))
    block_df = pd.DataFrame(for_df)
    length = len(list(block_df.mode()))
    sum_seq = ""
    for i in np.arange(0,length):
        sum_seq += block_df.mode()[i][0]
    locus_num = block[-1].split("|")[1]
    clean_seq = sum_seq.replace("-","")
    outfile.write(">" + locus_num + "\n" + clean_seq + "\n")
outfile.close()
