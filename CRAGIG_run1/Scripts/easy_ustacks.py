##########################################################################################
### ``ustacks``




# Assumptions: order of samples in sample list and barcode list is identical; lengths of two lists identical
#
##########################################################################################

# import modules
import sys
import subprocess
import time
import argparse
import numpy

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

#subprocess.call(["sh ustacks_shell.txt"], shell = True)

### time the subprocess

end = time.time()

print "\nRunning ustacks took "
timer(start,end)

### plotting results

## (1) get counts of unique loci per tags file using Eleni's bash command and order of samples

countbash = ""
firststr = "cd " + args.out + "\n"
countbash += firststr

populations = []
samples_in_popmap = []

popmap = open(args.popmap, "r")
for line in popmap:
	linelist = line.strip().split()
	sample_popord = linelist[0]
	samples_in_popmap.append(sample_popord)
	pop = linelist[1]
	populations.append(pop)

for sample in samples_in_popmap:
	countstring = "grep --count --with-filename consensus " + sample + ".tags.tsv > " + args.count + "/n"
	countbash += countstring
subprocess.call([countbash], shell = True)

## (2) read file back in

countresults = open(args.count, "r")
lines = countresults.readlines()
counts = []
for line in lines:
	linelist = line.strip().split(":")
	count = linelist[1]
	counts.append(count)
countresults.close()

## (3) make dataframe with population

populations = []

popmap = open(args.popmap, "r")
for line in popmap:
	linelist = line.strip().split()
	pop = linelist[1]
	populations.append(pop)

df = pd.DataFrame(
    {'Population':populations,
     'Counts':counts}
)

print df









#########################################################################################
