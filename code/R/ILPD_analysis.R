library(psych)
library(mlbench)
library(Hotelling)
library(profileR)
library(ICSNP)
library(mvtnorm)
library(matlib)
library(MVN)


ILPD<-read.csv("ILPD.csv") #Read in data

#For loop prints how many patients are in each cohort, 100 in cohorts 1-5 and 83 in cohort 6.
for(i in 1:6){
  print(paste("Number of patients in cohort",i,"is:",length(which(ILPD[9]==i))))
}

#Number of females
print(length(which(ILPD[2]=="Female")))

#Patient with highest TB levles
which(ILPD$TB==max(ILPD$TB)) #patient with highest TB is row 167, Male belonging to 2nd cohort.

#Creating a drop name vector to remove from dataset. Then from this creating new data frame of quantative variables
col_drop <- c("Age","Gender","Label","Cohort")
ILPD_pre_mean<-ILPD[ , !(names(ILPD) %in% col_drop)]

#Sample mean vector
sample_mean_vector<-colMeans(ILPD_pre_mean)

#Applying variance function to columns of quant variables. lowest variance is AG ratio
variance_vector<- apply(ILPD_pre_mean,2,var)

#Correlation matrix
cor(ILPD_pre_mean)

#Pairs.panel correlation-scatterplot matrix with conf ints and density histograms for visualisation of normality
pairs.panels(ILPD_pre_mean,digits= 4,ci = TRUE,smoother = TRUE,hist.col = "Magenta",stars = TRUE) #Comment this out if it takes too long to run one downside of smoother being true is it takes a while
pairs.panels(ILPD_pre_mean,digits= 4,ci = TRUE,smoother = FALSE,hist.col = "Magenta",stars = TRUE,pch=".")

# a whole bunch of univariate qq plots
qqnorm(ILPD_pre_mean$TB, main="")
title("Normal Q-Q plot for TB", line=0.5)
qqline(ILPD_pre_mean$TB)

qqnorm(ILPD_pre_mean$DB, main="")
title("Normal Q-Q plot for DB", line=0.5)
qqline(ILPD_pre_mean$DB)

qqnorm(ILPD_pre_mean$TP, main="")
title("Normal Q-Q plot for TP", line=0.5)
qqline(ILPD_pre_mean$TP)

qqnorm(ILPD_pre_mean$ALB, main="")
title("Normal Q-Q plot for ALB", line=0.5)
qqline(ILPD_pre_mean$ALB)

qqnorm(ILPD_pre_mean$AG_Ratio, main="")
title("Normal Q-Q plot for AG Ratio", line=0.5)
qqline(ILPD_pre_mean$AG_Ratio)

#A whole bunch of univariate shapiro tests
shapiro.test(ILPD_pre_mean$TB)
shapiro.test(ILPD_pre_mean$DB)
shapiro.test(ILPD_pre_mean$TP)
shapiro.test(ILPD_pre_mean$ALB)
shapiro.test(ILPD_pre_mean$AG_Ratio)

#Testing normalit univately and mulitvariately with chi-squared qq plot. not univariate normal or multi variate normal
mvn(ILPD_pre_mean, subset = NULL, mvnTest = c("mardia"), covariance = TRUE, tol = 1e-25, alpha = 0.5,
    scale = FALSE, desc = TRUE, transform = "none", R = 1000,
    univariateTest = c("SW", "CVM", "Lillie", "SF", "AD"),
    univariatePlot = "none", multivariatePlot = "qq",
    multivariateOutlierMethod = "none", bc = FALSE, bcType = "rounded",
    showOutliers = FALSE, showNewData = FALSE)


#hotellings t2 provides answer, true mu does not equal 3,2,6,3,1
HotellingsT2(ILPD_pre_mean,mu= c(3,2,6,3,1))

#discriminant function.
a <- solve(cov(ILPD_pre_mean)) %*% (sample_mean_vector-c(3,2,6,3,1))
a

#starting profile plot
y_points<-sample_mean_vector
x_points<-c(1,2,3,4,5)

#Createing the actual plot
plot(x_points,y_points,pch = 3,col = 'red',xaxt = "n",main = "Sample profile plot",xlab="Observed Variables",ylab="Mean")
axis(1,at = 1:5,labels = colnames(ILPD_pre_mean))
lines(x_points,y_points,col = 'black',lty = 2)

#Function to see if profile is flat etc.
paos(ILPD_pre_mean)

#one way manova with idividual anova tests.
ILPD_oneway_manova <- manova(as.matrix(ILPD_pre_mean)~Cohort, data=ILPD)
summary(ILPD_oneway_manova,test='Wilks')
summary.aov(ILPD_oneway_manova)

#removing other cohorts from data
ILPD_2_5<- ILPD[-c(which(ILPD[9]==1),which(ILPD[9]==3),which(ILPD[9]==4),which(ILPD[9]==6)),]
ILPD_2_5_quant <- ILPD_2_5[ , !(names(ILPD_2_5) %in% col_drop)]

#New model only between cohorts 2 and 5. Again conducting manova and individual anova tests
ILPD_2_5_man <- manova(as.matrix(ILPD_2_5_quant)~Cohort,data = ILPD_2_5)
summary(ILPD_2_5_man,test="Wilks")
summary.aov(ILPD_2_5_man)

  #Further proof of means not being equal:
########################################################################################################################
#Isolating cohort 2
ILPD_2<-ILPD_2_5[-which(ILPD_2_5[9]==5),]
ILPD_2_quant <- ILPD_2[ , !(names(ILPD_2) %in% col_drop)]

#isolating cohort 5
ILPD_5<-ILPD_2_5[-which(ILPD_2_5[9]==2),]
ILPD_5_quant <- ILPD_5[ , !(names(ILPD_2) %in% col_drop)]

#means of cohorts 2 and 5 and then compared with hotellings t2 and a porfile plot
colMeans(ILPD_2_quant)
colMeans(ILPD_5_quant)
HotellingsT2(ILPD_2_quant,mu=colMeans(ILPD_5_quant))
HotellingsT2(ILPD_5_quant,mu=colMeans(ILPD_2_quant))

#Two sample profile plot we reject all H0's therefroe means are not equal between cohort 2 and 5
col_drop2 <- c("Age","Gender","Label")
ILPD_2_5_modified <- ILPD_2_5[ , !(names(ILPD_2_5) %in% col_drop2)]
ILPD_2_5_modified <- data.frame(sapply(ILPD_2_5_modified,as.numeric))
pbg(ILPD_2_5_modified[,1:5], factor(ILPD_2_5_modified[,6]),original.names = TRUE, profile.plot = TRUE)
summary(pbg(ILPD_2_5_modified[,1:5], factor(ILPD_2_5_modified[,6]),original.names = TRUE, profile.plot = TRUE))
  ########################################################################################################################

#Two way manova tests with interaction
ILPD_interaction_manova <- manova(cbind(TB,DB,TP,ALB,AG_Ratio)~Cohort*Gender, data=ILPD)
summary(ILPD_interaction_manova,test="Wilks")
summary.aov(ILPD_interaction_manova)

#Two manova with addative model
ILPD_add_manova <- manova(cbind(TB,DB,TP,ALB,AG_Ratio)~Cohort+Gender, data=ILPD)
summary(ILPD_add_manova)
summary.aov(ILPD_add_manova)









