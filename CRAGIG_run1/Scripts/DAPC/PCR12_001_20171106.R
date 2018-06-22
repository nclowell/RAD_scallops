# Let's first run a DAPC with all individuals and all loci


# Import these libraries
library(adegenet)
library(hierfstat)

# Set working directory
setwd("E:/PARCAL_ipyrad/PCR12_001_outfiles/new_outfiles/")

# Read in structure file, with a ".str" file extension
data_all_loci <-read.structure("PCR12_001_biall_maf_oneSNP_inames_wpop.str")

names(data_all_loci)
data_all_loci$pop

SantaBarbara_CA <- rep("CA1", 28)
EldInlet_WA <- rep("WA1",26) # sans reps
JamesIsland_WA <- rep("WA2",40)
BellaBella_BC <- rep("BC1",17)
AukeBay_AK <- rep("AK1",12) # these add to 66
YakutatBay_AK <- rep("AK2",29)
ChiniakBay_AK <- rep("AK3",27)

pop_groups <- as.factor(c(rep("CA1", 28),rep("WA1",26),rep("WA2",40),rep("BC1",17),rep("AK1",12),rep("AK2",29),rep("AK3",27)))                        
pop_labels <- c(SantaBarbara_CA,EldInlet_WA,JamesIsland_WA,BellaBella_BC,AukeBay_AK,YakutatBay_AK,ChiniakBay_AK)
pop_cols <- c("black","dodgerblue","chocolate3","deepskyblue","red","darkorchid4","forestgreen")


# Data exploration to find # PCs. Go through all of their prompts:
dapc_all <- dapc(data_all_loci,data_all_loci$pop)

# [1] Choose the number PCs to retain (>=1):
#     You will see a plot of cumulative variance by number retained PCs
#     Retain N/3 Prinicpal components
#     E.g., if x axis goes until 70, retain 7-/3 = 23.333 = 23
#     You can also get this number from the test_a_score plot, subtitle

# [2] Choose the number discriminant functions to retain (>=1):
#     You will see a fiery histogram with N number of bars
#     Retain the number of linear discriminants (I think that is == n.da)
#     

myclusters <- find.clusters(data_all_loci)
test_a_score <- optim.a.score(dapc_all) # this also gives you optimal number of PCs, subtitle of plot


dapc_all <- dapc(data_all_loci,data_all_loci$pop,n.pca=58,n.da=6) ##22 PC's is the optimal number

#2D plot
scatter(dapc_all,scree.da=FALSE,cellipse=0,leg=FALSE, label=c("CA_SantaBarbara","WA_EldInlet","WA_JamesIsland","BC_BellaBella","AK_AukeBay","AK_YakutatBay","AK_ChiniakBay"),
        posi.da="bottomleft",csub=2,col=pop_cols,cex=1,clabel=.7,solid=1)
#legend(x = -5, y = 2,bty='n',legend=c("CA1","WA1","WA2","BC1","AK1","AK2","AK3"),col=pop_cols,cex=1.3)

# by axis, 2,2 and 1,1
#scatter(dapc_all,2,2,scree.da=FALSE,cellipse=0,leg=FALSE,
#        posi.da="bottomleft",csub=2,col=pop_cols,cex=.8,clabel=1,solid=1)

