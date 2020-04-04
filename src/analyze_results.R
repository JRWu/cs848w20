#!/usr/bin/Rscript



# Read in dedupe's results
dedupe.results <- read.csv('dedupe/output/restaurants_output.csv')

# Read in the fodors, zagats and ground truth respectively
fodors.data <- read.csv('datasets/restaurants/fodors.csv')
zagats.data <- read.csv('datasets/restaurants/zagats.csv')
ground.truth <- read.csv('datasets/restaurants/matches_fodors_zagats.csv')

# unique in zagats
z <- length(which(!zagats.data$id %in% ground.truth$zagats_id == TRUE))
# unique in fodors
f <- length(which(!fodors.data$id %in% ground.truth$fodors_id == TRUE))
g <- nrow(ground.truth)
sum(z,f,g)



restaurants.data <- rbind(
	fodors.data,
	zagats.data[!zagats.data$id %in% ground.truth$zagats_id,]
)



# Read in the record_linkage dataset(s)

abt <- read.csv('datasets/buy_sell/AbtBuy_Abt.csv')
buy <- read.csv('datasets/buy_sell/AbtBuy_Buy.csv')
abtbuy.common <- intersect(abt$id, buy$id)

length(which(!abt$id %in% abtbuy.common == TRUE))
length(which(!buy$id %in% abtbuy.common == TRUE))




# Create venn diagrams
# install.packages("VennDiagram")

library(VennDiagram)

zag <- c(as.character(rep(1:nrow(ground.truth))), paste('z',rep(1:z),sep=''))
fod <- c(as.character(rep(1:nrow(ground.truth))), paste('f',rep(1:f),sep=''))

venn.diagram(
	x = list(zag,fod),
	category.names = c("Zagats", "Fodors"),
	filename = 'writeup/figures/restaurants_venn.png',
	imagetype="png",
	cex=1.5
)
venn.diagram(
	x = list(abt$id,buy$id),
	category.names = c("ABT", "BUY"),
	filename = 'writeup/figures/abt_buy_venn.png',
	imagetype="png",
	cex=1.5
)
























# Misc
# length(unique(dedupe.results$Cluster.ID))
# nrow(fodors.data) + nrow(zagats.data) - nrow(ground.truth)




# Dedupe results from 1:533 are from FODORS
# Dedupe results from 534:864 are from ZAGATS
#ground.truth$fodors_id
#ground.truth$zagats_id
#dedupe.results
dedupe.fodors <- dedupe.results[dedupe.results$id %in% ground.truth$fodors_id,]
dedupe.zagats <- dedupe.results[dedupe.results$id %in% ground.truth$zagats_id,]

# False Negatives
# Dedupe says it is NOT a Duplicate when in reality it IS a duplicate
dedupe.fn <- dedupe.fodors$Cluster.ID == dedupe.zagats$Cluster.ID
dedupe.fn <- length(which(dedupe.fn == FALSE))


# False Positives
# Dedupe says it is TRULY a Duplicate when in reality it is NOT a Duplicate

# Number of Clusters reported by dedupe
dedupe.fp <- length(unique(c(dedupe.results$Cluster.ID)))
dedupe.fp <- abs(dedupe.fp - nrow(restaurants.data))






