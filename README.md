# Collaborative Filtering - Regression with Latent Factors

Collaborative Filtering: This approach, build a model from past behaviors, comparing items or users trough ratings, and in this case a Regression with Latent Factors technique can extract k features to predict the missing values. The Stochastic Gradient Descent is used to find minimum loss value. The function returns: the prediction of the missing data, the users features weights, the items features weights and the rmse (root mean square error).

* Xdata = Dataset Attributes. A matrix with users ratings about a set of items.

* mean_centering = "none", "row", "column", "global". If "none" is selected then no centering is made, if "row" is selected then a row mean centering is performed,  if "column" is selected then a column mean centering is performed and if "global" is selected then a global centering (matrix mean) is performed. The default value is "none".

* features = Total number of features to be extracted. The default value is 2.

* iterations = The total number of iterations. The default value is 1000.

* alpha = The learning rate. The default value is 0.01.
