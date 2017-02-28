#!/bin/bash

### This shell script will unzip all of the individual .tags.tsv files needed for Marine Brieuc's genotypes_verif.py script, then call Marine's python script. Use this bash script AFTER running Marine's script `preparing_file_for_correcting_genotypes.py` ###

## M. Fisher 12/5/2016


#Ask for input from user
echo "This is your current location:"
pwd
echo "Please input the local path to the directory containing the individual 'tags' and 'matches' files"
read DIRECTORY


#(1) Navigate to directory with .tags.tsv files
cd $DIRECTORY
pwd
echo "--"

#(2) find all files that end in .tags.tsv.gz
echo "finding all gzipped 'tags' files"
tags_file_array="$(find . -name "*.tags.tsv.gz")"

#(2a) find all files that end in .matches.tsv.gz
echo "finding all gzipped 'matches' files"
matches_file_array="$(find . -name "*.matches.tsv.gz")"


#(3) unzip each "tags" file
echo "unzipping all 'tags' files"
for file in $tags_file_array
do
	echo $file
	gzip -d $file
	echo "file unzipped"
done

#(3a) unzip each "matches" file
echo "unzipping all 'matches' files"
for file in $matches_file_array
do
	echo $file
	gzip -d $file
	echo "file unzipped"
done


#(4) call Marine's script

echo "Make sure that you have the correct ABSOLUTE file paths and stack depth for the genotypes_verif_v2_noref.py script!! Type 'Yes' when ready"
read YES

echo "This is your current location:"
pwd
echo "Please input the local path to the directory containing the genotypes_verif_v2_noref.py script"
read MBSCRIPT_PATH

cd $MBSCRIPT_PATH
pwd
python genotypes_verif_v2_no_ref_12-7.py

