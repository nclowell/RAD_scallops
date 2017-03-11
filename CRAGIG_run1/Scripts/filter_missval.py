### Eleni Petrou
#python Eleni_FilterLoci_by_MissingValues.py Marr15_batch1_filteredMAF_genotypes.csv Marr15_batch1_FinalCleanOutput.csv Marr15_batch1_FinalBlacklisted_output.csv

## MF edit 12/8/2016 for Lanes 1 and 2 Pcod samples

#3 NL edit 3/7/17 for CRAGIG run1



# -----------------------------------------------------------------------------
import sys
import argparse
import numpy as np

# manage args with argparse
parser = argparse.ArgumentParser(description="Takes a populations genepop file from Stacks and reformats it to a CSV with sample names as column headers, and loci listed down column one, genoypes in cells, and the top left cell with the word 'sample'")
parser.add_argument("-g", "--genfile", help="Genotypes file, CSV transposed genepop file", type=str, required = True)
parser.add_argument("-p", "--popmap", help="Population map used in Stacks populations", type=stry, required=True)
parser.add_argument("-k", "--keptloci", help="Output file with kept loci, CSV", type=str, required = True)
parser.add_argument("-l", "--lostloci", help="Output file with lost loci, CSV", type=str, required = True)
args = parser.parse_args()


# get col indeces for each pop, by first getting unique pop name
# get pop names
popmap = open(args.popmap, "r")
all_popnames = [] # list to store names of all populations
unique_popnames = [] # list with just unique population names, to be filled after following loop
sampnames = [] # iniate list to store sample names in same order as pop map order
for line in popmap:
	popname = line.strip().split()[1]
	sampname = line.strip().split()[0]
	all_popnames.append(popname)
	sampenames.append(sampname)
unique_popnames.append(list(set(all_popnames)))
popmap.close()

# open files for storing output
lostloci = open(args.lostloci, "w")
keptloci = open(args.keptloci, "w")

# ---
genfile = open(args.genfile, "r") # open genotypes file for reading
gen_header = genfile.readline() # get first line, header
keptloci.write(gen_header) # write genfile header to output files
lostloci.write(gen_header)


# get indeces

index_list = []
for population in unique_popnames:
	indices = [i for i, x in enumerate(popnames) if x == population]
	print indices

genfile_lines = genfile.readlines()
genotype_lines = genfile_lines[1:]
for locus_row in genotype_lines:
	stripped_row = locus_row.strip()
	missdata_freq_list = [] # initiate list that will store frequency of missing data by population within a locus
	split_row = stripped_row.split(",")
	for population_num in enumerate(unique_popnames):
		split_row[index_list[population_num]]






## ex code:
# indices = [i for i, x in enumerate(my_list) if x == "whatever"]
header = True # will toggle to False after first iteration so that only first line becomes header to output files
for mystring in genfile:		# Read in each line in the file as a string
	# if header:			# This code takes the header from the original genotypes file and saves it as the header of the output genotypes files. We do not remove any individuals in this script so we can keep the original headers
	# 	genotypes_header = mystring
	# 	keptloci.write(genotypes_header)
	# 	lostloci.write(genotypes_header)
	# 	header = False
	else:
		stripped_string = mystring.strip('\n')		## Make sure to strip your string of the newline, otherwise weird stuff might happen.
		locus_name = stripped_string.split(",")[0] 	## This tells the computer how to split your string. If csv, use comma. This saves the locus name.
		# Rule = [excel column -1 : excel column]


		#print QlBy12_10minNaOCl_ampurebeads 						###CHECK THIS OUTPUT TO MAKE SURE YOU DID NOT FUCK UP!!

		#Geoje14
		Count_MissingGenotypesByLocus_Geoje14 = float(Geoje14.count("0"))
		NumberOf_Geoje14_individuals = float(len(Geoje14))
		Percent_MissingData_Geoje14 = float(Count_MissingGenotypesByLocus_Geoje14/NumberOf_Geoje14_individuals)

		if (Percent_MissingData_Geoje14  > 0.49):
			print "Geoje14 -- Fuck! missing data!"
			lostloci.write(mystring)
		else:
			#print "all good!"
			keptloci.write(mystring)

		#SocMuk
			keptloci.write(mystring)


# Close files

genfile.close()
keptloci.close()
lostloci.close()
