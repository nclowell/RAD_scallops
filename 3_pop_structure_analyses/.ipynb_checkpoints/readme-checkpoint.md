#### Population structure analyses

I calculated Fst and ran genic differentiation tests at the pairwise and global scales in ``genepop``, using [this R script](https://github.com/nclowell/SeaCukes/blob/master/3_pop_structure_analyses/FST_and_genic_diff_tests.R). I calculated expected heterozygosity, observed heterozygosity, and the proportion of polymorphic loci per site using [this R script](https://github.com/nclowell/SeaCukes/blob/master/3_pop_structure_analyses/get_He_Ho_propPolym_fromGP.R). To visualize patterns in population differentiation, I plotted PCAs and DAPCs using [this R script](https://github.com/nclowell/RAD_scallops/blob/master/3_pop_structure_analyses/PCA_DAPC.R). I tested whether the data could be subdivided into significant subpopulations using a clustering analyses in ``ADMIXTURE`` following [this tutorial](https://speciationgenomics.github.io/ADMIXTURE/). Lastly, I used [this script](https://github.com/nclowell/RAD_scallops/blob/master/3_pop_structure_analyses/amova.R) to run AMOVAs using the following hierarchical groupings: by state/provine (arbitary mid-scale regions) and inside or outside the Salish Sea.

#### Some population structure results

Overall, I observed low population structure: global Fst = 0.0009 and pairwise Fsts are presented in the table below. Only AMOVAs provided statistically significant results of population strcuture, but still have very small signals.

![fst](https://github.com/nclowell/RAD_scallops/blob/master/imgs/pairwise_fst.PNG?raw=true)