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

# --- [A] call necessary modules

import subprocess
import sys

### --- [C] Make shell script to run all samples through command line through ``ustacks``

# ``ustacks`` requires an arbitrary integer for every sample, although unclear how it gets used as it does not become the name of the file


# name your 'from' and 'to' directories that will go in each line of your ustacks shell script
dirfrom = sys.argv[2]
dirto = sys.argv[3]

newfile2 = open("ustacks_shell.txt", "w")	 # make ustacks shell script to run through terminal
myfile = open(sys.argv[1], "r")	#open the file with a list of barcodes + sample IDs

# dir = sys.argv[2] # directory files that need names changed
# firststr = "cd " + dir + "\n"
# new_file.write(firststr)

dir2 = sys.argv[2] # directory with files that we want to run ustacks on

ID_int = 001								# start integer counter

lines = myfile.readlines()[2:] # skip first two lines because just cd and pwd


ID_int = 001								# start integer counter
for line in lines: 			#for each line in the barcode file
	linelist=line.strip().split()
	sampID = linelist[1] #save the second object as "sampID"
	if ID_int < 10:
		ustacks_code = "stacks ustacks -t gzfastq -f " + dirfrom + "/" + sampID + ".fq.gz" + " -r -d -o " + dirto + " -i 00" + str(ID_int) + " -m 10 -M 3 -p 10" + "\n"
								#create a line of code for ustacks that includes the new sample ID (with 2 leading 0s)
	elif ID_int >= 10 & ID_int < 100:
		ustacks_code = "stacks ustacks -t gzfastq -f " + dirfrom + "/" + sampID + ".fq.gz" + " -r -d -o " + dirto + " -i 0" + str(ID_int) + " -m 10 -M 3 -p 10" + "\n"
								#create a line of code for ustacks that includes the new sample ID (with 1 leading 0)
	else:
		ustacks_code = "stacks ustacks -t gzfastq -f " + dirfrom + "/" + sampID + ".fq.gz" +" -r -d -o " + dirto + " -i " + str(ID_int) + " -m 10 -M 3 -p 10" + "\n"
								#create a line of code for ustacks that includes the new sample ID (with no leading 0s)
	newfile2.write(ustacks_code)	#append this new line of code to the output file
	ID_int += 1

myfile.close()
newfile2.close()

# run this new script through the terminal
subprocess.call(['sh ustacks_shell.txt'], shell=True)

##########################################################################################
