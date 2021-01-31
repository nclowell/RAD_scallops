## Population structure and adaptive differentiation in the purple-hinged rock scallop, *Crassadoma gigantea*

![image](https://github.com/nclowell/RAD_Scallops/blob/master/imgs/scallop.jpg)

[Photo credit](https://www.centralcoastbiodiversity.org/rock-scallop-bull-crassodoma-gigantea.html)

#### Background

For decades, the shellfish growing community has been interested in cultivating the purple-hinged rock scallop. Although growing methods have been challenged by this species' life history (in particular the cementing behavior of adults), there is renewed interest in developing methods for commercial production.

However, farmed escapes pose genetic risks to populations. If hatchery-produced and wild individuals interbreed, they can cause loss of genetic diversity within and between populations through the production of many offspring from few broodstock and through the movement of animals due to collection of broodstock and transfer of seed. Therefore, it is important to assess parameters related to genetic diversity to inform native shellfish aquaculture management.

A research team led by my PhD adviser Dr. Lorenz Hauser set out to explore population structure and test for local adaptation in the rock scallop, using a multidiscplinary approach. To address several project objectives, I used RAD sequencing to quantify and characterize patterns in population structure, investigate adaptive differentiation, and identify potential drivers of population differentiation. This project was funded by the NOAA Sea Grant Aquaculture Research Program ([project R/SFA/N-1](https://wsg.washington.edu/research/a-new-native-species-for-shellfish-aquaculture-and-precautionary-guidelines-to-protect-wild-populations-local-adaptation-population-differentiation-and-broodstock-development-in-rock-scallops/))

#### Project Goals

**[1]** Quantify and characterize patterns in population structure
<br>**[2]** Identify putatively adaptive loci and evaluate whether patterns of population structure differ between putatively neutral and adaptive data sets

#### Overview of methods

I extracted, quantified and verified quality of DNA from 7 sites spanning from Alaska to California, and then prepared single-digest RAD libraries using *sbfI* follwing [Etter et al 2011](https://link.springer.com/protocol/10.1007/978-1-61779-228-1_9). DNA was sequenced to 150bp at BGI. You can find the library prep protocols in [1_library_prep](https://github.com/nclowell/RAD_scallops/tree/master/1_library_prep).

I clustered loci and genotyped individuals using the [*dDocent*](https://www.ddocent.com/) pipeline, using a de novo assembly. Genotype data were filtered using [*vcftools*](http://vcftools.sourceforge.net/) and custom python scripts, such that retained loci passed the following filters:

- minimum minor allele count of 5 reads
- minimum quality score of 20
- minimum genotype depth of 10 reads
- minimum minor allele frequency of 5%
- maximum missing data per locus of 30% across sites
- one SNP per RAD tag, retaining that with the highest minor allele frequency
- in Hardy Weinberg Equilibrium

Individuals were retained if they were successfully genotyped at at least 70% of loci. You can find documentation for my assembly, genotyping, and filtering [here]().

I used [*genepop*](https://cran.r-project.org/web/packages/genepop/index.html) to calculate FST and run exact G tests at global and pairwise scales. We used *genepop* to calculate expected and observed heterozygosity as well, and used custom python scripts to calculate the proportion of polymorphic loci per site.

I used principal component analysis and dicriminant analysis of principal components to investigate patterns of population differentiation, using the R package [*adegenet*](https://cran.r-project.org/web/packages/adegenet/index.html). I used [*ADMIXTURE*](https://gaworkshop.readthedocs.io/en/latest/contents/07_admixture/admixture.html) to conduct a clustering analysis and the R package [*poppr*](https://cran.r-project.org/web/packages/poppr/index.html) to summarize the partitioning of variance among different hierarchical groupings in AMOVAs. You can see the scripts used for population structure analyses [here]().

A major objective of the grant was to investigate the potential for local adaptation in the species. Reciprocal transplant and common garden experiments were attempted, but ultimately rock scallops would not spawn in ways necessary for the breeding designs needed for those experiments. Alternative projects to address related questions were designed and implemented, such as investigating age at maturity (collaborator Molly Jackson's master's thesis) and 

Meanwhile, I leveraged my genomic data to look for signatures of local adaptation. Specifically, I used gene-environment association methods including [*bayenv2*](https://gcbias.org/bayenv/) and redundancy analysis. Additionally, I used FST outlier detection to find additional SNPs putatively under selection. For these methods, I used [*Bayescan*](http://cmpg.unibe.ch/software/BayeScan/) and the R package [*OutFLANK*](http://rstudio-pubs-static.s3.amazonaws.com/305384_9aee1c1046394fb9bd8e449453d72847.html). To determine potential biological processes associated with putatively adaptive loci, I used [*blastx*](https://blast.ncbi.nlm.nih.gov/Blast.cgi?LINK_LOC=blasthome&PAGE_TYPE=BlastSearch&PROGRAM=blastx) and the [*UniProt Knowledge Base*](https://www.uniprot.org/help/uniprotkb) to retrieve GO Slim terms. You can find scripts and notebooks associated with these analyses [here]().

 Loci were classified as putatively adaptive if identified using at least one of two approaches:

We investigated potential drivers of observed differentiation. We tested for isolation by distance using a Mantel test in R. We also compared patterns of differentiation between putatively neutral and putatively adaptive loci.

#### Some results

Data files and all results will be shared publicly here after publication. Below is a DAPC along with site map, to see general patterns of popuation differentiation. Some other results are shared within the readmes per directory of this repo.



#### This repository

This repository contains the protocols, scripts, and notebooks that I used in this project. Here are the quick links:

[1_library_prep](https://github.com/nclowell/RAD_scallops/tree/master/1_library_prep)

[2_assembly_genotyping_and_filtering](https://github.com/nclowell/RAD_scallops/tree/master/2_assembly_genotyping_and_filtering)

[3_pop_structure_analyses](https://github.com/nclowell/RAD_scallops/tree/master/3_pop_structure_analyses)

[4_detecting_adaptive_differentiation]()

[5_potential_drivers_of_differentiation]()

