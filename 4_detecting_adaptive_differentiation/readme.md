#### Detecting putatively adaptive differentiation

We used several methods for detected putatively adaptive differentiation.

The first is Fst outlier detection methods, for which we used [*BayeScan*](http://cmpg.unibe.ch/software/BayeScan/) and [*OutFLANK*](http://rstudio-pubs-static.s3.amazonaws.com/305384_9aee1c1046394fb9bd8e449453d72847.html). I ran BayesScan in the GUI using default parameters and plotted the output using [this script](https://github.com/nclowell/SeaCukes/blob/master/4_detecting_adaptive_differentiation/plot_bayescan.R). I ran OutFLANK and plotted the results using [this script](https://github.com/nclowell/SeaCukes/blob/master/4_detecting_adaptive_differentiation/OutFLANK.R).

The second is gene environment association methods, for which we used [*bayenv2*](https://gcbias.org/bayenv/) and redundancy analysis. For both, I gathered environmental predictor data from the Bio-Oracle and Bio-Oracle2 databases using [this script](https://github.com/nclowell/SeaCukes/blob/master/4_detecting_adaptive_differentiation/access_biooracle_for_env_predictors.R). 

Then, for bayenv2, I ran it using scaled environmental data, using default parameters (-k 100000) and the supplied script for running *bayenv2* per locus. Results were parsed using [this notebook](https://github.com/nclowell/SeaCukes/blob/master/4_detecting_adaptive_differentiation/parsing_bayenv2_results.ipynb).

For redundancy analysis, I used the R package [*vegan*](https://cran.r-project.org/web/packages/vegan/index.html) and [this script](https://github.com/nclowell/SeaCukes/blob/master/4_detecting_adaptive_differentiation/RDA.R). I ran regular RDAs and partial RDAs that conditioned spatial MEM variables, to account of neutral variation attributed to isolation-by-distance. I did so using multiple sets of predictors. For each set of predictors, I reduced them to few PCs. The sets of predictors were all variables, sea surface variables, bottom depth variables, and variables related to temperature. 

#### Some results

I found quite limited evidence for adaptive differentiation, identifying only 108 putatively adaptive loci (1.8% of total loci) using any of the approaches above. Using ``Bayenv2``, I identified some significant correlations between environmetnal predictors and SNPs. The environmental predictors with the most correlated SNPs included temperature and current velocity. No RDAs or partial RDAs were significant. No gene annotations were available for putatively adaptive loci.

