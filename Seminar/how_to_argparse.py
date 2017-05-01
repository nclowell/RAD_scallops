############# HOW TO USE ARGPARSE #################

# first import the module
import argparse

# Make a parser object, which allows you to provide a description of your
# script/program and defines the group of arguments.
parser = argparse.ArgumentParser(description="A script to explain how argparse works")

# Then, you add arguments using .add_argument(). You can tell the argument
# parser the type of object your input will be, with str, int, float, etc.
# You can also include a brief help string that will describe the argument.
# Later, these strings will automatically be organized into a help file.
parser.add_argument("-n", "--noun", help="A noun for your example sentence, e.g., 'dog'", type=str, required=True)
parser.add_argument("-v", "--verb", help="A verb for your example sentence, e.g., 'walk'", type=str, required=True)
parser.add_argument("-a", "--adjective", help="An adjective for your example sentence, e.g., 'fluffy'", type=str, required=True)
parser.add_argument("-p", "--punctuation", help="Punctuation for the end of your example sentence, e.g., '!!'; default = '!'", type=str, required=False)
parser.add_argument("-x", "--num1", help="A first integer to multiply to show you how argparse can take numbers", type=int, required=True)
parser.add_argument("-y", "--num2", help="A second integer to multiply to show you how argparse can take numbers", type=int, required=True)

# You can also add optional arguments, that don't have input values
parser.add_argument("-m", "--muahaha", help="Add evil muahaha to end of sentence.", action='store_true')

# Define args, which is the class that defines your arguments.
# E.g., now you can can your arguments with args.noun, or args.verb
args = parser.parse_args()

# Assign any default values with simple loops
punctuation = ""
if args.punctuation == None:
    punctuation += "!"
else:
    punctuation += args.punctuation

# Assign optional arguments with similar loop
endstring = ""
if args.muahaha == True:
    endstring += " Muahaha!"

# Assemble sentence and print
sentence = "The " + args.adjective + " " + args.noun + " will " + args.verb + args.punctuation + endstring
print sentence

# Calculate result and print
result = args.num1*args.num2
print "Multiplying " + str(args.num1) + " and " + str(args.num2) + " gets you "+ str(result)
