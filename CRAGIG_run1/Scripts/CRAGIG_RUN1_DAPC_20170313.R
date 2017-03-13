# Let's first run a DAPC with all individuals and all loci

data_all_loci <-read.genepop("doublet.gen")

names(data_all_loci)
data_all_loci$pop

WA_Dabob <- rep("WA3", 11)
WA_SanJuans <- rep("WA2",14) # missing one for some reason! it's not even in the first genepop prior to filtering...
AK <- rep("AK1",7)
CA_Catalina_06seg <- rep("CA1",12) # these add to 71!
WA_Strait <- rep("WA1",26)






pop_groups <- as.factor(c(rep("WA3", 11),rep("WA2",14),rep("AK1",7),rep("CA1",12),rep("WA1",26)))
                        
pop_labels <- c(WA_Dabob,WA_SanJuans,AK,CA_Catalina,WA_Strait)

pop_cols <- c("black","dodgerblue","tomato","deepskyblue","red")


#Data exploration to find # PCs. Go through all of their stoopid prompts.
dapc_all <- dapc(data_all_loci,data_all_loci$pop)
# retain N/3 Prinicpal components
# Look at histogram; retain given number of linear discriminants (I think that is == n.da)
myclusters <- find.clusters(data_all_loci)
test_a_score <- optim.a.score(dapc_all)


dapc_all <- dapc(data_all_loci,data_all_loci$pop,n.pca=22,n.da=4) ##22 PC's is the optimal number

#2D plot
scatter(dapc_all,scree.da=FALSE,cellipse=0,leg=FALSE,label=c("WA1", "WA2","WA3","AK1","CA1"),
        posi.da="bottomleft",csub=2,col=pop_cols,cex=1.5,clabel=1,pch=c(18,15,15,16,16),solid=1)
legend(x = -5, y = 2,bty='n',legend=c("WA1", "WA2","WA3","AK1","CA1"),pch=c(18,15,15,16,16),col=pop_cols,cex=1.3)
