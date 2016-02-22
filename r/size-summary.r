types = list.files("~/Desktop/stat-out", full.names=TRUE)

for(i in 1:length(types))
{
  type <- read.csv(types[i], header=FALSE)
  type <- type[type > 0]
  summary_file <- "~/Desktop/stat-res/summary"
  cat(basename(types[i]), file=summary_file, sep="\n", append=TRUE)
  cat(summary(type), file=summary_file, sep="\n", append=TRUE)
  cat("--------", file=summary_file, sep="\n", append=TRUE)
  
  if (length(unique(type)) <= 5) {
    cat(basename(types[i]), file="~/Desktop/stat-res/cluster-error.csv", sep="\n", append=TRUE)
    next
  }

  group <- kmeans(type, 5)
  op <- data.frame(type, group$cluster)
  names(op) <- c("size", "cluster")
  
  jpeg(file=paste("~/Desktop/stat-res/", basename(types[i]), sep=''))
  title = paste("File Size Variation For", basename(types[i]))
  plot(op$cluster, op$size, col=op$cluster, main = title)
  dev.off()
  
  sizes <- c()
  for(j in 1:5){
    sizes[j] <- max(op[op$cluster == j,])
  }
  
  sizes <- c(basename(types[i]), sort(sizes))
  write.table(matrix(sizes, nrow=1), file = "~/Desktop/stat-res/clusters.csv", sep = ",", row.names=FALSE, col.names = FALSE, append=TRUE)
}