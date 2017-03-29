# ``easy_pstacks.py``

### What is ``pstacks``?
``pstacks`` is a program in the Stacks pipeline that uses alignments to identify putative loci and detect SNPs using a maximum likelihood framework. It is the alternative to ``ustacks`` when using a reference genome.

### What does ``easy_pstacks.py`` do?
The ``easy_pstacks.py`` script writes and executes a ``pstacks`` bash script to run the program on a set of samples, then counts and plots the number of retained loci per individual.

### What inputs does ``easy_pstacks.py`` take?

Inputs include the following input parameters to ``ustacks``:
* ``-t`` for file type: sam, bam
* ``-o`` for output path to write results
* ``-m`` for minimum depth of coverage
* ``-p`` for number of threads

Additional inputs include:
* ``-i`` for relative path to directory with individual sequence files
* ``-c`` for the name to give the file with counts of loci
* ``-P`` for the population map including only samples you want to run through ``ustacks``
* ``-x`` for the starting number for SQL ID, if not starting at 001

You can access the help file by running the script with the flag `` -h``, which lists these inputs, and to see which are optional.

### What outputs does ``easy_pstacks.py`` make?

Individual tags, alleles, and snps files are created when the script runs ``pstacks``. In addition, the script will produce a text file with counts of loci per individual, and a plot of retained loci per population.

### How does ``easy_pstacks.py`` work?

#### Running ``pstacks``
The script builds a dictionary, pairing flags with values, e.g., ``dictionary["-m"] = "10"`` for stack depth m of 10. The script then writes and calls a ``pstacks`` bash script for all individuals based on their order in the population map. The script times how long it takes to run the ``pstacks`` bash script, and reports it to the user.

#### Counting and plotting retained loci
The script uses a grep command, counting every time the word "consensus" appears in the individual tags.tsv files produced by ``pstacks``, as these denote unique loci and writes them to a file. The file is called back in, parsed, and plotted by population. X axis labels are population names from your population map.

**20170329 Natalie Lowell**
