#!/usr/bin/Rscript



# Read in dedupe's results
dedupe.results <- read.csv('dedupe/output/restaurants_output.csv')

# Read in the fodors, zagats and ground truth respectively
fodors.data <- read.csv('datasets/restaurants/fodors.csv')
zagats.data <- read.csv('datasets/restaurants/zagats.csv')
ground.truth <- read.csv('magellan/py_entitymatching-master/py_entitymatching/datasets/end-to-end/restaurants/matches_fodors_zagats.csv')


restaurants.data <- rbind(
	fodors.data,
	zagats.data[!zagats.data$id %in% ground.truth$zagats_id,]
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






