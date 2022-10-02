window <- 60
numberPairs <- 2

library(glmnet)
library(caret)
library(randomForest)
library(MASS)
library(ggplot2)
library(pROC)


# Importation des données
indicators <- read.csv(paste0('data/indicatorsDataFrame', window, '_', numberPairs, '.csv'))
pairsStock <- read.csv(paste0('data/newVariableDataFrame', window, '_', numberPairs, '.csv'))
pairsToTrade <- read.csv(paste0('data/newVariableToTradeDataFrame', window, '_', numberPairs, '.csv'))



# Creation d'une base de donnees fake
set.seed(1)
n <- 10000
x1 <- runif(n, min=-5, max= 3)
x2 <- rnorm(n, 1, 3)
x3 <- rbeta(n, 1, 2)

nonLinear <- rep(0, n)
nonLinear[x1>1] <- 1
nonLinear[x1<(-3)] <- -2


y <- 0 + 4*x1 + 1*x2 + 12*x3 + x3*x1*10 + 
  3*x2*nonLinear**2 + 2*nonLinear + rnorm(n, 0, 7)


hist(y)

trainData <- data.frame("y"= y[1:floor(n*0.7)],
                         "x1" = x1[1:floor(n*0.7)],
                         "x2" = x2[1:floor(n*0.7)],
                        "x3" = x3[1:floor(n*0.7)])

testData <- data.frame( "y"= y[(floor(n*0.7)+1):n],
                        "x1" = x1[(floor(n*0.7)+1):n],
                        "x2" = x2[(floor(n*0.7)+1):n],
                        "x3" = x3[(floor(n*0.7)+1):n])

rm(x1, x2, x3, y, nonLinear, n)
## Fin de la création des données


### REGRESSION
# Interaction entre tout nos prédicteurs
trainXmat <- model.matrix(y ~ .^2, data = trainData)
testXmat <- model.matrix(y ~ .^2, data = testData)

## glm Gaussien AIC
set.seed(161)
AIC.mod1 <- glm(y ~ .^2, data=trainData)

AIC.mod1 <- stepAIC(AIC.mod1, k=2, direction='backward', trace=FALSE)


# Calcul du RMSE sur test
testPred.AIC <- as.vector(predict(AIC.mod1, newdata = testData, type = "response"))
testRMSE.AIC <- sqrt(mean((testData$y - as.vector(predict(AIC.mod1, newdata = testData, type = "response")))**2))
trainRMSE.AIC <- sqrt(mean((trainData$y - as.vector(predict(AIC.mod1, newdata = trainData, type='response')))**2))

print(c(paste0('AIC RMSE train: ', trainRMSE.AIC), paste('AIC RMSE test:', testRMSE.AIC)))

## Lasso Model
set.seed(161)
cv <- cv.glmnet(x      = trainXmat,
                y      = trainData$y,
                family = "gaussian",
                alpha  = 1,
                nfolds = 5) # cross validation
plot(cv)

las.mod1 <- glmnet(x      = trainXmat,
                   y      = trainData$y,
                   family = "gaussian",
                   lambda = cv$lambda.1se,
                   alpha  = 1) # Création du modèle avec meilleur lambda


coef.glmnet(las.mod1)  # Coefficient de régression Lasso

# Calcul du RMSE sur test
testPred.lasso <- as.vector(predict(las.mod1, newx = testXmat, type = "response"))
testRMSE.lasso <- sqrt(mean((testData$y - as.vector(predict(las.mod1, newx = testXmat, type = "response")))**2))
trainRMSE.lasso <- sqrt(mean((trainData$y - as.vector(predict(las.mod1, newx=trainXmat, type='response')))**2))

print(c(paste0('lasso RMSE train: ', trainRMSE.lasso), paste('lasso RMSE test:', testRMSE.lasso)))

## Ridge Model
set.seed(161)
cv <- cv.glmnet(x      = trainXmat,
                y      = trainData$y,
                family = "gaussian",
                alpha  = 0,
                nfolds = 5) # cross validation
plot(cv)

ridge.mod1 <- glmnet(x      = trainXmat,
                   y      = trainData$y,
                   family = "gaussian",
                   lambda = cv$lambda.1se,
                   alpha  = 0) # Création du modèle avec meilleur lambda


coef.glmnet(ridge.mod1)  # Coefficient de régression Lasso

# Calcul du RMSE sur test
testPred.ridge <- as.vector(predict(ridge.mod1, newx = testXmat, type = "response"))
testRMSE.ridge <- sqrt(mean((testData$y - as.vector(predict(ridge.mod1, newx = testXmat, type = "response")))**2))
trainRMSE.ridge <- sqrt(mean((trainData$y - as.vector(predict(ridge.mod1, newx=trainXmat, type='response')))**2))

print(c(paste0('ridge RMSE train: ', trainRMSE.ridge), paste('ridge RMSE test:', testRMSE.ridge)))

## Elastic Net Model, alpha=0.5
set.seed(161)
cv <- cv.glmnet(x      = trainXmat,
                y      = trainData$y,
                family = "gaussian",
                alpha  = 0.5,
                nfolds = 5) # cross validation
plot(cv)

elastic.mod1 <- glmnet(x      = trainXmat,
                     y      = trainData$y,
                     family = "gaussian",
                     lambda = cv$lambda.1se,
                     alpha  = 0.5) # Création du modèle avec meilleur lambda


coef.glmnet(elastic.mod1)  # Coefficient de régression Lasso

# Calcul du RMSE sur test
testPred.elastic <- as.vector(predict(elastic.mod1, newx = testXmat, type = "response"))
testRMSE.elastic <- sqrt(mean((testData$y - as.vector(predict(elastic.mod1, newx = testXmat, type = "response")))**2))
trainRMSE.elastic <- sqrt(mean((trainData$y - as.vector(predict(elastic.mod1, newx=trainXmat, type='response')))**2))

print(c(paste0('Elastic Net RMSE train: ', trainRMSE.elastic), paste('Elastic Net RMSE test:', testRMSE.elastic)))

## Random Forest Model
set.seed(161)
rf.mod1 <- train(y          = trainData$y,
                 x          = trainData[, colnames(trainData) != "y"],
                 method     = "rf", # random forest
                 trControl  = trainControl(method          = "cv", # Cross Validation
                                           number          = 5),
                 metric     = "RMSE",
                 tuneGrid   = expand.grid(mtry = c(2, 3)),
                 ntree      = 300,
                 importance = T)

rf.mod1
plot(rf.mod1) # Plot le tune Grid
plot(rf.mod1$finalModel) # plot le nombre d'arbres

testPred.rf <- as.vector(predict(rf.mod1$finalModel, newdata = testData, type = "response"))
testRMSE.rf <- sqrt(mean((testData$y - as.vector(predict(rf.mod1$finalModel, newdata = testData, type = "response")))**2))
trainRMSE.rf <- sqrt(mean((trainData$y - as.vector(predict(rf.mod1$finalModel, newdata = trainData, type='response')))**2))

print(c(paste0('Random Forest RMSE train: ', trainRMSE.rf), paste('Random Forest RMSE test:', testRMSE.rf)))

modelComparison <- data.frame("Model"=c("AIC", "Lasso", "Ridge", "Elastic Net", "Random Forest"),
           "Train RMSE" = c(trainRMSE.AIC, trainRMSE.lasso, trainRMSE.ridge, trainRMSE.elastic, trainRMSE.rf),
           "Test RMSE" = c(testRMSE.AIC, testRMSE.lasso, testRMSE.ridge, testRMSE.elastic, testRMSE.rf))
print(modelComparison)

chosenModel <- modelComparison$Model[which.min(modelComparison$Test.RMSE)]
print(paste('Chosen model:', chosenModel))

finalModel <- list(AIC.mod1, las.mod1, ridge.mod1, elastic.mod1, rf.mod1)
finalPred <- list(testPred.AIC, testPred.lasso, testPred.ridge, testPred.elastic, testPred.rf)

finalModel <- finalModel[[which.min(modelComparison$Test.RMSE)]]
finalPred <- finalPred[[which.min(modelComparison$Test.RMSE)]]


ggplot(data.frame('pred'=finalPred,
                  'y' = testData$y), aes(x=pred, y=y))+
  geom_point(alpha=0.5)+
  geom_abline(slope=1, col='red')+
  theme_bw()+
  ggtitle(paste('Vrai valeurs en fonction des prédictions du modèle', chosenModel))+
  xlab('Prediction')+
  ylab('y')
  

### CLASSIFICATION
# Interaction entre tout nos prédicteurs
trainData$y <- ifelse(trainData$y > 0, 1, 0)
testData$y <- ifelse(testData$y > 0, 1, 0)


trainXmat <- model.matrix(y ~ .^2, data = trainData)
testXmat <- model.matrix(y ~ .^2, data = testData)

## glm binomial AIC
set.seed(161)
AIC.mod2 <- glm(y ~ .^2, family='binomial', data=trainData)

AIC.mod2 <- stepAIC(AIC.mod2, k=2, direction='backward', trace=FALSE)


# Calcul du AUC
testPred.AIC <- as.vector(predict(AIC.mod2, newdata = testData, type = "response"))
testAUC.AIC <- roc(testData$y ~ testPred.AIC)
trainAUC.AIC <- roc(trainData$y ~ as.vector(predict(AIC.mod2, newdata = trainData, type = "response")))

print(c(paste0('AIC AUC train: ', trainAUC.AIC$auc), paste('AIC AUC test:', testAUC.AIC$auc)))

## Lasso Model
set.seed(161)
cv <- cv.glmnet(x      = trainXmat,
                y      = trainData$y,
                family = "binomial",
                alpha  = 1,
                nfolds = 5) # cross validation
plot(cv)

las.mod2 <- glmnet(x      = trainXmat,
                   y      = trainData$y,
                   family = "binomial",
                   lambda = cv$lambda.1se,
                   alpha  = 1) # Création du modèle avec meilleur lambda


coef.glmnet(las.mod2)  # Coefficient de régression Lasso

# Calcul du AUC
testPred.lasso <- as.vector(predict(las.mod2, newx = testXmat, type = "response"))
testAUC.lasso <- roc(testData$y ~ testPred.lasso)
trainAUC.lasso <- roc(trainData$y ~ as.vector(predict(las.mod2, newx = trainXmat, type = "response")))


print(c(paste0('Lasso AUC train: ', trainAUC.lasso$auc), paste('Lasso AUC test:', testAUC.lasso$auc)))

## Ridge Model
set.seed(161)
cv <- cv.glmnet(x      = trainXmat,
                y      = trainData$y,
                family = "binomial",
                alpha  = 0,
                nfolds = 5) # cross validation
plot(cv)

ridge.mod2 <- glmnet(x      = trainXmat,
                     y      = trainData$y,
                     family = "binomial",
                     lambda = cv$lambda.1se,
                     alpha  = 0) # Création du modèle avec meilleur lambda


coef.glmnet(ridge.mod2)  # Coefficient de régression Lasso

# Calcul du AUC
testPred.ridge <- as.vector(predict(ridge.mod2, newx = testXmat, type = "response"))
testAUC.ridge <- roc(testData$y ~ testPred.ridge)
trainAUC.ridge <- roc(trainData$y ~ as.vector(predict(ridge.mod2, newx = trainXmat, type = "response")))

print(c(paste0('Ridge AUC train: ', trainAUC.ridge$auc), paste('Ridge AUC test:', testAUC.ridge$auc)))

## Elastic Net Model, alpha=0.5
set.seed(161)
cv <- cv.glmnet(x      = trainXmat,
                y      = trainData$y,
                family = "binomial",
                alpha  = 0.5,
                nfolds = 5) # cross validation
plot(cv)

elastic.mod2 <- glmnet(x      = trainXmat,
                       y      = trainData$y,
                       family = "binomial",
                       lambda = cv$lambda.1se,
                       alpha  = 0.5) # Création du modèle avec meilleur lambda


coef.glmnet(elastic.mod2)  # Coefficient de régression Lasso

# Calcul du AUC 
testPred.elastic <- as.vector(predict(elastic.mod2, newx = testXmat, type = "response"))
testAUC.elastic <- roc(testData$y ~ testPred.elastic)
trainAUC.elastic <- roc(trainData$y ~ as.vector(predict(elastic.mod2, newx = trainXmat, type = "response")))

print(c(paste0('Elastic Net AUC train: ', trainAUC.elastic$auc), paste('Elastic Net AUC test:', testAUC.elastic$auc)))

## Random Forest Model
set.seed(161)
trainYN <- trainData
testYN <- testData

trainYN$y <- ifelse(trainYN$y == 1, "Y", "N")
testYN$y <- ifelse(testYN$y == 1, "Y", "N")

rf.mod2 <- train(y          = trainYN$y,
                 x          = trainYN[, colnames(trainYN) != "y"],
                 method     = "rf", # random forest
                 trControl  = trainControl(method          = "cv", # Cross Validation
                                           number          = 5,
                                           summaryFunction = twoClassSummary,
                                           classProbs = TRUE),
                 metric     = "ROC",
                 tuneGrid   = expand.grid(mtry = c(2, 3)),
                 ntree      = 300,
                 importance = T)


rf.mod2
plot(rf.mod2) # Plot le tune Grid
plot(rf.mod2$finalModel) # plot le nombre d'arbres

# Calcul du AUC
testPred.rf <- as.vector(predict(rf.mod2, newdata = testYN, type = "prob"))$Y
testAUC.rf <- roc(testData$y ~ testPred.rf)
trainAUC.rf <- roc(trainData$y ~ as.vector(predict(rf.mod2, newdata = trainYN, type = "prob")$Y))

print(c(paste0('Random Forest AUC train: ', trainAUC.rf$auc), paste('Random Forest AUC test:', testAUC.rf$auc)))

# Comparaison des modèles de classification
modelComparison <- data.frame("Model"=c("AIC", "Lasso", "Ridge", "Elastic Net", "Random Forest"),
                              "Train AUC" = c(trainAUC.AIC$auc, trainAUC.lasso$auc, trainAUC.ridge$auc, trainAUC.elastic$auc, trainAUC.rf$auc),
                              "Test AUC" = c(testAUC.AIC$auc, testAUC.lasso$auc, testAUC.ridge$auc, testAUC.elastic$auc, testAUC.rf$auc))
print(modelComparison)

chosenModel <- modelComparison$Model[which.max(modelComparison$Test.AUC)]
print(paste('Chosen model:', chosenModel))

finalModel <- list(AIC.mod2, las.mod2, ridge.mod2, elastic.mod2, rf.mod2)
finalPred <- list(testPred.AIC, testPred.lasso, testPred.ridge, testPred.elastic, testPred.rf)

finalModel <- finalModel[[which.min(modelComparison$Test.AUC)]]
finalPred <- finalPred[[which.min(modelComparison$Test.AUC)]]

#### CHOISIR LE THRESHOLD
threshold <- 0.5
thresholdPred <- ifelse(finalPred>threshold, 'Y', 'N')
confMatrix <- confusionMatrix(data = factor(thresholdPred), reference = factor(testYN$y), positive = "Y")
confMatrix$table

plot(list(testAUC.AIC, testAUC.lasso, testAUC.ridge, testAUC.elastic, testAUC.rf)[[which.min(modelComparison$Test.AUC)]],
     main=paste(paste('Test data ROC for', chosenModel), 'model'))
text(0.4, 0.4, labels=paste('Test AUC:', round(modelComparison$Test.AUC[which.min(modelComparison$Test.AUC)], 4)))

