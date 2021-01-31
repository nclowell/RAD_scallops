########################################################
## Making PCA and DAPC with matching color schemes
## 20191206 NL
#############################################################                                                    

library(adegenet)
library(hierfstat)
library (ggplot2)
library(ggpubr)

#############################################################                                                    

setwd("E:/dD_cragig_mox_20191205/filtering/analyses/")

# Read in genepop files of neutral loci loci only and outliers only
gpfile_all <-read.genepop("primSNPs_CGmox_all.gen", ncode = 3)
gpfile_neu <-read.genepop("CG_likeX_neu5824.gen", ncode = 3)
gpfile_out <-read.genepop("CG_likeX_putadapt108.gen", ncode = 3)

#############################################################                                                    

# Replace missing data information with the mean
gpfile_all_scaled <- scaleGen(gpfile_all, NA.method="mean")
gpfile_neu_scaled <- scaleGen(gpfile_neu, NA.method="mean")
gpfile_out_scaled <- scaleGen(gpfile_out, NA.method="mean")

### levels & colors for plots
ordered_pops <- c("Seward, AK",
                  "Sekiu, WA",  
                  "Port Gamble, WA",   
                  "Cypress Island, WA",
                  "Dabob Bay, WA",
                  "Monterey Bay, CA",
                  "Catalina Island, CA")

site_colors <- c("darkorchid4",
                    "darkblue",
                    "mediumseagreen",
                    "greenyellow",
                    "gold",
                    "chocolate1",
                    "red4")

ordered_states <- c("Alaska",
                    "Washington",
                    "California")

state_colors <- c("tomato",
                  "goldenrod2",
                  "dodgerblue4")

ordered_SS <- c("Inside", "Outside")
SS_colors = c("dodgerblue4", "orange3")

#############################################################################
### PCAs

# Conduct PCAs
pca_gpfile_all <- dudi.pca(gpfile_all_scaled,cent=TRUE,scale=FALSE,scannf=FALSE,nf=3)
pca_gpfile_neu <- dudi.pca(gpfile_neu_scaled,cent=TRUE,scale=FALSE,scannf=FALSE,nf=3)
pca_gpfile_out <- dudi.pca(gpfile_out_scaled,cent=TRUE,scale=FALSE,scannf=FALSE,nf=3)
# summary(pca_gpfile_neu) # info about variation is here

# Save the plotting coordinates as a seprate dataframe, so you can customize plot
gpfile_all_df <- pca_gpfile_all$li
gpfile_neu_df <- pca_gpfile_neu$li  
gpfile_out_df <- pca_gpfile_out$li  

# Custom vector of popnames
popnames_gpfile <- c(rep("Seward, AK",20), 
                                     rep("Sekiu, WA",59),
                                     rep("Port Gamble, WA",15),
                                     rep("Cypress Island, WA",50), 
                                     rep("Dabob Bay, WA",53),
                                     rep("Monterey Bay, CA",44),
                                     rep("Catalina Island, CA",39))
gpfile_all_df$Population = popnames_gpfile # add the names to the df
gpfile_neu_df$Population = popnames_gpfile
gpfile_out_df$Population = popnames_gpfile 

# re-order the levels in the order of appearance in the data.frame
gpfile_all_df$Population <- factor(gpfile_all_df$Population, levels = ordered_pops)
gpfile_neu_df$Population <- factor(gpfile_neu_df$Population, levels = ordered_pops)
gpfile_out_df$Population <- factor(gpfile_out_df$Population, levels = ordered_pops)

statenames_gpfile <-  c(rep("Alaska", 20), 
                        rep("Washington", 59),
                        rep("Washington",15),
                        rep("Washington", 50), 
                        rep("Washington", 53),
                        rep("California",44),
                        rep("California",39))

gpfile_all_df$States = statenames_gpfile # add the names to the df
gpfile_neu_df$States = statenames_gpfile 
gpfile_out_df$States = statenames_gpfile 

# re-order the levels in the order of appearance in the data.frame
gpfile_all_df$States <- factor(gpfile_all_df$States, levels = ordered_states)
gpfile_neu_df$States <- factor(gpfile_neu_df$States, levels = ordered_states)
gpfile_out_df$States <- factor(gpfile_out_df$States, levels = ordered_states)

reSS_gpfile <-  c(rep("Outside", 20), 
                  rep("Inside", 59),
                  rep("Inside",15),
                  rep("Inside", 50), 
                  rep("Inside", 53),
                  rep("Outside",44),
                  rep("Outside",39))
   
gpfile_all_df$SalishSea = reSS_gpfile # add the names to the df
gpfile_neu_df$SalishSea = reSS_gpfile 
gpfile_out_df$SalishSea = reSS_gpfile

# re-order the levels in the order of appearance in the data.frame
gpfile_all_df$SalishSea <- factor(gpfile_all_df$SalishSea, levels = ordered_SS)
gpfile_neu_df$SalishSea <- factor(gpfile_neu_df$SalishSea, levels = ordered_SS)
gpfile_out_df$SalishSea <- factor(gpfile_out_df$SalishSea, levels = ordered_SS)

# get percet var explained by each axis
eigs_all <- pca_gpfile_all$eig
axis1_var_all <- paste(substr(as.character((eigs_all[1] / sum(eigs_all))*100),1,5),"%",sep="")
axis2_var_all <- paste(substr(as.character((eigs_all[2] / sum(eigs_all))*100),1,5),"%",sep="")
eigs_neu <- pca_gpfile_neu$eig
axis1_var_neu <- paste(substr(as.character((eigs_neu[1] / sum(eigs_neu))*100),1,5),"%",sep="")
axis2_var_neu <- paste(substr(as.character((eigs_neu[2] / sum(eigs_neu))*100),1,5),"%",sep="")
eigs_out <- pca_gpfile_out$eig
axis1_var_out <- paste(substr(as.character((eigs_out[1] / sum(eigs_out))*100),1,5),"%",sep="")
axis2_var_out <- paste(substr(as.character((eigs_out[2] / sum(eigs_out))*100),1,5),"%",sep="")

### PCA by site

PCA_all_bysite <- ggplot(data = gpfile_all_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = Population), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_all, y=axis2_var_all) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
PCA_all_bysite

PCA_neu_bysite <- ggplot(data = gpfile_neu_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = Population), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_neu, y=axis2_var_neu) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
PCA_neu_bysite

PCA_out_bysite <- ggplot(data = gpfile_out_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = Population), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_out, y=axis2_var_out) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
PCA_out_bysite

### PCA by state

PCA_all_bystate <- ggplot(data = gpfile_all_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = States), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=state_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_all, y=axis2_var_all) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
PCA_all_bystate

PCA_neu_bystate <- ggplot(data = gpfile_neu_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = States), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=state_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_neu, y=axis2_var_neu) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
PCA_neu_bystate

PCA_out_bystate <- ggplot(data = gpfile_out_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = States), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=state_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_out, y=axis2_var_out) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
PCA_out_bystate

### PCA by Salish Sea, inside or outside

PCA_all_bySS <- ggplot(data = gpfile_all_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = SalishSea), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values = SS_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_all, y=axis2_var_all) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
PCA_all_bySS

PCA_neu_bySS <- ggplot(data = gpfile_neu_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = SalishSea), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values = SS_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_neu, y=axis2_var_neu) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
PCA_neu_bySS

PCA_out_bySS <- ggplot(data = gpfile_out_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = SalishSea), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=SS_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_out, y=axis2_var_out) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
PCA_out_bySS

#############################################################################
### DAPCs

ninds = 325
npcas = ninds - 1
n_pops = 9
ndims = n_pops - 1

dapc_all <- dapc(gpfile_all,gpfile_all$pop,n.pca=npcas,n.da=ndims,scannf=FALSE) 
test_a_score_all <- optim.a.score(dapc_all)
best_a_all = test_a_score_all$best
dapc_all <- dapc(gpfile_all,gpfile_all$pop,n.pca=best_a_all,n.da=ndims) 

dapc_neu <- dapc(gpfile_neu,gpfile_neu$pop,n.pca=npcas,n.da=ndims,scannf=FALSE) 
test_a_score_neu <- optim.a.score(dapc_neu)
best_a_neu = test_a_score_neu$best
dapc_neu <- dapc(gpfile_neu,gpfile_neu$pop,n.pca=best_a_neu,n.da=ndims) 

dapc_out <- dapc(gpfile_out,gpfile_out$pop,n.pca=npcas,n.da=ndims,scannf=FALSE) 
test_a_score_out <- optim.a.score(dapc_out)
best_a_out = test_a_score_out$best
dapc_out <- dapc(gpfile_out,gpfile_out$pop,n.pca=best_a_out,n.da=ndims) 

# make new df from loading coords & add pop and state cols
dapc_all_df <- as.data.frame(dapc_all$ind.coord)
dapc_all_df$pop <- popnames_gpfile 
dapc_all_df$state <- statenames_gpfile
dapc_all_df$SS <- reSS_gpfile

# make extra columns into 
dapc_all_df$pop <- factor(dapc_all_df$pop,levels = ordered_pops)
dapc_all_df$state <- factor(dapc_all_df$state,levels = ordered_states)
dapc_all_df$SS <- factor(dapc_all_df$SS,levels = ordered_SS)

# get string of percent pop var explained by first two axes
perc_first_PC_all <- paste(substr(as.character((dapc_all$eig[1] / sum(dapc_all$eig))*100), 1, 5), "%", sep="")
perc_second_PC_all <- paste(substr(as.character((dapc_all$eig[2] / sum(dapc_all$eig))*100), 1, 5), "%", sep="")

# make new df from loading coords & add pop and state cols
dapc_neu_df <- as.data.frame(dapc_neu$ind.coord)
dapc_neu_df$pop <- popnames_gpfile 
dapc_neu_df$state <- statenames_gpfile
dapc_neu_df$SS <- reSS_gpfile

# make extra columns into 
dapc_neu_df$pop <- factor(dapc_neu_df$pop,levels = ordered_pops)
dapc_neu_df$state <- factor(dapc_neu_df$state,levels = ordered_states)
dapc_neu_df$SS <- factor(dapc_neu_df$SS,levels = ordered_SS)

# get string of percent pop var explained by first two axes
perc_first_PC_neu <- paste(substr(as.character((dapc_neu$eig[1] / sum(dapc_neu$eig))*100), 1, 5), "%", sep="")
perc_second_PC_neu <- paste(substr(as.character((dapc_neu$eig[2] / sum(dapc_neu$eig))*100), 1, 5), "%", sep="")

# make new df from loading coords & add pop and state cols
dapc_out_df <- as.data.frame(dapc_out$ind.coord)
dapc_out_df$pop <- popnames_gpfile 
dapc_out_df$state <- statenames_gpfile
dapc_out_df$SS <- reSS_gpfile

# make extra columns into 
dapc_out_df$pop <- factor(dapc_out_df$pop,levels = ordered_pops)
dapc_out_df$state <- factor(dapc_out_df$state,levels = ordered_states)
dapc_out_df$SS <- factor(dapc_out_df$SS,levels = ordered_SS)

# get string of percent pop var explained by first two axes
perc_first_PC_out <- paste(substr(as.character((dapc_out$eig[1] / sum(dapc_out$eig))*100), 1, 5), "%", sep="")
perc_second_PC_out <- paste(substr(as.character((dapc_out$eig[2] / sum(dapc_out$eig))*100), 1, 5), "%", sep="")

### DAPC by site

DAPC_all_bypop <- ggplot(data = dapc_all_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = pop), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_all, y=perc_second_PC_all) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
DAPC_all_bypop

DAPC_neu_bypop <- ggplot(data = dapc_neu_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = pop), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_neu, y=perc_second_PC_neu) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
DAPC_neu_bypop

DAPC_out_bypop <- ggplot(data = dapc_out_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = pop), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_out, y=perc_second_PC_out) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
DAPC_out_bypop

### PCA by state

DAPC_all_bystate <- ggplot(data = dapc_all_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = state), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=state_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_all, y=perc_second_PC_all) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
DAPC_all_bystate

DAPC_neu_bystate <- ggplot(data = dapc_neu_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = state), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=state_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_neu, y=perc_second_PC_neu) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
DAPC_neu_bystate

DAPC_out_bystate <- ggplot(data = dapc_out_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = state), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=state_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_out, y=perc_second_PC_out) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
DAPC_out_bystate

### PCA by SS

DAPC_all_bySS <- ggplot(data = dapc_all_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = SS), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=SS_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_all, y=perc_second_PC_all) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
DAPC_all_bySS

DAPC_neu_bySS <- ggplot(data = dapc_neu_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = SS), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=SS_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_neu, y=perc_second_PC_neu) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
DAPC_neu_bySS

DAPC_out_bySS <- ggplot(data = dapc_out_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = SS), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=SS_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_out, y=perc_second_PC_out) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank())
DAPC_out_bySS

###############################################################################
### Multi-panel plots

### PCA all and DAPC all

# flip on axis
dapc_all_df$LD2 = dapc_all_df$LD2*-1

PCA_all_bysite <- ggplot(data = gpfile_all_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = Population), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_all, y=axis2_var_all) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank()) + 
  ggtitle("PCA") +
  theme(plot.title = element_text(hjust = 0.5))
PCA_all_bysite

DAPC_all_bypop <- ggplot(data = dapc_all_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = pop), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_all, y=perc_second_PC_all) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank()) + 
  ggtitle("DAPC") +
  theme(plot.title = element_text(hjust = 0.5))
DAPC_all_bypop

ggarrange(PCA_all_bysite, DAPC_all_bypop, 
          ncol=2, nrow=1, 
          common.legend = TRUE, 
          legend="bottom")

### PCA neu, all, out

PCA_neu_bysite <- ggplot(data = gpfile_neu_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = Population), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_neu, y=axis2_var_neu) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank()) + 
  ggtitle("Neutral") +
  theme(plot.title = element_text(hjust = 0.5))
PCA_neu_bysite

PCA_all_bysite <- ggplot(data = gpfile_all_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = Population), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_all, y=axis2_var_all) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank()) + 
  ggtitle("All") +
  theme(plot.title = element_text(hjust = 0.5))
PCA_all_bysite

PCA_out_bysite <- ggplot(data = gpfile_out_df, aes(x= Axis1, y= Axis2)) + 
  geom_point(aes(colour = Population), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=axis1_var_out, y=axis2_var_out) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank()) + 
  ggtitle("Outliers") +
  theme(plot.title = element_text(hjust = 0.5))
PCA_out_bysite

ggarrange(PCA_neu_bysite, PCA_all_bysite, PCA_out_bysite,
          ncol=3, nrow=1, 
          common.legend = TRUE, 
          legend="bottom")

### DAPC neu, all, out

dapc_out_df$LD2 = dapc_out_df$LD2*-1


DAPC_all_bypop <- ggplot(data = dapc_all_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = pop), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_all, y=perc_second_PC_all) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank()) +
  ggtitle("All") +
  theme(plot.title = element_text(hjust = 0.5))
DAPC_all_bypop

DAPC_neu_bypop <- ggplot(data = dapc_neu_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = pop), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_neu, y=perc_second_PC_neu) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank()) +
  ggtitle("Neutral") +
  theme(plot.title = element_text(hjust = 0.5))
DAPC_neu_bypop

DAPC_out_bypop <- ggplot(data = dapc_out_df, aes(x= LD1, y= LD2)) + 
  geom_point(aes(colour = pop), size = 3.0, alpha = 0.7) +
  scale_colour_manual(values=site_colors) +
  theme(plot.margin = unit(c(6,0,6,0), "pt")) +
  labs(x=perc_first_PC_out, y=perc_second_PC_out) +
  theme_classic() +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.text.y=element_blank(), axis.ticks.y=element_blank()) +
  theme(legend.position="right") +
  theme(legend.title=element_blank()) +
  ggtitle("Outliers") +
  theme(plot.title = element_text(hjust = 0.5))
DAPC_out_bypop

ggarrange(DAPC_neu_bypop, DAPC_all_bypop, DAPC_out_bypop,
          ncol=3, nrow=1, 
          common.legend = TRUE, 
          legend="bottom")
