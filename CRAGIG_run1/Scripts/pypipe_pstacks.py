##########################################################################################
#
###--- ``pstacks`` script
#
# PURPOSE: similar to ustacks, except extracts stacks that have been aligned to a genome
# INPUT: either SAM or bowtie reference genome
# OUTPUT: tags, snps, and alleles files like ustacks
#
#### WHEN RUNNING THIS SCRIPT, INPUTS AT THE COMMAND LINE ARE:
# python
# {0}[pypipe_pstacks.py]
# {1}[text file with names of SAM files to run pstacks, each on its own new line
#
### DEPENDENCIES:
# [1]
#
### WARNINGS:
# [1]
#
##########################################################################################


import sys
import subprocess

namelist = []

names = open(sys.argv[1], "r")
for line in names:
	name = line.strip()
	namelist.append(name)

names.close()

string = ""

# example text from Eleni's code
# pstacks -p 8 -t sam -f ./aligned/exp1_dam.sam -o ./stacks -i 1 -m 3

IDs = range(0,71)

for i in enumerate(namelist):
	string += "stacks pstacks -p 5 -m 10 -t sam -i" IDs[i] + " -f " + namelist[i] + ".sam " + " -o Stacks" + "\n"
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

# subprocess.call(["sh pstacks_shell.txt"], shell = True)

print "Finished running pstacks_shell.txt script."

end = time.time() # get end time

print "\nRunning pstacks took "
timer(start,end) # report time
