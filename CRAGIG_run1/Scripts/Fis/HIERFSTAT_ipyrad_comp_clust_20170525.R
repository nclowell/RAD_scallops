# 20170522
#
# Purpose:
# To compare Fis distribution of different clustering thresholds with ipyrad
# 
#
# 
# ---------------------------------------------------------------------------------

# mport libraries
library(adegenet)
library(hierfstat)

# Set working directory
setwd("C:/Users/Natalie Lowell/SHARED_FOLDER/Learn_iPyrad/CRAGIG_RUN1_py")

# Read in structure file, with a ".str" file extension
my_data <-read.structure("Edited_outfiles/cragig006_biall_spid.str", 
                           onerowperind = FALSE,
                           col.pop = 2,
                           n.ind = 10,
                           n.loc = 29057,
                           col.lab = 1,
                           NA.char = "-9",
                           ask = FALSE)

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
write.table(my_stats$Fis, "Fis_cragig006_20170531.txt", sep="\t")
Fwrite.table(basic.stats(my_data)$n.ind.samp, "Genotype_counts.txt", sep="\t")
