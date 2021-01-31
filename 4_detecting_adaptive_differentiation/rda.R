#######################################################
## RDA 20210112

#######################################################

library(codep)
library(adespatial)
library(adegraphics)
library(vegan)
library(ape)
library(car)
library(adegenet)
library(tidyverse) 
library(psych)
library(MonteCarlo)
library(data.table)

#######################################################

outliers <- function(x,z){
  lims <- mean(x) + c(-1, 1) * z * sd(x)     # find loadings +/-z sd from mean loading     
  x[x < lims[1] | x > lims[2]]               # locus names in these tails
}

make_zero <- function(adjR2){
  if(is.na(adjR2) == FALSE){
    if(adjR2 < 0){
      return(0)
    } else {
      return(adjR2)
    }
  }
  else {
    return(adjR2)
  }
}

#######################################################
# Read in genetic data, environmental data, and site coordinates

# set wd
setwd("~/Desktop/RDA/CG_rda/")

### read in site allele frequencies
afs <- read_csv("CG_all_pops_AFs_array.csv", col_names = FALSE) # geographic order
dim(afs) # 7 sites (rows) and 5886 SNPs (columns)
afs[1:7,1:7] # peek
# # A tibble: 7 x 7
# X1    X2    X3    X4    X5    X6    X7
# <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl>
#   1 0.975 0.75  0.8   0.975 0.775 0.675 0.875
# 2 0.958 0.72  0.873 0.924 0.873 0.814 0.847
# 3 0.867 0.7   0.8   0.9   0.767 0.867 0.867
# 4 0.97  0.83  0.8   0.84  0.73  0.87  0.88 
# 5 0.972 0.736 0.849 0.906 0.811 0.83  0.849
# 6 0.886 0.75  0.761 0.875 0.898 0.818 0.83 
# 7 0.872 0.731 0.808 0.821 0.821 0.782 0.833

### hellinger transformation of allele frequencies
afs_hell <- decostand(afs,
                      method="hellinger",
                      MARGIN=1, # SNPs are in rows, so 1 = rows # <--- is this the correct margin?
                      na.rm=TRUE)
afs_hell[1:5,1:5]
# X1         X2         X3         X4         X5
# 1 0.01408907 0.01235693 0.01276218 0.01408907 0.01256119
# 2 0.01394183 0.01208658 0.01330896 0.01369220 0.01330896
# 3 0.01327134 0.01192488 0.01274824 0.01352155 0.01248254
# 4 0.01402401 0.01297256 0.01273595 0.01305047 0.01216600
# 5 0.01403696 0.01221459 0.01311879 0.01355202 0.01282184

### reduce allele frequencies into few PCs using kaiser-guttman criterion (select axes with eigenvalues > mean eigevalue)
geno.pca <- prcomp(afs_hell, scale = T)
screeplot(geno.pca, npcs = 20, type = "lines", bstick = F)
afs_hell_egvals <- geno.pca$sdev^2
KG_afs_hell_egvals <- afs_hell_egvals[afs_hell_egvals > mean(afs_hell_egvals)] 
retain_num <- length(KG_afs_hell_egvals)
geno.pca.axes <- geno.pca$x[,1:retain_num] # 58.29% cumulative genetic variation explained
head(geno.pca.axes)

### read in environmental data (not yet scaled)
Env <- read_csv("CG_env_data_29.csv")
Env[1:5,1:5]
# # A tibble: 5 x 5
# Name            BO2_salinitymean_ss BO2_ppmean_ss BO2_nitratemean_ss BO2_phosphatemean_ss
# <chr>                         <dbl>         <dbl>              <dbl>                <dbl>
#   1 SewardAK                       31.4        0.0171              4.03                 0.576
# 2 SekiuWA                        26.1        0.0213              0.915                0.714
# 3 PortGambleWA                   24.1        0.0704              2.54                 0.717
# 4 DabobBayWA                     24.4        0.0557              2.00                 0.733
# 5 CypressIslandWA                25.2        0.0252              0.791                0.932

corr_matrix <- as.data.frame(cor(Env[,2:ncol(Env)]))
write_csv(corr_matrix, "CG_corr_matrix_env_preds.csv")

### reduce env data into few PCs using kaiser-guttman criterion (select axes with eigenvalues > mean eigevalue)
env.pca <- prcomp(Env[,2:ncol(Env)], scale = T)
screeplot(env.pca, npcs = 20, type = "lines", bstick = F)
env_egvals <- env.pca$sdev^2
KG_env_egvals <- env_egvals[env_egvals > mean(env_egvals)] 
retain_num_env <- length(KG_env_egvals)
env.pca.axes <- as.data.frame(env.pca$x[,1:retain_num_env]) # 58.29% cumulative genetic variation explained
head(env.pca.axes)

### which predictors are strongly associated with the first 3 axes?
envPred_load_2PCs <- as_tibble(env.pca$rotation[,1:2], rownames="EnvPred")
write_csv(envPred_load_2PCs, "CG_EnvPred_loadings_2PCs.csv")
envPred_load_2PCs_abs <- as_tibble(envPred_load_2PCs)
envPred_load_2PCs_abs[2:3] <- abs(envPred_load_2PCs_abs[2:3])

# with the first
envPred_load_PC1_abs <- arrange(envPred_load_2PCs_abs, desc(PC1)) %>%
  select(EnvPred, PC1)

# second
envPred_load_PC2_abs <- arrange(envPred_load_2PCs_abs, desc(PC2)) %>%
  select(EnvPred, PC2)

### site coords
site_coords <- read_csv("CG_site_coords.csv")
site_coords
# # A tibble: 7 x 3
# Site    Lat  Long
# <chr> <dbl> <dbl>
#   1 SW_AK  60.1 -149.
# 2 SK_WA  48.3 -124.
# 3 PG_WA  47.9 -123.
# 4 CI_WA  48.6 -123.
# 5 DB_WA  47.8 -123.
# 6 MT_CA  36.8 -122.
# 7 CI_CA  33.5 -118.

# keep just lat and long and save in matrix
Coor <- site_coords %>%
  select(Lat, Long)
Coor_asmat <- as.matrix(Coor)

### get dbMEMs
plot(Coor_asmat[,2], Coor_asmat[,1], asp=1)
DistSpatial<-gcd.hf(Coor_asmat) 
scallop_dbmem <- as.matrix(dbmem(DistSpatial, MEM.autocor = "positive")) # 1

#######################################################
# [RDA1]
# - pop-based
# - partial RDA, condition with dbMEMs
# - all env predictors combined into few PCS
# - all genetic variation in allele frequences

# RESULTS
# VIF: all < 10
# adjR2 = -0.109 (null = 0.00821 with negatives as zeros)
# quotient real / null adjR2: -13.28
# difference real - null adjR2: -0.117
# ANOVAs insignificant for full model and each axis
#######################################################

# run RDA
Y1 <- env.pca.axes
X1 <- afs_hell
Z1 <- scallop_dbmem
rda1 <- rda(X1 ~ . + Condition(Z1), data= Y1)
# Call: rda(formula = X1 ~ PC1 + PC2 + Condition(Z1), data = Y1)
# 
# Inertia Proportion Rank
# Total         0.0009431  1.0000000     
# Conditional   0.0002158  0.2287718    1
# Constrained   0.0002395  0.2539795    2
# Unconstrained 0.0004878  0.5172487    3
# Inertia is variance 
# 
# Eigenvalues for constrained axes:
#   RDA1       RDA2 
# 0.00013331 0.00010622 
# 
# Eigenvalues for unconstrained axes:
#   PC1        PC2        PC3 
# 0.00027440 0.00012396 0.00008947 

# loadings
coef(rda1)
# RDA1       RDA2
# Z1   0.07976744 -0.5517054
# PC1  0.10588114 -0.0451462
# PC2 -0.01086855 -0.2373876

# ANOVA for all axes at once
sig.full.rda1 <- anova.cca(rda1, parallel=getOption("mc.cores")) # default is permutation=999
sig.full.rda1 
# Model: rda(formula = X1 ~ PC1 + PC2 + Condition(Z1), data = Y1)
# Df   Variance      F Pr(>F)
# Model     2 0.00023953 0.7365  0.722
# Residual  3 0.00048783   

# ANOVA per axis
sig.axis.rda1<- anova.cca(rda1, by="axis", parallel=getOption("mc.cores"))
sig.axis.rda1 
# Model: rda(formula = X1 ~ PC1 + PC2 + Condition(Z1), data = Y1)
# Df   Variance      F Pr(>F)
# RDA1      1 0.00013331 0.8198  0.791
# RDA2      1 0.00010622 0.6532  0.662
# Residual  3 0.00048783  

vif.cca(rda1)
# Z1      PC1      PC2 
# 3.175192 1.227154 2.948038 

RsquareAdj(rda1)
# $r.squared
# [1] 0.2539795
# 
# $adj.r.squared
# [1] -0.1090236

#######################################################
# [RDA1_nospace]
# - pop-based
# - all env predictors combined into few PCS
# - all genetic variation in allele frequences

# RESULTS
# VIF: all < 10
# adjR2 = 0.0546 (null = 0.00436 with negatives as zeros)
# quotient real / null adjR2: 12.52294
# difference real - null adjR2: 0.05024
# ANOVAs insignificant for full model and each axis
#######################################################

# run RDA
Y1 <- env.pca.axes
X1 <- afs_hell
rda1_nospace <- rda(X1 ~ ., data= Y1)
# Call: rda(formula = X1 ~ PC1 + PC2, data = Y1)
# 
# Inertia Proportion Rank
# Total         0.0009431  1.0000000     
# Constrained   0.0003487  0.3697594    2
# Unconstrained 0.0005944  0.6302406    4
# Inertia is variance 
# 
# Eigenvalues for constrained axes:
#   RDA1       RDA2 
# 0.00021599 0.00013274 
# 
# Eigenvalues for unconstrained axes:
#   PC1        PC2        PC3        PC4 
# 0.00027965 0.00012719 0.00009811 0.00008945 

# loadings
coef(rda1_nospace)
# RDA1        RDA2
# PC1 0.03510458 -0.09779666
# PC2 0.13026517  0.04675930

# ANOVA for all axes at once
sig.full.rda1_nospace <- anova.cca(rda1_nospace, parallel=getOption("mc.cores")) # default is permutation=999
sig.full.rda1_nospace 
# Model: rda(formula = X1 ~ PC1 + PC2, data = Y1)
# Df   Variance      F Pr(>F)
# Model     2 0.00034873 1.1734  0.329
# Residual  4 0.00059439  

# ANOVA per axis
sig.axis.rda1_nospace <- anova.cca(rda1_nospace, by="axis", parallel=getOption("mc.cores"))
sig.axis.rda1_nospace
# Model: rda(formula = X1 ~ PC1 + PC2, data = Y1)
# Df   Variance      F Pr(>F)
# RDA1      1 0.00021599 1.4535  0.400
# RDA2      1 0.00013274 0.8933  0.496
# Residual  4 0.00059439   

vif.cca(rda1_nospace)
# PC1 PC2 
# 1   1 
RsquareAdj(rda1_nospace)
# $r.squared
# [1] 0.3697594
# 
# $adj.r.squared
# [1] 0.05463907

#######################################################
# [RDA_ss]
# - pop-based
# - partial RDA, conditioning for space
# - all sea surface env predictors combined into few PCS
# - all genetic variation in allele frequences

# RESULTS
# VIF: all < 10
# adjR2 = -0.107 (null =  0.0113 with negatives as zeros)
# quotient real / null adjR2: -9.469027
# difference real - null adjR2: -0.1183
# ANOVAs insignificant for full model and each axis
#######################################################

### sea surface env vars
subset_ss = subset(Env, 
                   select=c(Name,
                            BO2_salinitymean_ss,
                            BO2_ppmean_ss,
                            BO2_nitratemean_ss,
                            BO2_phosphatemean_ss,
                            BO2_dissoxmean_ss,
                            BO_ph,
                            BO_calcite,
                            BO2_curvelmax_ss,
                            BO2_curvelmin_ss,
                            BO2_curvelrange_ss,
                            BO2_curvelmean_ss,
                            BO2_tempmean_ss,
                            BO2_tempmin_ss,
                            BO2_tempmax_ss,
                            BO2_temprange_ss))

# PCA on sea surface environmental predictors, use just few that explain most variation
env_ss_pca <- prcomp(subset_ss[,2:ncol(subset_ss)], scale = TRUE)
env_ss_egvals <- env_ss_pca$sdev^2
KG_env_ss_egvals <- env_ss_egvals[env_ss_egvals > mean(env_ss_egvals)] 
retain_num_env_ss <- length(KG_env_ss_egvals)
env.ss.pca.axes <- as.data.frame(env_ss_pca$x[,1:retain_num_env_ss]) # 58.29% cumulative genetic variation explained
head(env.ss.pca.axes)

### which predictors are strongly associated with the first 2 axes?
envPred_ss_load_2PCs <- as_tibble(env_ss_pca$rotation[,1:2], rownames="EnvPred")
#write_csv(envPred_ss_load_2PCs, "EnvPred_ss_loadings_2PCs.csv")
envPred_ss_load_2PCs_abs <- as_tibble(envPred_ss_load_2PCs)
envPred_ss_load_2PCs_abs[2:3] <- abs(envPred_ss_load_2PCs_abs[2:3])

# with the first
envPred_ss_load_PC1_abs <- arrange(envPred_ss_load_2PCs_abs, desc(PC1)) %>%
  select(EnvPred, PC1)

# second
envPred_ss_load_P2_abs <- arrange(envPred_ss_load_2PCs_abs, desc(PC2)) %>%
  select(EnvPred, PC2)

# run RDA
Y_ss <- env.ss.pca.axes
X_ss <- afs_hell
Z_ss <- scallop_dbmem  
rda6_ss_sp <- rda(X_ss ~ . + Condition(Z_ss), data= Y_ss)
# Call: rda(formula = X_ss ~ PC1 + PC2 + Condition(Z_ss), data = Y_ss)
# 
# Inertia Proportion Rank
# Total         0.0009431  1.0000000     
# Conditional   0.0002158  0.2287718    1
# Constrained   0.0002405  0.2549782    2
# Unconstrained 0.0004869  0.5162501    3
# Inertia is variance 
# 
# Eigenvalues for constrained axes:
#   RDA1       RDA2 
# 0.00013301 0.00010747 
# 
# Eigenvalues for unconstrained axes:
#   PC1        PC2        PC3 
# 0.00027474 0.00012266 0.00008949 

coef(rda6_ss_sp)
# RDA1        RDA2
# Z_ss 0.3770557 -0.72831199
# PC1  0.1425952  0.05442324
# PC2  0.2092763 -0.42472499

# ANOVA for all axes at once
sig.full.rda6_ss_sp <- anova.cca(rda6_ss_sp, parallel=getOption("mc.cores")) # default is permutation=999
sig.full.rda6_ss_sp 
# Model: rda(formula = X_ss ~ PC1 + PC2 + Condition(Z_ss), data = Y_ss)
# Df   Variance      F Pr(>F)
# Model     2 0.00024047 0.7409  0.687
# Residual  3 0.00048688  

# ANOVA per axis
sig.axis.rda6_ss_sp <- anova.cca(rda6_ss_sp, by="axis", parallel=getOption("mc.cores"))
sig.axis.rda6_ss_sp
# Model: rda(formula = X_ss ~ PC1 + PC2 + Condition(Z_ss), data = Y_ss)
# Df   Variance      F Pr(>F)
# RDA1      1 0.00013301 0.8195  0.794
# RDA2      1 0.00010747 0.6622  0.649
# Residual  3 0.00048688    

vif.cca(rda6_ss_sp)
# Z_ss      PC1      PC2 
# 5.708266 1.010621 5.697645 

RsquareAdj(rda6_ss_sp)
# $r.squared
# [1] 0.2549782
# 
# $adj.r.squared
# [1] -0.1070263

#######################################################

# [RDA_ss_ns]
# - pop-based
# - not conditioning for space
# - all sea surface env predictors combined into few PCS
# - all genetic variation in allele frequences

# RESULTS
# VIF: all < 10
# adjR2 = 0.060 (null = 0.005 including negatives, with negatives as zeros)
# quotient real / null adjR2: 12
# difference real - null adjR2: 0.055
# ANOVAs marginally significant for full model and for first axis
#######################################################

# run RDA
Y_ss_ns <- env.ss.pca.axes
X_ss_ns <- afs_hell
rda_ss_ns <- rda(X_ss ~ ., data= Y_ss)
# Call: rda(formula = X_ss ~ PC1 + PC2, data = Y_ss)
# 
# Inertia Proportion Rank
# Total         0.0009431  1.0000000     
# Constrained   0.0003516  0.3728447    2
# Unconstrained 0.0005915  0.6271553    4
# Inertia is variance 
# 
# Eigenvalues for constrained axes:
#   RDA1       RDA2 
# 0.00022464 0.00012699 
# 
# Eigenvalues for unconstrained axes:
#   PC1        PC2        PC3        PC4 
# 0.00028340 0.00012674 0.00009204 0.00008930 

coef(rda_ss_ns)
# RDA1        RDA2
# PC1 -0.004873114 0.151745562
# PC2  0.198259752 0.006366858

# ANOVA for all axes at once
sig.full.rda_ss_ns <- anova.cca(rda_ss_ns, parallel=getOption("mc.cores")) # default is permutation=999
sig.full.rda_ss_ns 
# Model: rda(formula = X_ss ~ PC1 + PC2, data = Y_ss)
# Df   Variance     F Pr(>F)
# Model     2 0.00035164 1.189  0.325
# Residual  4 0.00059148 

# ANOVA per axis
sig.axis.rda_ss_ns <- anova.cca(rda_ss_ns, by="axis", parallel=getOption("mc.cores"))
sig.axis.rda_ss_ns
# Model: rda(formula = X_ss ~ PC1 + PC2, data = Y_ss)
# Df   Variance      F Pr(>F)
# RDA1      1 0.00022464 1.5192  0.354
# RDA2      1 0.00012699 0.8588  0.514
# Residual  4 0.00059148   

vif.cca(rda_ss_ns)
# PC1 PC2 
# 1   1 

RsquareAdj(rda_ss_ns)
# $r.squared
# [1] 0.3728447
# 
# $adj.r.squared
# [1] 0.05926708

#######################################################
# [RDA_bd]
# - pop-based
# - partial RDA, conditioning for space
# - all bottom depth env predictors combined into few PCS
# - all genetic variation in allele frequences

# RESULTS
# VIF: all < 10
# adjR2 = -0.11 (null = 0.009 with negatives as zeros)
# quotient real / null adjR2: -12.22222
# difference real - null adjR2: -0.119
# ANOVAs insignificant for full model and each axis
#######################################################

### sea surface env vars
subset_bdmean = subset(Env, 
                       select=c(Name,
                                BO2_salinitymean_bdmean,
                                BO2_ppmean_bdmean,
                                BO2_nitratemean_bdmean,
                                BO2_phosphatemean_bdmean,
                                BO2_dissoxmean_bdmean,
                                BO2_curvelmax_bdmean,
                                BO2_curvelmin_bdmean,
                                BO2_curvelrange_bdmean,
                                BO2_curvelmean_bdmean,
                                BO2_tempmean_bdmean,
                                BO2_tempmin_bdmean,
                                BO2_tempmax_bdmean,
                                BO2_temprange_bdmean))

# PCA on sea surface environmental predictors, use just few that explain most variation
env_bd_pca <- prcomp(subset_bdmean[,2:ncol(subset_bdmean)], scale = TRUE)
env_bd_egvals <- env_bd_pca$sdev^2
KG_env_bd_egvals <- env_bd_egvals[env_bd_egvals > mean(env_bd_egvals)] 
retain_num_env_bd <- length(KG_env_bd_egvals)
env.bd.pca.axes <- as.data.frame(env_bd_pca$x[,1:retain_num_env_bd]) # 58.29% cumulative genetic variation explained
head(env.bd.pca.axes)

### which predictors are strongly associated with the first 2 axes?
envPred_bd_load_2PCs <- as_tibble(env_bd_pca$rotation[,1:2], rownames="EnvPred")
#write_csv(envPred_bd_load_2PCs, "EnvPred_bd_loadings_2PCs.csv")
envPred_bd_load_2PCs_abs <- as_tibble(envPred_bd_load_2PCs)
envPred_bd_load_2PCs_abs[2:3] <- abs(envPred_bd_load_2PCs_abs[2:3])

# with the first
envPred_bd_load_PC1_abs <- arrange(envPred_bd_load_2PCs_abs, desc(PC1)) %>%
  select(EnvPred, PC1)

# second
envPred_bd_load_P2_abs <- arrange(envPred_bd_load_2PCs_abs, desc(PC2)) %>%
  select(EnvPred, PC2)

# run RDA
Y_bd <- env.bd.pca.axes
X_bd <- afs_hell
Z_bd <- scallop_dbmem  
rda_bd <- rda(X_bd ~ . + Condition(Z_bd), data= Y_bd)
# Call: rda(formula = X_bd ~ PC1 + PC2 + Condition(Z_bd), data = Y_bd)
# 
# Inertia Proportion Rank
# Total         0.0009431  1.0000000     
# Conditional   0.0002158  0.2287718    1
# Constrained   0.0002375  0.2518633    2
# Unconstrained 0.0004898  0.5193649    3
# Inertia is variance 
# 
# Eigenvalues for constrained axes:
#   RDA1       RDA2 
# 0.00013180 0.00010574 
# 
# Eigenvalues for unconstrained axes:
#   PC1        PC2        PC3 
# 0.00027599 0.00012433 0.00008951 

coef(rda_bd)
# RDA1       RDA2
# Z_bd -0.1082899 -0.6921139
# PC1   0.1076272 -0.1270799
# PC2  -0.1436859 -0.3964336

# ANOVA for all axes at once
sig.full.rda_bd  <- anova.cca(rda_bd, parallel=getOption("mc.cores")) # default is permutation=999
sig.full.rda_bd 
# Model: rda(formula = X_bd ~ PC1 + PC2 + Condition(Z_bd), data = Y_bd)
# Df   Variance      F Pr(>F)
# Model     2 0.00023754 0.7274  0.707
# Residual  3 0.00048982 

# ANOVA per axis
sig.axis.rda_bd <- anova.cca(rda_bd, by="axis", parallel=getOption("mc.cores"))
sig.axis.rda_bd
# Model: rda(formula = X_bd ~ PC1 + PC2 + Condition(Z_bd), data = Y_bd)
# Df   Variance      F Pr(>F)
# RDA1      1 0.00013180 0.8072  0.818
# RDA2      1 0.00010574 0.6476  0.638
# Residual  3 0.00048982  

vif.cca(rda_bd)
# Z_bd      PC1      PC2 
# 4.435239 1.495438 3.939800 

RsquareAdj(rda_bd)
# $r.squared
# [1] 0.2518633
# 
# $adj.r.squared
# [1] -0.113256

#######################################################
# [RDA_bd_ns]
# - pop-based
# - not conditioning for space
# - all bottom depth env predictors combined into few PCS
# - all genetic variation in allele frequences

# RESULTS
# VIF: all < 10
# adjR2 = 0.060 (null = 0.0083 with negatives as zeros)
# quotient real / null adjR2: 7.228916
# difference real - null adjR2:  0.0517
# ANOVAs insignificant for full model and each axis
#######################################################

# run RDA
Y_bd <- env.bd.pca.axes
X_bd <- afs_hell
rda_bd_ns <- rda(X_bd ~ ., data= Y_bd)
# Call: rda(formula = X_bd ~ PC1 + PC2, data = Y_bd)
# 
# Inertia Proportion Rank
# Total         0.0009431  1.0000000     
# Constrained   0.0003519  0.3731068    2
# Unconstrained 0.0005912  0.6268932    4
# Inertia is variance 
# 
# Eigenvalues for constrained axes:
#   RDA1       RDA2 
# 0.00022135 0.00013054 
# 
# Eigenvalues for unconstrained axes:
#   PC1        PC2        PC3        PC4 
# 0.00027714 0.00012685 0.00009775 0.00008950 

coef(rda_bd_ns)
# RDA1       RDA2
# PC1 0.0620812 -0.1212062
# PC2 0.1890803  0.0968460

# ANOVA for all axes at once
sig.full.rda_bd_ns  <- anova.cca(rda_bd_ns, parallel=getOption("mc.cores")) # default is permutation=999
sig.full.rda_bd_ns 
# Model: rda(formula = X_bd ~ PC1 + PC2, data = Y_bd)
# Df   Variance      F Pr(>F)
# Model     2 0.00035188 1.1903  0.251
# Residual  4 0.00059123  

# ANOVA per axis
sig.axis.rda_bd_ns <- anova.cca(rda_bd_ns, by="axis", parallel=getOption("mc.cores"))
sig.axis.rda_bd_ns
# Model: rda(formula = X_bd ~ PC1 + PC2, data = Y_bd)
# Df   Variance      F Pr(>F)
# RDA1      1 0.00022135 1.4975  0.328
# RDA2      1 0.00013054 0.8832  0.651
# Residual  4 0.00059123 

vif.cca(rda_bd_ns)
# PC1 PC2 
# 1   1 

RsquareAdj(rda_bd_ns)
# $r.squared
# [1] 0.3731068
# 
# $adj.r.squared
# [1] 0.05966021

#######################################################
# [RDA_temp] 
# - pop-based
# - partial RDA, conditioning for space
# - temp predictors into few PCs
# - all genetic variation in allele frequences

# RESULTS
# VIF: all < 10
# adjR2 = -0.11 (null = 0.0091 with negatives as zeros)
# quotient real / null adjR2: -12.09
# difference real - null adjR2: -0.12
# ANOVAs insignificant for full model and each axis
#######################################################

### temp env vars
subset_temp = subset(Env, 
                       select=c(Name,
                                BO2_tempmean_bdmean,
                                BO2_tempmin_bdmean,
                                BO2_tempmax_bdmean,
                                BO2_temprange_bdmean,
                                BO2_tempmean_ss,
                                BO2_tempmin_ss,
                                BO2_tempmax_ss,
                                BO2_temprange_ss))


# PCA on cv_temp environmental predictors, use just few that explain most variation
env_temp_pca <- prcomp(subset_temp[,2:ncol(subset_temp)], scale = TRUE)
env_temp_egvals <- env_temp_pca$sdev^2
KG_env_temp_egvals <- env_temp_egvals[env_temp_egvals > mean(env_temp_egvals)] 
retain_num_env_temp <- length(KG_env_temp_egvals)
env.temp.pca.axes <- as.data.frame(env_temp_pca$x[,1:retain_num_env_temp]) # 58.29% cumulative genetic variation explained
head(env.temp.pca.axes)

### which predictors are strongly associated with the first 3 axes?
envPred_temp_load_3PCs <- as_tibble(env_temp_pca$rotation[,1:3], rownames="EnvPred")
write_csv(envPred_temp_load_3PCs, "EnvPred_temp_loadings_3PCs.csv")
envPred_temp_load_3PCs_abs <- as_tibble(envPred_temp_load_3PCs)
envPred_temp_load_3PCs_abs[2:4] <- abs(envPred_temp_load_3PCs_abs[2:4])

# with the first
envPred_temp_load_PC1_abs <- arrange(envPred_temp_load_3PCs_abs, desc(PC1)) %>%
  select(EnvPred, PC1)

# second
envPred_temp_load_P2_abs <- arrange(envPred_temp_load_3PCs_abs, desc(PC2)) %>%
  select(EnvPred, PC2)

# run RDA
Y_temp <- env.temp.pca.axes
X_temp <- afs_hell
Z_temp <- scallop_dbmem  
rda_temp <- rda(X_temp ~ . + Condition(Z_temp), data= Y_temp)
# Call: rda(formula = X_temp ~ PC1 + PC2 + Condition(Z_temp), data = Y_temp)
# 
# Inertia Proportion Rank
# Total         0.0009431  1.0000000     
# Conditional   0.0002158  0.2287718    1
# Constrained   0.0002368  0.2510562    2
# Unconstrained 0.0004906  0.5201721    3
# Inertia is variance 
# 
# Eigenvalues for constrained axes:
#   RDA1       RDA2 
# 0.00013103 0.00010574 
# 
# Eigenvalues for unconstrained axes:
#   PC1        PC2        PC3 
# 0.00027546 0.00012466 0.00009046 

coef(rda_temp)
# RDA1       RDA2
# Z_temp  0.32475801 -0.3943314
# PC1    -0.23608005  0.1091831
# PC2     0.02172345 -0.3930561

# ANOVA for all axes at once
sig.full.rda_temp  <- anova.cca(rda_temp, parallel=getOption("mc.cores")) # default is permutation=999
sig.full.rda_temp
# Model: rda(formula = X_temp ~ PC1 + PC2 + Condition(Z_temp), data = Y_temp)
# Df   Variance     F Pr(>F)
# Model     2 0.00023678 0.724  0.727
# Residual  3 0.00049058 
 

# ANOVA per axis
sig.axis.rda_temp <- anova.cca(rda_temp, by="axis", parallel=getOption("mc.cores"))
sig.axis.rda_temp
# Model: rda(formula = X_temp ~ PC1 + PC2 + Condition(Z_temp), data = Y_temp)
# Df   Variance      F Pr(>F)
# RDA1      1 0.00013103 0.8013  0.806
# RDA2      1 0.00010574 0.6466  0.676
# Residual  3 0.00049058 

vif.cca(rda_temp)
# Z_temp      PC1      PC2 
# 2.826755 2.103706 1.723049 

RsquareAdj(rda_temp)
# $r.squared
# [1] 0.2510562
# 
# $adj.r.squared
# [1] -0.1148702

#######################################################
# [RDA_temp_ns] 
# - pop-based
# - NOT conditioning for space
# - cv and temp predictors into few PCs
# - all genetic variation in allele frequences

# RESULTS
# VIF: all < 10
# adjR2 = 0.14 (null = 0.0011, 0.018 with negatives as zeros)
# quotient real / null adjR2: 8.043955
# difference real - null adjR2: 0.1233377
# ANOVAs significant for full model and first axis
#######################################################

# run RDA
Y_temp <- env.cv_temp.pca.axes
X_temp <- afs_hell
rda_temp_ns <- rda(X_temp ~ ., data= Y_temp)
# Call: rda(formula = X_temp ~ PC1 + PC2, data = Y_temp)
# 
# Inertia Proportion Rank
# Total         0.0009431  1.0000000     
# Constrained   0.0003314  0.3513549    2
# Unconstrained 0.0006117  0.6486451    4
# Inertia is variance 
# 
# Eigenvalues for constrained axes:
#   RDA1       RDA2 
# 0.00021056 0.00012081 
# 
# Eigenvalues for unconstrained axes:
#   PC1        PC2        PC3        PC4 
# 0.00029424 0.00012667 0.00010095 0.00008989 

coef(rda_temp_ns)
# RDA1       RDA2
# PC1 -0.1394605 -0.1127412
# PC2  0.1885358 -0.2332182

# ANOVA for all axes at once
sig.full.rda_temp_ns  <- anova.cca(rda_temp_ns, parallel=getOption("mc.cores")) # default is permutation=999
sig.full.rda_temp_ns
# Model: rda(formula = X_temp ~ PC1 + PC2, data = Y_temp)
# Df   Variance      F Pr(>F)
# Model     2 0.00033137 1.0834  0.436
# Residual  4 0.00061175                  

# ANOVA per axis
sig.axis.rda_temp_ns <- anova.cca(rda_temp_ns, by="axis", parallel=getOption("mc.cores"))
sig.axis.rda_temp_ns
# Model: rda(formula = X_temp ~ PC1 + PC2, data = Y_temp)
# Df   Variance      F Pr(>F)
# RDA1      1 0.00021056 1.3768  0.472
# RDA2      1 0.00012081 0.7899  0.629
# Residual  4 0.00061175  

vif.cca(rda_temp_ns)
# PC1 PC2 
# 1   1 

RsquareAdj(rda_temp_ns)
# $r.squared
# [1] 0.3513549
# 
# $adj.r.squared
# [1] 0.02703242
