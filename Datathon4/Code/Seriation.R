library(seriation)

d <- scan('in.txt')

d <- matrix(d, ncol = 191, byrow = TRUE)

# print(dim(d))

d <- as.dist(d)

o <- seriate(d,method="HC")

pimage(d,o,main="HC")

# res <- as.dist(res)

# pimage(res,main="BEA")
# or <- get_order(o)

# m <- permute(d,o)

# m <- as.matrix(m)

# write.csv(or,"output/TSP/or.csv")
# write.csv(m,"output/TSP/out.csv")


# methods <- c("VAT","R2E", "HC", "OLO", "TSP")
# o <- sapply(methods, FUN = function(m) seriate(d, m))

# o <- ser_align(o)
# for(s in o) pimage(d, s, main = get_method(s), key = FALSE)

# hmap(d,method="HC", margin =c(7, 4), cexCol=1, labRow = FALSE)

 # hmap(d,method="VAT", control = list(rep = 10))

# l <- kmeans(d, 3)$cluster

# res <- dissplot(d, method="R2E")

# print(res)
