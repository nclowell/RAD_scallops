####################################################################
### AMOVA in R
# 20201014 Natalie Lowell

####################################################################

# import libraries
library(poppr)
library(pegas)

####################################################################

# set working directory 
setwd("E:/dD_cragig_mox_20191205/filtering/analyses/amova/pegas")

####################################################################

# name & read in genepop files, all loci, neutral loci, and putatively 
# adaptive loci
CG_gp_file_all = "primSNPs_CGmox_all.gen"
CG_gp_file_neu = "CG_likeX_neu5824.gen"
CG_gp_file_adap = "CG_likeX_putadapt108.gen"

####################################################################

CG_data_all <-read.genepop(CG_gp_file_all, ncode=3)
CG_data_neu <-read.genepop(CG_gp_file_neu, ncode=3)
CG_data_adap <-read.genepop(CG_gp_file_adap, ncode=3)

# read in strata file
CG_strata<- read.csv("CG_strata_for_amova.csv")
head(CG_strata)

# assign hierarchical levels from strata file to genind object
strata(CG_data_all) <- CG_strata
strata(CG_data_neu) <- CG_strata
strata(CG_data_adap) <- CG_strata

# change the format of your data from a genind to a genclone object
CG_all_gc <- as.genclone(CG_data_all)
CG_neu_gc <- as.genclone(CG_data_neu)
CG_adap_gc <- as.genclone(CG_data_adap)

#############################
# Running AMOVAs

# by site
amova_CG_site_all_nowithin <- poppr.amova(CG_all_gc, ~site, within = FALSE, method = "pegas", nperm = 1000)
amova_CG_site_all_nowithin

amova_CG_site_neu_nowithin <- poppr.amova(CG_neu_gc, ~site, within = FALSE, method = "pegas", nperm = 1000)
amova_CG_site_neu_nowithin

amova_CG_site_adap_nowithin <- poppr.amova(CG_adap_gc, ~site, within = FALSE, method = "pegas", nperm = 1000)
amova_CG_site_adap_nowithin

# by state / region
amova_CG_state_all_nowithin <- poppr.amova(CG_all_gc, ~state, within = FALSE, method = "pegas", nperm = 1000)
amova_CG_state_all_nowithin

amova_CG_state_neu_nowithin <- poppr.amova(CG_neu_gc, ~state, within = FALSE, method = "pegas", nperm = 1000)
amova_CG_state_neu_nowithin

amova_CG_state_adap_nowithin <- poppr.amova(CG_adap_gc, ~state, within = FALSE, method = "pegas", nperm = 1000)
amova_CG_state_adap_nowithin

# by inside or outside the Salish Sea
amova_CG_PS_all_nowithin <- poppr.amova(CG_all_gc, ~PS, within = FALSE, method = "pegas", nperm = 1000)
amova_CG_PS_all_nowithin

amova_CG_PS_neu_nowithin <- poppr.amova(CG_neu_gc, ~PS, within = FALSE, method = "pegas", nperm = 1000)
amova_CG_PS_neu_nowithin

amova_CG_PS_adap_nowithin <- poppr.amova(CG_adap_gc, ~PS, within = FALSE, method = "pegas", nperm = 1000)
amova_CG_PS_adap_nowithin

