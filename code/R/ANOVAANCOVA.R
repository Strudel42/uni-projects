#Libraries needed for data analysis
library(readxl) 
library(car)
library(MASS)
library(Hmisc)
library(ggplot2)
library(gridExtra)
library(BaylorEdPsych)#This is being used instead of DescTools as PseudoR2 would not work inside function from DescTools
library(ROCR)
library(gbm)
library(ResourceSelection)
library(mlbench)

data_in <- read_excel("Ancova_Basketball.xlsx",skip = 2)
data_in[1]<- NULL
data_pre <- data_in[, -c(4:6)]
colnames(data_pre)<-c('EU 1','EU 2','EU 3')
data_post <- data_in[, -c(1:3)]
df <- data.frame(stack(data_pre)[2],stack(data_pre)[1],stack(data_post)[1])
colnames(df) <- c('group','pre_value','post_value')


#checking normality
shapiro.test(subset(df,group == "EU 1")$post_value)
shapiro.test(subset(df,group == "EU 2")$post_value)
shapiro.test(subset(df,group == "EU 3")$post_value)

#checking homogenaity of variance
leveneTest(df$post_value ~ df$group,center = mean)

group <- df$group
post_value <- df$post_value
pre_value <- df$pre_value

anova_ancova <- function(factor_var,cont_var,covariate,ow_anova = TRUE,ancova = TRUE,comparison = TRUE,plots = TRUE){
  ########################################### How to use this function ###########################################
  # Your data should look like the above formatted data (type View(df) to inspect the structure).                #
  # Next we need take inputs for our arguments.                                                                  #
  # In our case they are:                                                                                        #
  # df$group (or group) as our factor variable                                                                   #
  # df$post_value (or post_value) as our cont_var (continous variable)                                           #
  # df$pre_value (or pre_value) as our covariate                                                                 #
  # ow_anova, ancova,comparison and plots are all optional and will simply disable parts of the code if false    #
  # Eg if plots = FALSE then no plots will appear, comparison is to show how the covariate impacts the model     #
  ################################################################################################################
  N <- c(length(factor_var)/3,length(factor_var)/3,length(factor_var)/3) # this number is used for the number of repetitions in the plot for colouring plot points

  if(ow_anova==TRUE){
    #ow_anova stands for one way anova prints summary and can do plots
    
    ow_anova1 <- summary(aov(cont_var~factor_var))
    print(ow_anova1)
    par(mfrow=c(1,2))
    if(plots == TRUE){
      boxplot(cont_var~factor_var,xlab = "Group",ylab ="Pre treatment" )
      boxplot(covariate~factor_var,xlab = "Group",ylab = "Post treatment")
    }
    
  }
  if(ancova == TRUE){
    ##similar to ow_anova, ancova prints a summary and can plot an anova plot as well
    
    ancova <- summary(aov(cont_var~factor_var+covariate))
    print(ancova)
    if(plots == TRUE){
      par(mfrow=c(1,1))
      mod1 <- lm(cont_var~factor_var)
      mod2 <- lm(cont_var~factor_var+covariate)
      Res <- summary(mod2)
      coeffs <- coef(Res)
      group_1_intercept <- coeffs[1,1]
      group_2_intercept <- coeffs[2,1] + group_1_intercept
      group_3_Intercept <- coeffs[3,1] + group_1_intercept
      slope <- coeffs[4,1]
      
      plot(cont_var~covariate,pch = rep(c(3,17,19),N),col = rep(c("green","red","blue"),N),main="Ancova",xlab = "pre value",ylab = "Post value")
      legend(x="topleft",legend=levels(factor_var),pch = c(3,17,19),col=c("green","red","blue"))
      abline(group_1_intercept,slope,col="green")
      abline(group_2_intercept,slope,col="red")
      abline(group_3_Intercept,slope,col="blue")
    }
  }
  if(comparison == TRUE){
    # a comparison between both models determining if we truly have a covariate
    mod1 <- lm(cont_var~factor_var)
    mod2 <- lm(cont_var~factor_var+covariate)
    anova(mod1,mod2)
  }
  
  
}

data2 <- mtcars
data2$wt <- NULL
data2$qsec <- NULL
data2$vs <- NULL
data2$gear <- NULL
data2$drat <- NULL
data2$hp<- NULL
data2$am <- data2$am+1 #am is by default numeric so this is to make sure it basically works inside the function (y=0 or y=1)

data(Mroz)
data3 <- Mroz
data3$lfp<- as.factor(data3$lfp)

data(Ionosphere)
data4<-Ionosphere
data4$V1<-NULL
data4$V2<-NULL
data4$Class <- as.factor(data4$Class)


logistic_regression <- function(outcome,mydata,plots=TRUE,summaries=TRUE,step_mode = "backward"){
  ################################################### How to use this function ###################################################
  # This function performs a logistical regression analysis comprising of vareious plots and metrics to help us analse our data. #
  #                                                                                                                              #
  # Outcome is the variable we want to try and predict so say we want to predict an outcome based on various predictors eg:      #
  # in the mtcars dataset you may want to try and predict a cars transmission type based on its miles per gallon weight etc.     #
  #                                                                                                                              #
  # Mydata is fairly self explanatory it is an input for your dataset,                                                           #
  # Summaries is just an output for whether or not you wish to see the summaries in the console as you may find it cluttering    #
  #                                                                                                                              #
  # step_mode is the direction selection for the stepAIC function NOTE that forward selection is not available                   #
  #                                                                                                                              #
  # An example of this functions use is would be logistic_regression(lfp,data3) or a better one logistic_regression(Class,data4) #
  # Trying these you will see it produces some nice plots and metrics on these datasets from the mlbench library                 #
  ################################################################################################################################
  
  #This is to make sure the outcome variable does not appear in the glm function (specifically the nulling of the outcome variable collumn)
  outcome <- deparse(substitute(outcome))
  d<- mydata[,outcome]
  levels(d)<-c(0,1)
  mydata[,outcome]<- NULL
  #note d is just the outcome variable and i have chosen to keep it as a factor variable, therefore you will see as.numeric(d)-1 for the numeric vector of 1's and 0's
  
  deparse(substitute(step_mode))
  if(step_mode=="backward"){
    logit_model <- glm((as.numeric(d)-1)~.,data=mydata,family="binomial")
    fitted_model<-stepAIC(logit_model,direction = "backward")
  }else if(step_mode=="both"){
    logit_model <- glm((as.numeric(d)-1)~.,data=mydata,family="binomial")
    fitted_model<-stepAIC(logit_model,direction = "both")
  }
  
  #prediction of models
  ## NOTE pred1 is the fitted model from the stepAIC function and pred2 is your base model (logit_model)
  pred1 <- predict(fitted_model,type="response")#fitted
  pred2 <- predict(logit_model,type="response")#full
  
  
  if(summaries == TRUE){
    print(summary(logit_model))
    print(summary(fitted_model))
  }
  #print("Fitted model R2")
  #print(PseudoR2(fitted_model))
  #print("Full model R2")
  #print(PseudoR2(logit_model))
  
  #prediction objects used later for ROC curve plots
  pred.obj1 <- prediction(predictions = pred1,labels = as.numeric(d)-1)
  pred.obj2 <- prediction(predictions = pred2,labels = as.numeric(d)-1)
  perf1 <- performance(pred.obj1,measure="tpr",x.measure="fpr")#fitted model
  perf2 <- performance(pred.obj2,measure="tpr",x.measure="fpr")#full model
  
  #somers test for AUC values ## TO DO aplpy c values to legend on ROC plot
  som1<-somers2(pred1,as.numeric(d)-1)#fitted model
  som2<-somers2(pred2,as.numeric(d)-1)#full
  print("Fitted model somers")
  print(som1)
  print("Full model somers")
  print(som2)
  
  #Hosmer-Lemeshow test
  print("Fitted model Hosmer-Lemeshow test:")
  print(hoslem.test(as.numeric(d)-1,pred1))
  print("Full model Hosmer-Lemeshow test:")
  print(hoslem.test(as.numeric(d)-1,pred2))
  
  if(plots==TRUE){
    
    #Boxplots of predicted values with respect to outcome variable (discrimination plots)
    data_plot <- cbind(mydata,pred1,pred2)
    p1 <- ggplot(data_plot,aes(as.factor(d),pred1))+geom_boxplot()+xlab(outcome)+ylab("Fitted model")
    p2 <- ggplot(data_plot,aes(as.factor(d),pred2))+geom_boxplot()+xlab(outcome)+ylab("Full model")
    grid.arrange(p1,p2)
    
    #ROC curve plot
    par(mfrow=c(1,1))
    plot(perf1,col="orange",lwd=2)
    plot(perf2,col="darkviolet",lwd=2,add=TRUE)
    fitted_model_AUC <- c("Fitted Model AUC:",round(som1["C"],digits=5))
    full_model_AUC <- c("Full Model AUC:",round(som2["C"],digits = 5))
    legend(x="bottomright",title = "Model AUC",legend = c(paste(fitted_model_AUC,collapse = ' '),paste(full_model_AUC,collapse = ' ')),col = c("orange","darkviolet"),lty=1:1, cex=1.25,bg="grey",lwd = 2)
    
    #Calibration plots for Hosmer
    par(mfrow=c(2,1))
    calibrate.plot(as.numeric(d)-1,pred1,main="Fitted model")
    calibrate.plot(as.numeric(d)-1,pred2,main="Full model")
  }
}


