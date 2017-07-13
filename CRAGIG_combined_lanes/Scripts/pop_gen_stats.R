# test command line args for R

args <- commandArgs(TRUE)

wd = args[1]
str = args[2]
inds = as.numeric(args[3])
loci = as.numeric(args[4])
date = args[5]

# import libraries
library(adegenet)
library(hierfstat)

# Set working directory
setwd(wd)

# Read in structure file
my_data <-read.structure(file = str,
                         n.ind = inds,
                         n.loc = loci,
                         onerowperind = FALSE,
                         col.lab = 1,
                         col.pop = 2,
                         NA.char = "-9",
                         ask = FALSE
                         )

# Calculate allele frequencies for each locus in each population
my_freq <- pop.freq(my_data)
my_stats <- basic.stats(my_data)

# Write any of these stats out to text files
write.table(my_stats$Hs, paste("Hs_",date, ".txt"), sep="\t")
write.table(my_stats$Ho, paste("Ho_",date, ".txt"), sep="\t")
write.table(my_stats$Fis, paste("Fis_",date, ".txt"), sep="\t")
