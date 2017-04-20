# Purpose: getting Fis per locus
#
# 20170420
# Notice the input file is kind of bananas because... I removed the "pop"s from the Genepop file, other than the first, so that hierfstat
# treats all populations as one, and I can get across population Fis. I don't think 
# hierfstat liked that, so I also copied and pasted all the samples so it thought I 
# had two populations, to get it to run. Then I can ignore the second pop.
#
# 
# ---------------------------------------------------------------------------------

# Import these libraries
library(adegenet)
library(hierfstat)

# Set working directory
setwd("C:/Users/Natalie Lowell/Desktop")

# Read in your data as a genepop file, with a ".gen" file extension
# Need comma after each individual, can be space or tab delimited
# Specify how many characters code each allele with ncode
my_data <-read.genepop("tags_gp_fMV_sansreps_onepoptwice_20170420.gen", ncode = 2)

# To retreive useful data summaries
(summary(my_data))
my_data$pop

###########################################################
# Calculate allele frequencies for each locus in each population . Output saved as list
my_freq <- pop.freq(my_data)


#Query a locus of interest:
my_freq$L_27234

##############################################################
# Calculate number of individuals in data

# Counts the number of individual genotyped per locus and population
my_ind <- ind.count(my_data)
my_stats <- basic.stats(my_data)

#Get Observed heterozygosities per locus and pop
my_stats$Ho

# Get Expected heterozygosities per locus and pop (well, a proxy for them called 'gene diversity". Fucking Goudet)
my_stats$Hs

# Count succesful genotypes per locus
basic.stats(my_data)$n.ind.samp

# Get Fis per locus and pop 
my_stats$Fis

# Write any ofthese stats out to a text file so you can see what the fuck you are doing
write.table(my_stats$Hs, "my_Hs.txt", sep="\t")
write.table(my_stats$Fis, "Fis_snps_onepop_20170418.txt", sep="\t")
write.table(basic.stats(my_data)$n.ind.samp, "Genotype_counts.txt", sep="\t")
