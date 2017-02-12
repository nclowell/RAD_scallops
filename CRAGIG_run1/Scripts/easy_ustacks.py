##########################################################################################
### ``easy ustacks``
#
# 20170212 NL
#
# purpose of ``easy ustacks``: writes a bash script to run ustacks, executes bash script, counts retained loci after ustacks, plots retained loci
# purpose of ustacks: align sequences to matching stacks within an individual to form set of loci and detect SNPs
#
# inputs via argparse: file type, input directory, removal algorithm, develeraging algorithm,
#						output directory, min depth, max distance, num threads, start ID, samples
#						name for counts file, pop map with only samples in this ustacks run
#
# outputs: tags, SNPs, and alleles files per sample and plot of retained loci per individual per population
#
# assumptions: pop map only includes the samples you want to run ustacks on
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

# make lists of inputs that will go directly into stacks with same flags - here, all but --samples and --startID and --inputdir
stacksin = [args.type, args.out, args.mindepth, args.maxdis, args.threads]
stacksfl = ["-t", "-o", "-m", "-M", "-p"]

# make list of flags that don't have parameter inputs, and list of flags; must match order
jflags_args = [args.removal, args.delever]
jflags = ["-r","-d"]

#  build a dictionary to store parameter inputs for those used here
inc_d = {} # initiate dictionary of included arguments
exc_d = {} # initatie dictionary to store excluded arguments

numpar = len(stacksin) # get number of total arguments

for i in range(0,numpar): # loop to sort arguments and input parameters for each dict
	if stacksin[i] == None:
		exc_d[stacksfl[i]] = stacksin[i]
	else:
		inc_d[stacksfl[i]] = stacksin[i]

# build a string with just flags used here
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


# get list of population labels and list of samples in population map order
populations = []
samples_in_poporder = []

popmap = open(args.popmap, "r")
for line in popmap:
	linelist = line.strip().split()
	sample_popord = linelist[0]
	samples_in_poporder.append(sample_popord)
	pop = linelist[1]
	populations.append(pop)
popmap.close()
numsamples = len(samples_in_poporder) # get number of samples in ustacks run

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
	linestr += "-s " + args.inputdir + "/" + samples_in_poporder[i] + ".fq.gz" + " "
	linestr += "-i " + str(IDs[i]) + " "
	for key, value in inc_d.iteritems():
		linestr += str(key) + " " + str(value) + " "
	linestr += string_flags
	ustacks_shell_str += linestr + "/n"

print "Your ustacks shell script looks like this: \n" # show the user the bash script
print ustacks_shell_str

# ask user if script okay and whether to proceed after seeing bash script printed to screen
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

### time running of ustacks

# write timing function
def timer(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

start = time.time() # get start time

### run the bash script
# subprocess.call(["sh ustacks_shell.txt"], shell = True)

end = time.time() # get end time

print "\nRunning ustacks took "
timer(start,end) # report time

### plotting results

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
	countstring = "grep --count --with-filename consensus " + sample + ".tags.tsv >> " + args.count + "/n"
	countbash += countstring

# run counting bash script
subprocess.call([countbash], shell = True)

# read results in
countresults = open(args.count, "r")
lines = countresults.readlines()
counts = []
for line in lines:
	linelist = line.strip().split(":")
	count = int(linelist[1])
	counts.append(count)
countresults.close()

# verify length of populations, counts, and samples all same length; otherwise something's wrong
length1 = len(populations)
length2 = len(samples_in_poporder)
length3 = len(counts)

if length1 == length2 == length3:
	print "Number of populations, counts, and samples equal. Continuing to plot."
else:
	print "The length of your population, counts, and samples lists are not equal. Check your code and files. Program will quit."
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

# plot with matplotlib pyplot
plt.boxplot(data_array) # multiple box plots with list of lists
plt.xticks(range(1,num_set_pops+1),set_pops) # label x axis with population names
plt.ylabel('Number of loci retained per individual') # axis label
plt.suptitle('Retained loci by population after ustacks') # title
plt.show() # show plot

################################################################################
