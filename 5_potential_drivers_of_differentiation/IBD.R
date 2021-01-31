#################################################################################
# IBD using crowfly and inwater distances 
# 20200103 NL

#################################################################################
# get packages into R
library(geosphere)
library(dplyr)
library(viridis)
library(ggplot2)
library(vegan)

#################################################################################

setwd("E:/dD_cragig_mox_20191205/filtering/analyses/IBD/")

#################################################################################

# read in file with lat & long, pairwise FST, etc.
cragig_data <- read.csv("cragig_alllocifst_and_inwaterdist_20191216.csv")

#################################################################################
# mantel takes two arrays
# - (1) pairwise distance matrix
# - (2) pairwise FST matrix
# Eleni's code adapted below to make these

# save the character values of the population names
pop_name <- with(cragig_data, sort(unique(c(as.character(pop1),
                                         as.character(pop2)))))

#create some  empty 2-D  arrays to hold the pairwise data
dist_array<- array(data = 0, dim = c(length(pop_name), length(pop_name)), 
                    dimnames = list(pop_name, pop_name))

fst_array <- array(data = 0, dim = c(length(pop_name), length(pop_name)), 
                   dimnames = list(pop_name, pop_name))

crow_dist_array <- array(data = 0, dim = c(length(pop_name), length(pop_name)), 
                         dimnames = list(pop_name, pop_name))

# save some vectors of the positions of first matches of the first argument to the second
i <- match(cragig_data$pop1, pop_name)
j <- match(cragig_data$pop2, pop_name)

# linearize Fst, add column to dataframe
cragig_data <- cragig_data %>% 
  rowwise() %>%
  mutate(linearized_fst = (fst/(1-fst)))

# make inwater distance as numeric
cragig_data$inwater_dist_km = as.numeric(cragig_data$inwater_dist_km)
class(cragig_data$inwater_dist_km)

# add as crow flies
cragig_data <- cragig_data %>% 
  rowwise() %>%
  mutate(km2 = (distVincentyEllipsoid(c(pop1long, pop1lat), c(pop2long, pop2lat))/1000))

# populate the empty arrays with data saved in the vectors
dist_array[cbind(i,j)] <- dist_array[cbind(j,i)] <- cragig_data$inwater_dist_km
fst_array[cbind(i,j)] <- fst_array[cbind(j,i)] <- cragig_data$linearized_fst
crow_dist_array[cbind(i,j)] <- crow_dist_array[cbind(j,i)] <- cragig_data$km2

write.csv(dist_array, "inwater_dist_array_20191216.csv")
write.csv(fst_array, "cragig_alllocifst_array_20191216.csv")
write.csv(crow_dist_array, "crow_dist_array_2020103.csv")

# run mantel test, inwater
mantel_results <- mantel(dist_array, fst_array, method="pearson", permutations=10000)

# Mantel statistic based on Pearson's product-moment correlation 
# 
# Call:
# mantel(xdis = dist_array, ydis = fst_array, method = "pearson",      permutations = 10000) 
# 
# Mantel statistic r: -0.5171 
# Significance: 0.99206 
# 
# Upper quantiles of permutations (null model):
# 90%   95% 97.5%   99% 
# 0.273 0.336 0.401 0.475 
# Permutation: free
# Number of permutations: 5039

#################################################################################

ggplot(data = cragig_data, aes(x=inwater_dist_km, y=linearized_fst)) + #specify dataframe
  geom_point( size = 3, alpha = 0.9) +
  ylab(expression(italic(F[ST]/(1-F[ST])))) +                           #set labels for the axes and title
  xlab("Distance (km)")  +
  geom_smooth(method = "lm") + # add regression line
  theme_classic()

########################################################################
# linear regression to get slope of line

lm_results <- lm(cragig_data$linearized_fst~cragig_data$inwater_dist_km)
lm_results$coefficients

# (Intercept) cragig_data$inwater_dist_km 
# 3.875009e-03                3.765970e-06 

# so slope is 3.765970e-06

########################################################################
# crow flies, Mantel test
########################################################################

crow_mantel_results <- mantel(crow_dist_array, fst_array, method="pearson", permutations=10000)
crow_mantel_results

# Mantel statistic based on Pearson's product-moment correlation 
# 
# Call:
# mantel(xdis = crow_dist_array, ydis = fst_array, method = "pearson",      permutations = 10000) 
# 
# Mantel statistic r: 0.07801 
# Significance: 0.3621 
# 
# Upper quantiles of permutations (null model):
# 90%   95% 97.5%   99% 
# 0.285 0.332 0.401 0.476 
# Permutation: free
# Number of permutations: 5039

crow_lm_results <- lm(cragig_data$linearized_fst~cragig_data$km2)
crow_lm_results$coefficients

# > crow_lm_results$coefficients
# (Intercept) cragig_data$km2 
# 8.544793e-04    4.874621e-08 

