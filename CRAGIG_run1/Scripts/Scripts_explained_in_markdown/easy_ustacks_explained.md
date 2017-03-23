# ``easy_ustacks.py``

### What is ``ustacks``?
``ustacks`` is a program in the Stacks pipeline that aligns individual sequence reads into "stacks," in order to identify putative loci and detect SNPs using a maximum likelihood framework.

### What does ``easy_ustacks.py`` do?
The ``easy_ustacks.py`` script writes and executes a ``ustacks`` bash script to run the program on a set of samples, then counts and plots the number of retained loci per individual.

### What inputs does ``easy_ustacks.py`` take?

Inputs include the following input parameters to ``ustacks``:
* ``-t`` for file type: fasta, fastq, gzfasta, gzfastq
* ``-r`` for enabling the removal algortihm to drop highly-repetitive stacks
* ``-d`` for enabling the deleveraging algorithm for resolving merged tags
* ``-o`` for output path to write results
* ``-m`` for minimum depth of coverage
* ``-M`` for number of mismatches allowed between stacks
* ``-p`` for number of threads

Additional inputs include:
* ``-i`` for relative path to directory with individual sequence files
* ``-c`` for the name to give the file with counts of loci
* ``-P`` for the population map including only samples you want to run through ``ustacks``

You can access the help file by running the script with the flag `` -h``, which lists these inputs, and to see which are optional.

### What outputs does ``easy_ustacks.py`` make?

Individual tags, alleles, and snps files are created when the script runs ``ustacks``. In addition, the script will produce a text file with counts of loci per individual, and a plot of retained loci per population.

### How does ``easy_ustacks.py`` work?

#### Running ``ustacks``
For inputs that are just flags (e.g., ``-d``), a short loop  builds a string based on the flags called at the command line. Similarly, the script builds a dictionary with flags as keys and values as values for those keys (e.g., ``dictionary["-m"] = "10"`` for stack depth m of 10). The script then writes and calls a ``ustacks`` bash script for all individuals based on their order in the population map. The script times how long it takes to run the ``ustacks`` bash script, and reports it to the user.

#### Counting and plotting retained loci
The script uses a grep command, counting every time the word "consensus" appears in the individual tags.tsv files produced by ``ustacks``, as these denote unique loci and writes them to a file. The file is called back in, parsed, and plotted by population. X axis labels are population names from your population map.

**Example plot:**

![image](https://github.com/nclowell/RAD_Scallops/blob/master/Seminar/images_for_notebook/pyplot_fig.png?raw=true)








**20170323 Natalie Lowell**
