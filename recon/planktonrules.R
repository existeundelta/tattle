library(e1071)
scores <- read.delim('scores.txt')
train <- sample(nrow(scores), 10000)
trainset <- scores[train,]
testset <- scores[-train,]
model <- svm(as.factor(planktonrules) ~ ., data=trainset)
predictions <- predict(model, newdata=testset)
mean(predictions == testset[,1])