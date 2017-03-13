# Let's first run a DAPC with all individuals and all loci

data_all_loci <-read.genepop("doublet.gen")

names(data_all_loci)
data_all_loci$pop

WA_Strait <- rep("WA1",26)
WA_SanJuans <- rep("WA2",15)
WA_Dabob <- rep("WA3", 11)
AK <- rep("AK1",7)
CA_Catalina_06seg <- rep("CA1",12) # these add to 71!


pop_groups <- as.factor(c(rep("WA1",26),rep("WA2",15),rep("WA3", 11),rep("AK1",7),rep("CA1",12)))
                        
pop_labels <- c(WA_Strait,WA_SanJuans,WA_Dabob,AK,CA_Catalina)

pop_cols <- c("black","dodgerblue","tomato","deepskyblue","red")

dapc_all <- dapc(data_all_loci,data_all_loci$pop,n.pca=465,n.da=8) ##Retain all, then identify optimal number by optim.a.score
test_a_score <- optim.a.score(dapc_all)
dapc_all <- dapc(data_all_loci,data_all_loci$pop,n.pca=25,n.da=8) ##63 PC's is the optimal number

#2D plot
scatter(dapc_all,scree.da=FALSE,cellipse=0,leg=FALSE,label=c("WA1", "WA2","WA3","AK1","CA1"),
        posi.da="bottomleft",csub=2,col=pop_cols,cex=1.5,clabel=1,pch=c(18,15,15,16,16),solid=1)
legend(x = -4, y = 2,bty='n',legend=c("WA1", "WA2","WA3","AK1","CA1"),pch=c(18,15,15,16,16),col=pop_cols,cex=1.3)
