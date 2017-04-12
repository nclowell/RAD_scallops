# Let's first run a DAPC with all individuals and all loci


# Import these libraries
library(adegenet)
library(hierfstat)


setwd("C:/Users/Natalie Lowell/Desktop")
data_all_loci <-read.genepop("just_WA_Genepop.gen")

names(data_all_loci)
data_all_loci$pop

WA_Dabob <- rep("WA3", 11)
WA_SanJuans <- rep("WA2",10) # sans reps
WA_Strait <- rep("WA1",26) # these add to 66






pop_groups <- as.factor(c(rep("WA3", 11),rep("WA2",10),rep("WA1",26)))                        
# pop_labels <- c(WA_Dabob,WA_SanJuans,WA_Strait)
pop_cols <- c("red","green","darkblue")


# Data exploration to find # PCs. Go through all of their prompts:
dapc_all <- dapc(data_all_loci,data_all_loci$pop)

16# [1] Choose the number PCs to retain (>=1):
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


dapc_all <- dapc(data_all_loci,data_all_loci$pop,n.pca=16,n.da=2) ##22 PC's is the optimal number

#2D plot
scatter(dapc_all,scree.da=FALSE,cellipse=0,leg=FALSE, label = c("1","2","3"),
        posi.da="bottomleft",csub=2,col=pop_cols,cex=1.5,pch=c(15,15,15),solid=1)
# legend(x = -5, y = 2,bty='n',pch=c(15,15,15),col=pop_cols,cex=1.3)
