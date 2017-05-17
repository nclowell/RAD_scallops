###################### ipyrad CLUSTER STATS PLOTS #############################
# 20170517 Natalie Lowell
#
# PURPOSE: to produce plots exploring output in _clusteR_stats.txt files from ipyrad
# INPUTS: managed by argparse,
# -a assembly name
# -i clust stats ipyrad output file
# -o relative path to directory to store output plot files
# -x flag if want plot of total number of clusters vs number of clusters filtered for depth
# -y average depth with majority rule vs number of clusters filtered for depth
# -z standard deviation of read depth with majority rule vs number of clusters filtered for depth
# OUTPUTS: plots, depending on which ones you specified
# ASSUMPTIONS: the directory structure is that provided by ipyrad
################################################################################

import argparse
import matplotlib.pyplot as plt
from datetime import datetime

# manage args with argparse
parser = argparse.ArgumentParser(description="Produces plots from ipyrad cluster stats output file")
parser.add_argument("-a", "--assembly", help="Assembly name", type=str, required = True)
parser.add_argument("-i", "--infile", help="Path to cluster stats output file from ipyrad", type=str, required = True)
parser.add_argument("-o", "--outdir", help="Path to directory for output files", type=str, required = False)
parser.add_argument("-x", help="Make scatter plot showing total number of clusters vs number of clusters filtered for depth", action = 'store_true')
parser.add_argument("-y", help="Make plot showing average depth with majority rule vs number of clusters filtered for depth", action = 'store_true')
parser.add_argument("-z", help="Make plot showing standard deviation of read depth with majority rule vs number of clusters filtered for depth", action = 'store_true')

args = parser.parse_args()

# directory for output files - make default empty string
outdir = ""
if args.outdir != None:
        outdir += args.outdir

# get date for naming file
today = datetime.today().strftime('%Y-%m-%d')
today = today.replace("-","")

# open cluster stats output file and get lines
cluster_stats_file = open(args.infile, "r")
cluster_stats_lines = cluster_stats_file.readlines()
cluster_stats_file.close()

# iniate lists to store columns of information
sample_list = []
clusters_total_list = []
clusters_hidepth_list = []
avg_depth_total_list = []
avg_depth_mj_list = []
avg_depth_stat_list = []
sd_depth_total_list = []
sd_depth_mj_list = []
sd_depth_stat_list = []
filtered_bad_align_list = []

# extract and store information into lists by iterating over lines in file
for line in cluster_stats_lines[1:]: # exclusing header, loop over lines
    linelist = line.strip().split()
    sample_list.append(linelist[0])
    clusters_total_list.append(linelist[1])
    clusters_hidepth_list.append(linelist[3])
    avg_depth_total_list.append(linelist[4])
    avg_depth_mj_list.append(linelist[5])
    avg_depth_stat_list.append(linelist[6])
    sd_depth_total_list.append(linelist[7])
    sd_depth_mj_list.append(linelist[8])
    sd_depth_stat_list.append(linelist[9])
    filtered_bad_align_list.append(linelist[10])

# make plot of total clusters v filtered clusters
if args.x == True:
    plt.scatter(clusters_total_list, clusters_hidepth_list)
    plt.xlabel("Total clusters")
    plt.ylabel("Number of clusters after filtering")
    plt.suptitle("Total clusters v. number filtered clusters")
    plt.savefig(outdir + 'tot_clusts_v_filt_clusts_' + today + '.png')
    plt.close()

# make plot of average depth v number clusters
if args.y == True:
    plt.scatter(avg_depth_mj_list, clusters_hidepth_list)
    plt.xlabel("Average read depth with majority rule")
    plt.ylabel("Number of clusters after filtering")
    plt.suptitle("Average read depth with majority rule v. number filtered clusters")
    plt.savefig(outdir + 'avg_rd_mj_v_filt_clusts_' + today + '.png')
    plt.close()

# make plot of average depth v number clusters
if args.z == True:
    plt.scatter(sd_depth_mj_list, clusters_hidepth_list)
    plt.xlabel("Standard deviation of read depth with majority rule")
    plt.ylabel("Number of clusters after filtering")
    plt.suptitle("Standard deviation of read depth with majority rule v. number filtered clusters")
    plt.savefig(outdir + 'sd_rd_mj_v_filt_clusts_' + today + '.png')
    plt.close()
