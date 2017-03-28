############################### EASY CSTACKS ###################################
# 20170203 Natalie Lowell
# PURPOSE: to produce and run a shell script for cstacks; cstacks builds a catalog of loci that you use to genotype your individuals
# INPUT: managed with argparse, includes:
# -num threads
# -batch number
# -text file with sample names each on own line, without file extension
# -directory for output files
# -include tags in the catalog that match to more than one entry
# -number of mismatches allowed between sample tags when generating the catalog
# -whether to base catalog construction on alignment position and not sequence identity
# OUTPUT: catalog file you can use to genotype individuals
# ASSUMPTIONS:
# -----------------------------------------------------------------------------

# import modules
import sys
import subprocess
import time
import argparse

# organize parameter inputs with argparse
parser = argparse.ArgumentParser(description="Write and call a cstacks shell script")
parser.add_argument("-p", "--threads", help="enable parallel execution with num_threads threads", type=int)
parser.add_argument("-b", "--batch", help="batch number", type=str, required=True)
parser.add_argument("-s", "--samples", help="text file with names of each sample to include in cstacks on its own line and without file extension", type=str, required=True)
parser.add_argument("-o", "--output", help="output path to write results", type=str, required=True)
parser.add_argument("-n", "--mismatch", help="number of mismatches allowed between sample tags when generating the catalog; only use when running cstacks without a reference genome.", type=str, required=False)
parser.add_argument("-i", "--input", help="relative path to directory with input sample files", type=str, required=True)
parser.add_argument("-g", "--genome", help ="base catalog construction on alignment position, not sequence identity", action='store_true')
args = parser.parse_args()

# make lists of required inputs that will go directly into stacks with same flags
stacksin = [args.threads, args.output]
stacksfl = ["-p", "-o"]
inc_d = {}
exc_d = {}
numpar = len(stacksin)

for i in range(0,numpar):
	if stacksin[i] == None:
		exc_d[stacksfl[i]] = stacksin[i]
	else:
		inc_d[stacksfl[i]] = stacksin[i]

for i in inc_d:
    print i, inc_d[i]

# optional argument string that will occur after sample list

if args.mismatch != None and args.genome == True:
	print "You gave both a mismatch value, and the matching by genome alignment flag, which are mutually exclusive. Script quitting."
	sys.exit()

opt_str = ""
if args.mismatch == None:
	opt_str = opt_str
else:
	opt_str += " -n " + str(args.mismatch) + " "
if args.genome == True:
	opt_str += " -g "

# get sample names from text file in -s
samples_file = open(args.samples, "r")
samples_file_lines = samples_file.readlines()

samples_for_use = []

for line in samples_file_lines:
	name = line.strip()
	samples_for_use.append(name)
samples_file.close()

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

# verify to user that the program is running on the appropriate number of samples using recursive function
numsamples = len(samples_for_use)
print "\n" + "Currently, this program thinks you intend to include " + str(numsamples) + " samples in cstacks."

prompt = "\nType YES if correct. Type NO if incorrect and check your files and code."
YES_string = "\nSample number verified. Program continuing."
NO_string = "\nRuh-roh. Something's wrong. Check your files and verify they match your expectations."
else_string = "\nYour answer is not a valid input. Only YES and NO are valid inputs."
simple_getinput(prompt, YES_string, NO_string, else_string)

# write cstacks shell script
cstacks_shell = ""
firststr = "stacks cstacks -b " + str(args.batch) + " "
cstacks_shell += firststr
sampstr = ""
sampstr += opt_str
for i in range(0,numsamples):
	sampstr += "-s " + args.input + "/" + samples_for_use[i] + " "
cstacks_shell +=sampstr
endstr = ""
for key, value in inc_d.iteritems():
	endstr += str(key) + " " + str(value) + " "
cstacks_shell +=endstr

cstacks_shell_txt = open("cstacks_shell.txt", "w") # open new text file for cstacks shell
cstacks_shell_txt.write(cstacks_shell) # write to file
cstacks_shell_txt.close() # close file

print "\nFinished writing cstacks shell script."
print "\nThis is what your cstacks shell looks like."
print cstacks_shell

prompt = "Run this shell script?"
YES_string = "Running shell script."
NO_string = "You identiifed something wrong with the shell script, so the easy cstacks program will not continue."
else_string = "Not a valid input. Only YES and NO are valid inputs."
simple_getinput(prompt, YES_string, NO_string, else_string)

# define timer function
def timer(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

start_time = time.time()

# run shell script
# subprocess.call(["sh cstacks_shell.txt"], shell = True)

end_time = time.time()
print "\nRunning cstacks took " # report time to user
timer(start_time, end_time)
