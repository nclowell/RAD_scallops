# 20170404 Natalie Lowell
# PURPOSE: to produce a histogram of read depth of tags within individuals
# INPUT: managed by argparse, includes:
# - text file with name of matches files to include
# - relative path to directory with matches files
# - relative path to directory to store plots
# OUTPUT: plots of read depth per locus in individuals, ???
################################################################################

# import modules
import argparse
import matplotlib.pyplot as plt
import numpy as np
import subprocess

# manage user input
parser = argparse.ArgumentParser(description="Makes a list of matches files from sstacks, parses them, and produces a histogram of tag read depth within individuals. To avoid memory errors, the histogram is of a random subset, default 1/100 of your read depth data. You can adjust the size of this subset depending on your needs.")
# parser.add_argument("-m", "--matchfiles", help="Text file with each line as name of matches files to analyze", type=str, required=True)
parser.add_argument("-i", "--indir", help="Relative path to directory with matches files and text file with names of matches file", type=str, required=True)
parser.add_argument("-o", "--outdir", help="Relative path to directory to store output files", type=str, required=True)
parser.add_argument("-d", "--dataname", help="Name of sequencing lane, run, or data set to appear in plots", type=str, required=False)
parser.add_argument("-p", "--plotname", help="Filename for histogram of within individual tag read depths, 99 percentile", type=str, required=True)
parser.add_argument("-c", "--percentile", help="Percentile of data to include in histogram. Default = 99, to avoid tail of data that makes plot unreadable.")
parser.add_argument("-s", "--subset", help="Fraction of data you want to randomly sample, e.g., '-s 100' would subset 1/100 of your data. Subsetting is necessary because otherwise the script can hit the memory capacity of your computer. Default = 100", type=str, default=True)
args = parser.parse_args()

### get text file with matches file names

# make bash string, and call with subprocess
bash_str = 'cd ' + args.indir + '\n' + 'printf "%s\n" *.matches.tsv > list_matches_filenames.txt'
subprocess.call([bash_str], shell = True)

# read file back in
matchfiles = open(args.indir + "/" + "list_matches_filenames.txt")

### get file names into list from matches list text file
lines = matchfiles.readlines()
filename_list = []
for line in lines:
    filename = line.strip()
    filename_list.append(filename)
num_files = len(filename_list)

### get within individual count data by building a temporary dictionary and merging lists

# get fraction size for subset
subset = ""
if args.subset == None:
    subset += 100
else:
    subset +=  args.subset

# parse files
within_inds_tag_rd = [] # initiate list to store tag read depth within individuals
for thisfile in filename_list:
    indfile = open(args.indir + "/" + thisfile,"r")
    lines = indfile.readlines()[1:]
    within_dict = {}
    for line in lines:
        linelist = line.strip().split()
        locus = int(linelist[2])
        count = int(linelist[6])
        if locus not in  within_dict:
            within_dict[locus] = int(count)
        elif locus in within_dict:
            oldcount =  within_dict[locus]
            newcount = oldcount + count
            within_dict[locus] = newcount
        else:
            print "Something funky is going on."
        counts = within_dict.values()
        length = len(counts)
        sample = list(np.random.choice(counts, size=(length/int(subset)),replace=False))
        within_inds_tag_rd += sample
    indfile.close()

### get tag read depths up to 99th percentile as default or specified to exclude most of tail that makes the plot unreadable

if args.percentile == None: # loop to make 99 default
    perc = 99
else:
    perc = int(args.percentile)
p = np.percentile(within_inds_tag_rd,perc) # get percentile value
within_ints_rag_rd_perc = []
for rd in within_inds_tag_rd: # keep only those up until percentile value
    if rd < p:
        within_inds_tag_rd_perc.append(rd)

### plot histogram of within individual tag read depths

# get optional data name string to add to plot
data_name_str = ""
if args.dataname == None:
    data_name_str = data_name_str
else:
    data_name_str = " in " + args.dataname

# plot
plt.hist(within_ints_rag_rd_perc, bins = np.arange(0,max(within_ints_rag_rd_99)+1,10)-5)
plt.xlabel("Read depth")
plt.ylabel("Frequency")
plt.suptitle("Distribution of tag read depths \nwithin individuals" + data_name_str + " with " + str(perc) + " percentile")
plt.show()
