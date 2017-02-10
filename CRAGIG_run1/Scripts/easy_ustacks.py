##########################################################################################
#
### ``ustacks``
#
# PURPOSE: This step aligns identical RAD tags within an individual into stacks & provides data for calling SNPs
# INPUT: fastq or gzfastq files
# OUTPUT: 4 files - alleles, modules, snps, tags
#
#
### WHEN RUNNING THIS SCRIPT, YOUR INPUTS AT THE COMMAND LINE ARE:
# python
# {0}[pipeline filename]
# {1}[barcodes & samples textfile]
# {2}[start directory]
# {3}[end directory]
#
### DEPENDENCIES
#
# [1] You need a file where first column is barcode and second is unique sample name
#
### WARNINGS
#
# [1] ustacks only works when your working directory is one direcotry above the folders you are
#		calling and storing data in
#
##########################################################################################

# import modules
import sys
import subprocess
import time
import argparse

# organize parameter inputs with argparse
parser = argparse.ArgumentParser(description="Write and call a ustacks shell script, and plot results")
parser.add_argument("-t", "--type", help="input file type; supported types: fasta, fastq, gzfasta, gzfastsq", type=str, required = True)
parser.add_argument("-i", "--inputdir", help="relative path to directory with samples for ustacks", type=str, required=True)
parser.add_argument("-r", "--removal", help="enable the removal algorithm to drop highly-repetitive stacks", type=str)
parser.add_argument("-d", "--delever", help="enable the deleveraging algortih for resolving merged tags", type=str)
parser.add_argument("-o", "--out", help="output path to write results", type=str)
parser.add_argument("-m", "--mindepth", help="minimum depth of coverage required to create a stack; default 2", type=int)
parser.add_argument("-M", "--maxdis", help="maximum distance in nucleotides allowed between stacks", type=int)
parser.add_argument("-p", "--threads", help="allow parallel execution with p num threads", type=int)
parser.add_argument("-x", "--startID", help="starting number for SQL ID intger if not starting at 001", type=int)
parser.add_argument("-s", "--samples", help="text file with list of samples for ustacks, each on its own new line")
args = parser.parse_args()

### make lists of inputs that will go directly into stacks with same flags - here, all but --samples and --startID and --inputdir
stacksin = [args.type, args.output, args.mindepth, args.maxdis, args.threads]
stacksfl = ["-p", "-o", "-n", "m", "M", "p"]

### make list of flags that don't have parameter inputs, and list of flags; must match order
jflags_args = [args.removal, args.delever]
jflags = ["-r","-d"]

###  build a dictionary to store parameter inputs for those used here

inc_d = {} # initiate dictionary of included arguments
exc_d = {} # initatie dictionary to store excluded arguments

numpar = len(stacksin) # get number of total arguments

for i in range(0,numpar): # loop to sort arguments and input parameters for each dict
	if stacksin[i] == None:
		exc_d[stacksfl[i]] = stacksin[i]
	else:
		inc_d[stacksfl[i]] = stacksin[i]

### build a string with just flags used here
numjflags = len(jflags) # get length of total just flags

jflags_inc = []
jflags_exc = []

for i in range(0,numjflags):
	if jflags_args[i] == None:
		flags_exc.append(jflags[i])
	else:
		flags_inc.append(jflags[i])

### get sample names into list

samples = open(args.samples, "r")
lines = samples.readlines()

samples_for_use = []

for line in lines:
	name = line.strip()
	samples_for_use.append(name)
samples_file.close()

print samples_for_use












# dir = sys.argv[2] # directory files that need names changed
# firststr = "cd " + dir + "\n"
# new_file.write(firststr)

# dir2 = sys.argv[2] # directory with files that we want to run ustacks on
#
# ID_int = 001								# start integer counter
#
# lines = myfile.readlines()[2:] # skip first two lines because just cd and pwd

#
# ID_int = 001								# start integer counter
# for line in lines: 			#for each line in the barcode file
# 	linelist=line.strip().split()
# 	sampID = linelist[1] #save the second object as "sampID"
# 	if ID_int < 10:
# 		ustacks_code = "stacks ustacks -t gzfastq -f " + dirfrom + "/" + sampID + ".fq.gz" + " -r -d -o " + dirto + " -i 00" + str(ID_int) + " -m 10 -M 3 -p 10" + "\n"
# 								#create a line of code for ustacks that includes the new sample ID (with 2 leading 0s)
# 	elif ID_int >= 10 & ID_int < 100:
# 		ustacks_code = "stacks ustacks -t gzfastq -f " + dirfrom + "/" + sampID + ".fq.gz" + " -r -d -o " + dirto + " -i 0" + str(ID_int) + " -m 10 -M 3 -p 10" + "\n"
# 								#create a line of code for ustacks that includes the new sample ID (with 1 leading 0)
# 	else:
# 		ustacks_code = "stacks ustacks -t gzfastq -f " + dirfrom + "/" + sampID + ".fq.gz" +" -r -d -o " + dirto + " -i " + str(ID_int) + " -m 10 -M 3 -p 10" + "\n"
# 								#create a line of code for ustacks that includes the new sample ID (with no leading 0s)
# 	newfile2.write(ustacks_code)	#append this new line of code to the output file
# 	ID_int += 1

##########################################################################################
