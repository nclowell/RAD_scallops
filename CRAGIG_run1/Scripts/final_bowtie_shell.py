##########################################################################################
#
###--- ``final bowtie`` script
#
# PURPOSE: align fastq files to bowtie index to feed into pstacks
# INPUT: bowtie index and fasta files of sequences to align
# OUTPUT: SAM alignment
#
#### WHEN RUNNING THIS SCRIPT, INPUTS AT THE COMMAND LINE ARE:
# python
# {0}[pypipe_pstacks.py]
# {1}[file with fastq filenames, here prt_out_filenames.txt]
# {2}[bowtie index name, e.g., batch_100_final_index.]
### DEPENDENCIES:
# [1] you want a SAM file without the header line
# [2] you're reading in fastq files
#
### WARNINGS:
# [1]
#
##########################################################################################

import sys
import subprocess
import time

namelist = [] # for counting how many names we have
filenames = open(sys.argv[1], "r")
for line in filenames:					# loop that gets file names out of a text file, separated by comma with no spaces
	name = line.strip()
	namelist.append(name)
filenames.close()

namelist_len = len(namelist)
print "You are working with " + str(namelist_len) + " files. Consider checking your code if you expected a different number of files." # print notice of how many filenames you counted, just to verify.

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

bashstring = ""

print namelist

for name in namelist:
	stringforfile = "bowtie -q -v 3 --norc --sam Blast/" + sys.argv[2] +  " Stacks/" + name + ".fq " + "Stacks/" + name + ".sam" + "\n"# write string for shell script
	bashstring += stringforfile

final_bowtie_shell = open("final_bowtie_shell.txt", "w") # open new file for writing shell script
final_bowtie_shell.write(bashstring)
final_bowtie_shell.close()

print "Your bash script looks like this: \n"
print bashstring

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

subprocess.call(["sh final_bowtie_shell.txt"], shell = True) # run shell script

end = time.time() # get end time

print "\nRunning bowtie took "
timer(start,end) # report time
