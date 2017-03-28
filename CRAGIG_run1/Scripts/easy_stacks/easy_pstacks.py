################################# EASY PSTACKS #################################
# 20170327 NL
# PURPOSE: write and execute a bash script to run pstacks, then count and plot retained loci after pstacks
# INPUT: managed by argparse below, includes:
# - file type
# - input directory
# - output directory
# - min depth
# - num threads
# - start ID
# - samples
# - name for counts file
# - pop map with only samples in this pstacks run
#
# OUTPUT: tags, SNPs, and alleles files per sample and plot of retained loci per individual per population, plot of retained loci per population
# ASSUMPTIONS: population map only includes the samples you want to run pstacks on, only allows SAM and BAM alignments
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
parser.add_argument("-P", "--popmap", help="population map, with only the samples you want to run sstacks on", type=str, required=True)
args = parser.parse_args()

# get sample names
samplelist = []
samples = open(args.popmap, "r")
for line in samples:
	linelist = line.strip().split()
	sample = linelist[0]
	samplelist.append(sample)
samples.close()

# get file extension
file_ext = ""
if args.type == "bam":
	file_ext += ".bam"
elif args.type == "sam":
	file_ext += ".sam"
else:
	print "\nError in your alignment file type. Quitting script."
	sys.exit()

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

### organize arguments and inputs for bash script with dictionary to loop through

# lists of inputs that match Stacks inputs and their flags
stacksin = [args.threads, args.mindepth, args.out, args.type]
stacksfl = ["-p", "-m", "-o", "-t"]

inc_d = {} # initialize dictionary with parameters to include in this script
exc_d = {} # initilize dictionary to store parameters that won't be included in script

numpar = len(stacksin) # get number of parameters to include

for i in range(0,numpar): # sort each arg and its parameter into the appropriate dictionary
	if stacksin[i] == None:
		exc_d[stacksfl[i]] = stacksin[i]
	else:
		inc_d[stacksfl[i]] = stacksin[i]

# get ID nums
start_ID = [] # set starting point at 1 if default or at specified starting point
if args.startID == None:
	start_ID.append(0)
else:
	start_ID.append(args.startID)

start_int = int(start_ID[0])
IDs = range(start_int,(start_int+numsamples))

# write bash script to run pstacks
shellfile = open("pstacks_shell.txt", "w") # create new file for shell script
shellstring = ""

# write pstacks shell script, example line:"stacks pstacks -p 5 -m 10 -t sam -i 1 -f Stacks/Q351.sam -o Stacks"
for i in range(0,numsamples):
	firststring = "stacks pstacks " + args.inputdir + "/" + str(samplelist[i]) + file_ext + " " + "-i " + str(IDs[i]) + " "
	secondstring = ""
	for key, value in inc_d.iteritems():
		secondstring += str(key) + " " + str(value) + " "
	linestring = firststring + secondstring
	shellstring += linestring + "\n"
shellfile.write(shellstring)
shellfile.close()

# let the user know the script is done
print "\nFinished writing pstacks shell script. This is what it looks like:"
print "\n" + shellstring + "\n"

prompt = "\nRun this pstacks shell script?"
YES_string = "\nRunning script."
NO_string = "\nWill not run script. Program discontinued."
else_string = "\nYour answer is not a valid input. Only YES and NO are valid inputs."
simple_getinput(prompt, YES_string, NO_string, else_string)

# write timer function
def timer(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

start = start_time = time.time()

# run pstacks shell script
subprocess.call(["sh pstacks_shell.txt"], shell=True)

end = time.time()
print "\nRunning pstacks took:" # report time to run pstacks
timer(start,end)

### plot results

# get counts of unique loci per tags file using Eleni's bash command and order of samples
countbash = ""
firststr = "cd " + args.out + "\n"
countbash += firststr

populations = []
samples_in_poporder = []

popmap = open(args.popmap, "r")
for line in popmap:
	linelist = line.strip().split()
	sample_popord = linelist[0]
	samples_in_poporder.append(sample_popord)
	pop = linelist[1]
	populations.append(pop)

for sample in samples_in_poporder:
	countstring = "zgrep --count --with-filename consensus " + sample + ".tags.tsv >> " + args.count + "\n"
	countbash += countstring

print countbash

# run counting bash script
subprocess.call([countbash], shell = True)

# read results in
countresults = open(args.out + "/" + args.count, "r")
lines = countresults.readlines()
counts = []
for line in lines:
	linelist = line.strip().split(":")
	count = int(linelist[1])
	counts.append(count)
countresults.close()

# verify length of populations, counts, and samples all same length; otherwise something's wrong
length2 = len(samples_in_poporder)
length3 = len(counts)

if length2 == length3:
	print "Continuing to plot."
else:
	print "There was a mismatch between the number of tags files counted, and the number of tags files produced by ustacks. Check your code and files, and double-check that counts aren't appending to an existing file. Program will quit."
	print "\nTo help you debug..."
	print "Samples in popmap order list length: " + str(length2)
	print "Count list length: " + str(length3)
	sys.exit()

# get list of list where each sublist is a unique pop with list of counts
data_array = []

set_pops = list(set(populations)) # get unique pops from pops factor list
num_set_pops = len(set_pops) # get num pops

for pop in set_pops:
	indeces = [i for i, x in enumerate(populations) if x == pop] # collect indeces of one list when value matches in second list
	matches = []
	for i in indeces:
		matches.append(counts[i]) # get counts with those matching indeces and put in list
	data_array.append(matches) # append list within bigger list for plotting

# plot
plt.boxplot(data_array) # multiple box plots with list of lists
plt.xticks(range(1,num_set_pops+1),set_pops) # label x axis with population names
plt.ylabel('Number of loci retained per individual') # axis label
plt.suptitle('Retained loci by population after pstacks') # title
plt.show() # show plot

################################################################################



###############################################################################
