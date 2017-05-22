# Filtering with ``bowtie`` & ``BLAST`` to remove repetitive and paralogous loci
##### Introduction


Our lab uses additional screening steps to remove loci from repetitive regions and potentially paralogous loci from our catalogs we produce in ``cstacks``. These should not be included in our population genomics analyses, and are often not filtered out in the ``Stacks`` pipeline. So, we use ``bowtie`` and ``BLAST`` to filter these out.


Use ``bowtie2`` if you your data is above 50 bp or if your data has indels. Click [here](http://bowtie-bio.sourceforge.net/manual.shtml#the--v-alignment-mode) for the ``bowtie`` manual and [here](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml) for the ``bowtie2`` manual. The parsing script below works on both ``bowtie`` and ``bowtie2`` SAM output files, although there are some differences between the two worth nothing (e.g., no mismatch parameter ``-v`` in ``bowtie2``).

To install ``BLAST``, follow the [instructions on their website](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download). Click [here](https://www.ncbi.nlm.nih.gov/books/NBK279688/) for the ``BLAST`` manual.
<br>
<br>
<br>
## ``bowtie`` filtering

If a locus aligns to loci other than itself, it likely has a repeat sequence or is a paralogous locus and should be removed from our catalog, lest it confound or findings. To do this, we must [1] build a ``bowtie`` index ("index" is somewhat interchangeable with "database," "catalog," and "reference genome" here) and [2] align our index to itself, and then [3] boot out any loci that aligned to any loci other than itself.

##### [1] Making a fasta file for your ``bowtie`` index

To build a ``bowtie`` index, Mary made a [script](https://github.com/nclowell/FISH546/blob/master/Cod-Time-Series-Project/Scripts/genBOWTIEfasta.py) that creates a ``fasta`` file of the tags you would like to include in your index based on the output of ``populations``. You will need the .genepop file and the batch.catalog.tags.tsv file. Open your .genepop file and copy and paste the header that has the names of all of the SNPs (with format number_number, e.g., 4_26,4_140,5_9,8_24...) into a new text file. This will be your first command line argument. Then, unzip your batch.catalog.tags.tsv file. This will be your second command line argument. Afterwards, you can run Mary's [script](https://github.com/nclowell/FISH546/blob/master/Cod-Time-Series-Project/Scripts/genBOWTIEfasta.py).

Example code:
<br>
<br>
```
$	python genBOWTIEfasta.py \
../test_20k_cutoff/batch_3_loci.txt \
../test_20k_cutoff/batch_3.catalog.tags.tsv
```
<br>
<br>

##### [2] Building a ``bowtie`` index using ``bowtie-build``

The ``bowtie-build`` command main arguments are [i] a fasta file of sequences that you want to include in your index and [ii] the filename for your index. The index output files are named NAME.1.ebwt, NAME.2.ebwt, NAME.3.ebwt, NAME.4.ebwt, NAME.rev.1.ebwt, and NAME.rev.2.ebwt.


Example code:
<br>
<br>
```
$	bowtie-build seqsforBOWTIE.fa batch_3
```

##### [3] Aligning our ``bowtie`` index to itself

Use the ``bowtie`` command to align your index to itself. The command line arguments indlude [i] the filetype parameter (here, -f for ``fasta``), the number of reported alignments in the output file -k (here, 3) which must be more than 1, [iii] the mismatch paramter -v (here, 3), [iv] the --sam-nohead parameter that creates a SAM file as the alignment filetype output without a header line, [v] the name of your ``bowtie`` index files (here, batch_3), and [vi] the name for your output alignment file.



Example code:
<br>
<br>
```
$	./bowtie -f -v 3 -k 3 --sam --sam-nohead \
batch_3 \
seqsforBOWTIE.fa \
batch_3_BOWTIEout.sam
```


##### [4] Filtering out repetitive loci with custom script

Lastly, parse the ``bowtie`` output file using this [script](https://github.com/nclowell/RAD_Scallops/blob/master/CRAGIG_run1/Scripts/filtering/parse_bowtie_output.py). It will filter out any loci that matched to any sequences other than itself.

The command line arguments for this script are managed by ``argparse``: ``-i`` your input ``bowtie`` SAM output file and ``-o`` path to the output filtered fasta file.


Example code:
<br>
<br>
```
$ python parse_bowtie_output.py \
-i Bowtie/bowtie-1.2/bowtie2_test_k5.sam \
-o Bowtie/bowtie-1.2/bowtie2_filtered_k5.fa
```
<br>

## ``BLAST`` filtering

Similar to our ``bowtie`` filtering, we ``BLAST`` a database made of our catalog against itself and throw anything out that matches to more than itself.

##### [1] Make a ``BLAST`` database using ``bowtie``-filtered file

Use the ``makeblastdb`` command to make a database from your catalog. The command line arguments are [i] your -in paramter for input file, which is the ``bowtie``-filtered fasta you are using to make your database, [ii] the -parse_seqids flag, which allows you to retrieve sequences using the sequence identifiers, [iii] the -dbtype parameter for database type, which here is nucleotide, and [iv] the -out paramter for output filename for your ``bowtie``-filtered database.

Example code:
<br>
<br>
```
$ makeblastdb -in batch_3_BOWTIEout_filtered.fa \
-parse_seqids \
-dbtype nucl \
-out batch_3_BOWTIEfiltered
```

##### [2] ``BLAST`` query against itself

Use the ``blastn`` command to search the query against itself. The command line arguments are [i] the -query parameter for your ``bowtie``-filtered fasta file, [ii] -db parameter for your database you just made in ``BLAST``, and [iii] -out parameter for the output filename.

Example code:
<br>
<br>
```
$	blastn -query batch_3_BOWTIEout_filtered.fa \
-db batch_3_BOWTIEfiltered \
-out batch_3_BowtieBlastFiltered
```

##### [3] Filtering out repetitive loci with custom script

Lastly, you will use Dan's custom [script](https://github.com/nclowell/FISH546/blob/master/Cod-Time-Series-Project/Scripts/checkBlastResults_DD.py) for parsing out the repetitive loci. The command line arguments for this script are [i] the ``BLAST`` input file, [ii] the ``bowtie``-filtered fasta file, [iii] output filename for storing "good" data, and [iv] output filename for storing "bad" data.


Example code:
<br>
<br>
```
$	python checkBlastResults_DD.py
../Blast_b3_20k/batch_3_BowtieBlastFiltered
../Blast_b3_20k/batch_3_BOWTIEout_filtered.fa
../Blast_b3_20k/batch_3_BowtieBlastFiltered_GOOD.fa
../Blast_b3_20k/batch_3_BowtieBlastFiltered_BAD.fa
```

This will output a fasta file with loci that only matched themselves. This is what you will use to build your final SAM file to feed into ``pstacks`` in the final run of ``Stacks``.

<br>
<br>

## Creating final SAM with ``bowtie``

Now that you have double-filtered to remove repetitive loci and potential paralogs, you need to build your final index, and align your fastq files to it. Then, ``pstacks`` will be able to identify stacks from the alignment.

##### [1] Building your final ``bowtie`` index

Again, the ``bowtie-build`` command main arguments are [i] a fasta file of sequences that you want to include in your index and [ii] the filename for your index. Use your double-filtered fasta to build this index.

Example code:
<br>
<br>
```
$	./bowtie-build batch_3_BowtieBlastFiltered_GOOD.fa batch_3_final_index
```


### Helpful Reference
[Brieuc, M. S., Waters, C. D., Seeb, J. E., & Naish, K. A. (2014). A dense linkage map for Chinook salmon (Oncorhynchus tshawytscha) reveals variable chromosomal divergence after an ancestral whole genome duplication event. G3: Genes| Genomes| Genetics, 4(3), 447-460.](http://www.g3journal.org/content/4/3/447.full)

<br>
<br>
20170522 Natalie Lowell
