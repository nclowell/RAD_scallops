##########################################################################################
### ``easy ustacks``
#
# purpose: writes a bash script to run ustacks, executes bash script, counts retained loci after ustacks, plots retained loci
#
# inputs via argparse: file type, input directory, removal algorithm, develeraging algorithm,
#						output directory, min depth, max distance, num threads, start ID, samples
#						name for counts file, pop map with only samples in this ustacks run
#
# outputs: tags, snps, and alleles files per sample and plot of retained loci per individual per population

# Assumptions: order of samples in sample list and barcode list is identical; lengths of two lists identical
#
##########################################################################################

# import modules
import sys
import subprocess
import time
import argparse
import matplotlib.pyplot as plt

# organize parameter inputs with argparse
parser = argparse.ArgumentParser(description="Write and call a ustacks shell script, and plot results")
parser.add_argument("-t", "--type", help="input file type; supported types: fasta, fastq, gzfasta, gzfastsq", type=str, required = True)
parser.add_argument("-i", "--inputdir", help="relative path to directory with samples for ustacks", type=str, required=True)
parser.add_argument("-r", "--removal", help="enable the removal algorithm to drop highly-repetitive stacks", action='store_true')
parser.add_argument("-d", "--delever", help="enable the deleveraging algortih for resolving merged tags", action='store_true')
parser.add_argument("-o", "--out", help="output path to write results", type=str)
parser.add_argument("-m", "--mindepth", help="minimum depth of coverage required to create a stack; default 2", type=int)
parser.add_argument("-M", "--maxdis", help="maximum distance in nucleotides allowed between stacks", type=int)
parser.add_argument("-p", "--threads", help="allow parallel execution with p num threads", type=int)
parser.add_argument("-x", "--startID", help="starting number for SQL ID intger if not starting at 001", type=int)
parser.add_argument("-s", "--samples", help="text file with list of samples for ustacks, each on its own new line")
parser.add_argument("-c", "--count", help="name of text file that will store unique loci count data", type=str, required=True)
parser.add_argument("-P", "--popmap", help="population map", type=str)

args = parser.parse_args()


### make lists of inputs that will go directly into stacks with same flags - here, all but --samples and --startID and --inputdir
stacksin = [args.type, args.out, args.mindepth, args.maxdis, args.threads]
stacksfl = ["-t", "-o", "-m", "-M", "-p"]

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
	if jflags_args[i] == False:
		jflags_exc.append(jflags[i])
	else:
		jflags_inc.append(jflags[i])

string_flags = ""
for item in jflags_inc:
	string_flags += item + " "
print string_flags

### get sample names into list

samples = open(args.samples, "r") # open file with samle names for reading
lines = samples.readlines() # get lines in the file

samples_for_use = [] # iniate list for sample names

for line in lines: # loop over names, remove white space, store in list
	name = line.strip()
	samples_for_use.append(name)
samples.close() # close file

numsamples = len(samples_for_use) # get number of samples in ustacks run

start_ID = [] # set starting point at 1 if default or at specified starting point
if args.startID == None:
	start_ID.append(0)
else:
	start_ID.append(args.startID)

start_int = int(start_ID[0])
IDs = range(start_int,(start_int+numsamples))

### write ustacks shell string

ustacks_shell_str = "" # initialize string to write as shell script
for i in range(0,numsamples):
	linestr = "stacks ustacks "
	linestr += "-s " + args.inputdir + "/" + samples_for_use[i] + ".fq.gz" + " "
	linestr += "-i " + str(IDs[i]) + " "
	for key, value in inc_d.iteritems():
		linestr += str(key) + " " + str(value) + " "
	linestr += string_flags
	ustacks_shell_str += linestr + "/n"


print "Your ustacks shell script looks like this: \n" # show the user the bash script
print ustacks_shell_str

### ask user if okay and whether to proceed after seeing bash script printed to screen

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

### define function for timing bash script subprocess

def timer(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

start = time.time()

### run the bash script

subprocess.call(["sh ustacks_shell.txt"], shell = True)

### time the subprocess

end = time.time()

print "\nRunning ustacks took "
timer(start,end)

### plotting results

# (1) get counts of unique loci per tags file using Eleni's bash command and order of samples

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
	countstring = "grep --count --with-filename consensus " + sample + ".tags.tsv >> " + args.count + "/n"
	countbash += countstring
subprocess.call([countbash], shell = True)

# (2) read file back in

countresults = open(args.count, "r")
lines = countresults.readlines()
counts = []
for line in lines:
	linelist = line.strip().split(":")
	count = int(linelist[1])
	counts.append(count)
countresults.close()

print "look here:"
print counts

# (3) verify length of populations, counts, and samples all same length

length1 = len(populations)
length2 = len(samples_in_poporder)
length3 = len(counts)

if length1 == length2 == length3:
	print "Number of populations, counts, and samples equal. Continuing to plot."
else:
	print "The length of your population, counts, and samples lists are not equal. Check your code and files. Program will quit."
	sys.exit()

#

pops_set = set(populations)

data_array = []

set_pops = list(set(populations))
num_set_pops = len(set_pops)

print set_pops # looks like ['CA', 'AK', 'WA']

for pop in set_pops:
	indeces = [i for i, x in enumerate(populations) if x == pop]
	matches = []
	for i in indeces:
		matches.append(counts[i])
	data_array.append(matches)

print data_array

plt.boxplot(data_array)
plt.xticks(range(1,num_set_pops+1),set_pops)
plt.ylabel('Number of loci retained per individual')
plt.suptitle('Retained loci by population after ustacks')
plt.show()




#########################################################################################
