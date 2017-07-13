# 20170713 NL
# get pop gen stats (Ho, Hs, and Fis) from structure file

# get arguments from command line
args <- commandArgs(TRUE)

# name arguments
wd = args[1]
str = args[2]
inds = as.numeric(args[3])
loci = as.numeric(args[4])
date = args[5]

# import libraries
library(adegenet)
library(hierfstat)

# set working directory
setwd(wd)

# read in structure file
my_data <-read.structure(file = str,
                         n.ind = inds,
                         n.loc = loci,
                         onerowperind = FALSE,
                         col.lab = 1,
                         col.pop = 2,
                         NA.char = "-9",
                         ask = FALSE
                         )

# calculate allele frequencies for each locus in each population
my_freq <- pop.freq(my_data)
my_stats <- basic.stats(my_data)

# write any of these stats out to text files
write.table(my_stats$Hs, paste("Hs_",date, ".txt"), sep="\t")
write.table(my_stats$Ho, paste("Ho_",date, ".txt"), sep="\t")
write.table(my_stats$Fis, paste("Fis_",date, ".txt"), sep="\t")
