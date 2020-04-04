
a <- read.csv("AbtBuy_Abt.csv")
b <- read.csv("AbtBuy_Buy.csv")

a$name <- as.character(a$name)
b$name <- as.character(b$name)



a.tokens <- unique(
	unlist(
		lapply(as.list(a$name), function(x){strsplit(x,'')[[1]]})
	)
)
b.tokens <- unique(
	unlist(
		lapply(as.list(b$name), function(x){strsplit(x,'')[[1]]})
	)
)

# All tokens exist in A
a.tokens %in% b.tokens



a$id <- 1:length(a$id)

write.csv(a, 'MODIFIED_AbtBuy_Abt.csv', row.names=F)

#################################### ABT_BUY ###################################
#################################### ABT_BUY ###################################
#################################### ABT_BUY ###################################
##### Write the gold standard table for ABT_BUY
a <- read.csv("AbtBuy_Abt.csv")
b <- read.csv("AbtBuy_Buy.csv")

a <- a[unique(a$id),]
b <- b[b$id %in% a$id,]

a.names <- colnames(a)
b.names <- colnames(b)

final <- merge(a,b, by='id', all=T)

colnames(final) <- c('id',
	paste('ltable_',a.names[2:4],sep=''),
	paste('rtable_',b.names[2:4],sep='')
)

final$ltable_id <- final$id
final$rtable_id <- final$id
final$gold <- 1

final <- final[!duplicated(final$id),]

final.names <- colnames(final)
final.names[1] <- "_id"
colnames(final) <- final.names

write.csv(final, 'abtbuy_goldstandard.csv',row.names=F)


#################################### ABT_BUY ###################################
#################################### ABT_BUY ###################################
#################################### ABT_BUY ###################################
##### Write the gold standard table for RESTAURANT
a <- read.csv("fodors.csv")
b <- read.csv("zagats.csv")

matches <- read.csv("matches_fodors_zagats.csv")
a.not <- a[!(a$id %in% matches$fodors_id),]
b.not <- b[!(b$id %in% matches$zagats_id),]

final <- a[a$id %in% matches$fodors_id,]














#################################### LABEL #####################################
# Sample the labels
a <- read.csv("AbtBuy_Abt.csv")
b <- read.csv("AbtBuy_Buy.csv")


a.indicies <- sample(a$id,112)
if(length(a.indicies) == length(unique(a.indicies))){
	exit()# Quit if they are not the same
}


a.sample <- a[a.indicies,]
b.sample <- b[b$id %in% a.sample$id,]

a.sample <- a.sample[order(a.sample$id),]
b.sample <- b.sample[order(b.sample$id),]


colnames(a.sample) <- paste('ltable_',colnames(a.sample),sep='')
colnames(b.sample) <- paste('rtable_',colnames(b.sample),sep='')

final <- cbind(a.sample,b.sample)
final$gold <- 1


# Read in random rows from S
s <- read.csv('S.csv')
which(s$ltable_id == s$rtable_id)
s.ind <- sample(8:nrow(s),338) # Start from 8 because 7 is a duplicate

# Subset to the indicies sampled
s <- s[s.ind,]
s$gold <- 0	# These are mismatches, label them as such
s <- s[,-1] # drop index of X_ind because we generate new ones


# Combine
all <- rbind(s,final)

# Add artificial ID for Magellan
all$id <- 1:nrow(all)

# Save the resultant set
write.csv(all, 'G.csv',row.names=F)






g <- read.csv('G.csv')
g.ind <- sample(1:nrow(g),20)
g <- g[329:348,]
g

write.csv(g, 'G_sampled.csv',row.names=F)



##################################### FIG 2 ####################################
##################################### FIG 2 ####################################
##################################### FIG 2 ####################################
##################################### FIG 2 ####################################
rf.mag.active <- c(1.00, 1.00)
rf.mag.normal <- c(1.00, 1.00)
dedupe.active <- c(0.97, 0.034)

a <- t(as.data.frame(rf.mag.active))
b <- t(as.data.frame(rf.mag.normal))
c <- t(as.data.frame(dedupe.active))


final <- rbind(a,b,c)
colnames(final) <- c('precision','recall')
final <- t(final)

png('figure_2_barplot.png')
barplot(final,
	main='Precision & Recall Barplot for ABT_BUY',
	beside=TRUE,
	names.arg=c('EMSS','Magellan','Dedupe')
)
dev.off()

