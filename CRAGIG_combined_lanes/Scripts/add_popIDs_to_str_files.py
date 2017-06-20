################## ADD POPULATION IDS TO STRUCTURE FILES ######################
# 20170619 Natalie Lowell
# PURPOSE: to add population numbers to structure files from ipyrad using
#   population assignment files. Currently, it appears ipyrad assigns population
#   number 1 to all individuals despite the population assignment file
# INPUTS: managed by argparse below, include:
# - structure file to add population numbers to
# - population assignment file
# - output filepath
# OUTPUT: structure file with population numbers in second column
###############################################################################

import argparse

# organize parameter inputs with argparse
parser = argparse.ArgumentParser(description="Add population numbers to structure files from ipyrad")
parser.add_argument("-i", "--infile", help="input structure file that needs population numbers intsead of arbitrary 1s in second column", type=str, required=True)
parser.add_argument("-p", "--popfile", help="population assignment file from ipyrad", type=str, required=True)
parser.add_argument("-o", "--outfile", help="new structure file with population numbers in second column", type=str, required=True)
args = parser.parse_args()
