############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Course: Data Mining
# Lesson: Recommender Systems

# Citation: 
# PEREIRA, V. (2018). Project: Recommender Systems, File: Python-DM-Recommender Systems-CF-Regression.py, GitHub repository: <https://github.com/Valdecy/Recommender-Systems-CF-Regression>

############################################################################

# Installing Required Libraries
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt

# Function: User-User / Item-Item Mean Centering
def centering(Xdata, mean_centering = "global"):
    mean = "none"
    if mean_centering == "columns":
        mean = Xdata.mean() # Missing values are discarded when calculating the mean
        Xdata = Xdata.fillna(0)
        for i in range(0, Xdata.shape[0]):
            for j in range(0, Xdata.shape[1]):
                Xdata.iloc[i, j] = Xdata.iloc[i, j] - mean[j]          
    elif mean_centering == "rows":
        mean = Xdata.T.mean()
        Xdata = Xdata.fillna(0)
        for i in range(0, Xdata.shape[0]):
            for j in range(0, Xdata.shape[1]):
                Xdata.iloc[i, j] = Xdata.iloc[i, j] - mean[i]  
    elif mean_centering == "global":
        mean = sum(Xdata.sum())/sum(Xdata.count())
        Xdata = Xdata.fillna(0)
        for i in range(0, Xdata.shape[0]):
            for j in range(0, Xdata.shape[1]):
                Xdata.iloc[i, j] = Xdata.iloc[i, j] - mean        
    return Xdata

def x_teta_matrix(Xdata, features = 1):
    x_weight    = np.random.rand(Xdata.shape[0], features + 1)/100
    teta_weight = np.random.rand(features + 1, Xdata.shape[1])/100
    return x_weight, teta_weight

def rmse_calculator(Xdata, predictions): 
    mse = Xdata.copy(deep = True) 
    for i in range (0, Xdata.shape[0]):
        for j in range (0, Xdata.shape[1]):
            if pd.isnull(mse.iloc[i][j]) == False:
                mse.iloc[i][j] = (Xdata.iloc[i][j] - predictions[i][j])**2
    mse  = sum(mse.sum())/sum(mse.count())
    rmse = (mse)**(1/2)  
    return rmse       

def x_teta_update(Xdata, mean_centering = "global", features = 2, iterations = 1000, alpha = 0.01):  
    Xdata = centering(Xdata, mean_centering = mean_centering)
    error       = Xdata.copy(deep = True)
    weight_list = x_teta_matrix(Xdata, features)
    x_weight    = weight_list[0]
    teta_weight = weight_list[1]
    loss_graph = np.ones(shape = (iterations + 1, 1))
    stop = 0  
    while (stop <= iterations):      
        pred = np.dot(x_weight, teta_weight)      
        for i in range (0, Xdata.shape[0]):
            for j in range (0, Xdata.shape[1]):
                if pd.isnull(error.iloc[i][j]) == False:
                    error.iloc[i][j] = (-Xdata.iloc[i][j] + pred[i][j])
                else:
                    error.iloc[i][j] = 0                         
        for j in range (0, features + 1):
            aux_x    = error.copy(deep = True)
            aux_teta = error.copy(deep = True)
            for m in range (0, error.shape[0]):
                for L in range (0, error.shape[1]):
                    aux_x.iloc[m][L]    = aux_x.iloc[m][L]*teta_weight[j,L]
                    aux_teta.iloc[m][L] = aux_teta.iloc[m][L]*x_weight[m,j]
            for i in range (0, error.shape[0]):
                x_weight[i][j]    = x_weight[i][j] - alpha*aux_x.iloc[i,:].sum() 
            for k in range (0, error.shape[1]):
                teta_weight[j][k] = teta_weight[j][k] - alpha*aux_teta.iloc[:,k].sum()              
        rmse = rmse_calculator(Xdata, pred)
        loss_graph[stop, 0] = rmse
        stop = stop + 1
        print("iteration = ", stop, " rmse = ", rmse)        
    for i in range (0, Xdata.shape[0]):
        for j in range (0, Xdata.shape[1]):
            Xdata.iloc[i][j] = pred[i][j]        
    plt.figure()
    plt.plot(loss_graph, label = 'loss')
    plt.legend(bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0.0)
    plt.show() 
    
    return Xdata, pd.DataFrame(x_weight), pd.DataFrame(teta_weight.T), rmse     
######################## Part 1 - Usage ####################################

df = pd.read_csv('Python-DM-Recommender Systems-03-CF-02-Regression.txt', sep = '\t')
X = df.iloc[:, 1:6]
X = X.set_index(df.iloc[:,0]) # First column as row names

# Calling the Function
prediction = x_teta_update(X, mean_centering = "global", features = 2, iterations = 1500, alpha = 0.01)

########################## End of Code #####################################
