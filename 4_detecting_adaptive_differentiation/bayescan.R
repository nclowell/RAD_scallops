##########################################################
#### Plotting results from Bayescan
# 20191210 Natalie Lowell

##########################################################
# import libraries
library(ggplot2)
library(tidyverse)
library(genepopedit)
library(RColorBrewer)
library(cowplot)

###########################################################

setwd("E:/dD_cragig_mox_20191205/filtering/analyses/outliers")

# Specify the file names for the input files
bayescan_file <- "BSOut_CGmox_fst.txt" 
genepop_file <- "primSNPs_CGmox_noINDL_mac5_mQ20_mDP10_maf05_md70_inam_norep_HWE_oneSNPhiMAF_gorder_280i.gen"

##########################################################
# Specify the file names for the output files

bayescan_output_df_all <- "BS_CGmox_all_loci.txt"
bayescan_output_df_outliers <- "BS_CGmox_outliers.txt"

################################################################
# Part 1 : Read in the bayescan results and plot some summary stats

mydata <- read.table(bayescan_file, header = TRUE)
head(mydata)

# Plot some summary statistics from the bayescan results

# plot the distribution of fst
plot_fst <- ggplot() +
  geom_histogram(data =  mydata, aes(fst), bins = 100)+
  xlab(expression(italic(F[ST])))+
  ylab("Number of loci") +
  theme_classic()+
  geom_hline(yintercept=0, colour="white", size=0.25) 
plot_fst

plot_fsttail <- ggplot() +
  geom_histogram(data =  mydata, aes(fst), bins = 100)+
  xlab(expression(italic(F[ST])))+
  ylab("Number of loci") +
  coord_cartesian(xlim = c(0, 0.1), ylim = c(0, 100))+
  theme_classic()
plot_fsttail

# plot the distribution of q values
plot_qval <- ggplot() +
  geom_histogram(data =  mydata, aes(qval), bins = 100)+
  xlab("q-value") +
  ylab("Number of loci")+
  theme_classic()
plot_qval

# plot the fst vs qvalue
ggplot()+
  geom_point(data = mydata, aes(x = qval, y = fst), shape = 1, alpha = 0.4)+
  ylab(expression(italic(F[ST]))) +
  xlab("q-value")+
  theme_classic()

# plot the fst vs prob
ggplot()+
  geom_point(data = mydata, aes(x = prob, y = fst), shape = 1, alpha = 0.4)+
  ylab(expression(italic(F[ST]))) +
  xlab("Posterior probability")

# plot the fst vs log10_prob

plot_log10 <- ggplot()+
  geom_point(data = mydata, aes(x = log10.PO., y = fst), shape = 1, alpha = 0.4)+
  ylab(expression(italic(F[ST])))+
  xlab("log10 (posterior probability)")+
  theme_classic()
plot_log10

# arrange the three plots in a single row
multiplot <- plot_grid( plot_fst,
                        plot_fsttail ,
                        plot_qval, 
                        plot_log10 ,
                        align = 'vh',
                        labels = c("A", "B", "C", "D"),
                        hjust = 0,
                        nrow = 2)
multiplot

### Get outlier locus names

mydata <- read.table(bayescan_file, header = TRUE)

# read in locus names
locus_names <- read.csv("../../oneSNP_hiMAF_keepnames.txt", header=FALSE)

# add names column
data_inames <- cbind(locus_names, mydata)

# pick a threshold!! Here... 750
threshold = 750

# subset df for rows where log 10 posterior prob is over threshold
outliers_df <- filter(data_inames, log10.PO. > threshold)
outliers_df

# write to file
write.table(outliers_df, file = "BS_outliers.txt", sep="\t")

####################################################################

# Use built in FDR approach to set threshold
plot_bayescan(bayescan_file,FDR=0.05)
# 418  508  655 1470 1641 3013 3531 4425 4585 4592 4781
# so 11 outliers
bs_out_indeces <- c(418, 508, 655, 1470,
                    1641, 3013, 3531, 4425,
                    4585, 4592, 4781)

mydata2 <- mydata %>%
  mutate(BS_out_FDR=FALSE) %>%
  rowwise() %>%
  mutate(log10_q = log10(qval))
data2_inames <- cbind(locus_names, mydata2)
sig_data2_inam <- data2_inames %>%
  filter(BS_out_FDR == TRUE)

write_csv(sig_data2_inam, "Bayescan_11outliers_FDR_20201001.csv")

for(idx in bs_out_indeces){
  mydata2[idx,"BS_out_FDR"] = TRUE
}

# make new plot
plot_log10q_fst <- ggplot()+
  geom_point(data = mydata2, aes(x = log10_q, 
                                 y = fst, color=BS_out_FDR), 
             alpha = 0.4)+
  ylab(expression(italic(F[ST]))) +
  scale_color_manual(values=c("black", "red")) +
  xlab("log10 q-value") +

  theme_classic() +
  #scale_x_reverse() +
  xlim(0,-6) +
  theme(legend.position="none") #+

plot_log10q_fst

