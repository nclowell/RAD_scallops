########################## PARSE BOWTIE OUTPUT #################################
# Natalie Lowell 20170515
# PURPOSE: identify loci that match to no other loci than themselves after a
# bowtie alignment
#
# INPUTS: managed by argparse,
# - name of input SAM file
# - name of output file
#
# OUTPUT:
# - filtered fasta file with only loci that matched to no other loci than themselves
# code adapted from Dan Drinan's script, https://github.com/nclowell/FISH546/blob/master/Cod-Time-Series-Project/Scripts/parseBowtie_DD.py
################################################################################

import argparse
import sys

# manage args with argparse
parser = argparse.ArgumentParser(description="Produces a fasta file with loci that matched to no other loci than themselves")
parser.add_argument("-i", "--infile", help="Input SAM file of loci aligned to a bowtie index of the same loci", type=str, required = True)
parser.add_argument("-o", "--outfile", help="Name of output file for filtered fasta", type=str, required = True)
args = parser.parse_args()



loci_to_remove = [] # initiate list to store loci to filter OUT
loci_to_keep = [] # initiate list to store loci to KEEP
loci_dict = {} # iniatie dictionary for sorting loci and their sequences
parsecounter = 0 # counter to get number of reads parsed

# open alignment file for reading
infile = open(args.infile,"r")

# parse bowtie output by checking whether read and reference name match
# if match, then aligning to itself, and should keep
# if don't match, then aligning to another locus, and should filter out
for line in infile:
    parsecounter += 1
    locus_read_name = line.split()[0] # extracts locus read name
    locus_ref_name = line.split()[2] # extracts locus reference name
    seq = line.split()[9] # extracts sequence
    loci_dict[locus_read_name] = seq
    if locus_read_name == locus_ref_name: # keep only if read and reference names match
        loci_to_keep.append(locus_read_name)
    else: # if names don't match,
        loci_to_remove.append(locus_read_name) # get rid of both the read name locus
        loci_to_remove.append(locus_ref_name) # and the reference name locus
infile.close()

# tell user how many reads were parsed
print "Parsed " + str(parsecounter) + " reads in your SAM file."

# write "good" loci to a file
outfile = open(args.outfile, 'w')

# restart counter for counting number of reads written to output
writecounter = 0

# in order to keep a locus, it has to have aligned only to itself
# the previous loop didn't check for this, so here's a second loop to check
for locus in loci_dict.keys(): # for each locus in the dictionary
    if (locus not in loci_to_remove) and (locus in loci_to_keep): # aligned to self and nothing else,
        outfile.write('>' + locus + '\n') # write descriptive fasta line with > and locus name
        outfile.write(loci_dict[locus] + '\n') # write sequence fasta line pulling from loci dictionary
        writecounter += 1
outfile.close()

# tell user how many reads were written to output file
print "Wrote " + str(writecounter) + " reads to filtered output file."
