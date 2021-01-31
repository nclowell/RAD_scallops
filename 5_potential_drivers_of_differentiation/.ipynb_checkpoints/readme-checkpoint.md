## Drivers of population differentiation

I looked for evidence of isolation by distance using this [script](https://github.com/nclowell/RAD_scallops/blob/master/5_potential_drivers_of_differentiation/IBD.R).

I also investigated biological functions associated with putatively adaptive SNPs to develop hypotheses of selection driving population differentiation. I used the ``UniProt Knowledge Base`` to create a ``blastx`` database, and retrieved GO Slim terms for hits of the fasta file of putatively adaptive loci. Then I used [this script](https://github.com/nclowell/RAD_sea_cucumbers/blob/master/5_potential_drivers_of_differentiation/gene_annotation_w_uniprot.R)) to sort annotations.

I used DAPC and PCA on putatively neutral versus putatively adaptive loci to look at potential differences in clustering patterns ([script here](https://github.com/nclowell/RAD_scallops/blob/master/3_pop_structure_analyses/PCA_DAPC.R).

#### Some results

We did not find evidence for isolation by distance, in that we did not find correlation among genetic and geographic distance.

![ibd](https://github.com/nclowell/RAD_scallops/blob/master/imgs/ibd.png?raw=true)

Here are the predictors with the most correlated SNPs (Sc).

![pred](https://github.com/nclowell/RAD_scallops/blob/master/imgs/predictors.PNG?raw=true)