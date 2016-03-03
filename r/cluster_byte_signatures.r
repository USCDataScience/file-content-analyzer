signatures <- read.csv("/Users/nithinkrishna/Desktop/text-plain")
head(signatures)
signatures.matrix <- data.matrix(signatures[3:258])
names(signatures.matrix) <- NULL

kmean <-kmeans(signatures.matrix, 5)

signatures.frame <- data.frame(signatures.matrix, as.numeric(kmean$cluster))
head(signatures.frame)

names(signatures.frame) <- c(1:257)

write.table(signatures.frame[1:70000,], "/Users/nithinkrishna/Desktop/text-plain-train",col.names = F, row.names = F, sep=",")
write.table(signatures.frame[70000:90000,], "/Users/nithinkrishna/Desktop/text-plain-test",col.names = F, row.names = F, sep=",")
write.table(signatures.frame[90000:100000,], "/Users/nithinkrishna/Desktop/text-plain-validate",col.names = F, row.names = F, sep=",")


getCluster = function(n){
  c <- c(kmean$centers[n,])
  names(c) <- NULL
  return(c)
}

write.table(matrix(getCluster(1), nrow=1), file = "~/Desktop/tp1", sep = ",", row.names=FALSE, col.names = FALSE, append=FALSE)
write.table(matrix(getCluster(2), nrow=1), file = "~/Desktop/tp2", sep = ",", row.names=FALSE, col.names = FALSE, append=FALSE)
write.table(matrix(getCluster(3), nrow=1), file = "~/Desktop/tp3", sep = ",", row.names=FALSE, col.names = FALSE, append=FALSE)
write.table(matrix(getCluster(4), nrow=1), file = "~/Desktop/tp4", sep = ",", row.names=FALSE, col.names = FALSE, append=FALSE)
write.table(matrix(getCluster(5), nrow=1), file = "~/Desktop/tp5", sep = ",", row.names=FALSE, col.names = FALSE, append=FALSE)
