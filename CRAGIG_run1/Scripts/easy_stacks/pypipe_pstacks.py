################################# EASY PSTACKS #################################
# 20170327 NL
# PURPOSE: write and execute a bash script to run pstacks, then count and plot retained loci after pstacks
# INPUT: managed by argparse below, includes:
# - file type
# -input directory
# - output directory
# - min depth
# - num threads
# - start ID
# - samples
# - name for counts file
# - pop map with only samples in this ustacks run
#
# OUTPUT: tags, SNPs, and alleles files per sample and plot of retained loci per individual per population, plot of retained loci per population
# ASSUMPTIONS: population map only includes the samples you want to run pstacks on
##########################################################################################

import sys
import argparse
import subprocess
import time

# organize parameter inputs with argparse
parser = argparse.ArgumentParser(description="Write and call a pstacks shell script, and plot results")
parser.add_argument("-t", "--type", help="input file type; supported types: bam, sam, bowtie", type=str, required = True)
parser.add_argument("-i", "--inputdir", help="relative path to directory with samples for ustacks", type=str, required=True)
parser.add_argument("-o", "--out", help="output path to write results", type=str)
parser.add_argument("-m", "--mindepth", help="minimum depth of coverage required to create a stack; default 3", type=int)
parser.add_argument("-s", "--samples", help="text file with names of each sample to include in pstacks on its own line and without file extension", type=str, required=True)
parser.add_argument("-p", "--threads", help="allow parallel execution with p num threads", type=int)
parser.add_argument("-x", "--startID", help="starting number for SQL ID intger if not starting at 001", type=int)
parser.add_argument("-c", "--count", help="name of text file that will store unique loci count data", type=str, required=True)
parser.add_argument("-P", "--popmap", help="population map", type=str)
args = parser.parse_args()

# get sample names
samplelist = []
samples = open(args.samples, "r")
for line in samples:
	sample = line.strip()
	namelist.append(sample)
samples.close()

# make a recursive function that asks the user for input
def simple_getinput(prompt, YES_string, NO_string, else_string):
	answer = raw_input(prompt)
	if answer == "YES":
		print YES_string
	elif answer == "NO":
		sys.exit(NO_string)
	else:
		print else_string
		simple_getinput(prompt, YES_string, NO_string, else_string)

# verify to user that you have the right number of samples using above function
numsamples = len(samplelist)
print "\nYou are working with " + str(numsamples) + " samples."

prompt = "\nType YES if correct. Type NO if incorrect and check your files and code."
YES_string = "\nSample number verified. Program continuing."
NO_string = "\nRuh-roh. Something's wrong. Check your files and verify they match your expectations."
else_string = "\nYour answer is not a valid input. Only YES and NO are valid inputs."
simple_getinput(prompt, YES_string, NO_string, else_string)






string = ""

IDs = range(1,72)
print IDs
print str(len(IDs)) + " in list IDs"

for i in range(0,71):
	substring = "stacks pstacks -p 5 -m 10 -t sam -i " + str(IDs[i]) + " -f Stacks/" + namelist[i] + ".sam " + "-o Stacks" + "\n"
	string += substring

pstacks_shell = open("pstacks_shell.txt", "w")
pstacks_shell.write(string)
pstacks_shell.close()

print "Your pstacks shell looks like this: \n"
print string

def simple_getinput(prompt, YES_string, NO_string, else_string):
	answer = raw_input(prompt)
	if answer == "YES":
		print YES_string
	elif answer == "NO":
		sys.exit(NO_string)
	else:
		print else_string
		simple_getinput(prompt, YES_string, NO_string, else_string)

prompt = "\nType YES if correct. Type NO if incorrect and check your code."
YES_string = "\nScript verified. Program continuing."
NO_string = "\nRuh-roh. Something's wrong. Check your code and verify it matches your expectations."
else_string = "\nYour answer is not a valid input. Only YES and NO are valid inputs."
simple_getinput(prompt, YES_string, NO_string, else_string)

# write timing function
def timer(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

start = time.time() # get start time

subprocess.call(["sh pstacks_shell.txt"], shell = True)
print "Finished running pstacks_shell.txt script."

end = time.time() # get end time

print "\nRunning pstacks took "
timer(start,end) # report time
