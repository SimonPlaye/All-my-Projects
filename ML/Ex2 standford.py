import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as op


"""Logisitic regression"""
df = pd.read_csv("data/ex2data1.csv")
print(df)
X = df.iloc[:, [0,1]]
y = df.iloc[:,2]

"""plt.xlabel("Exam 1 score")
plt.ylabel("Exam 2 score")
pos = df[df["label"]==0].iloc[:,[0,1]]
neg = df[df["label"]==1].iloc[:,[0,1]]
plt.plot(pos.iloc[:,0], pos.iloc[:,1],"ko")
plt.plot(neg.iloc[:,0], neg.iloc[:,1], "k+")
plt.show()"""

def sigmoid(z):
    return(1/(1+np.exp(-z)))

m, n = X.shape
X = np.c_[np.ones(m), X]
initial_theta = np.zeros(n+1)

def costFunction(theta, X, y):
    m = y.shape[0]
    grad = np.zeros(theta.shape[0])

    prediction = sigmoid(np.dot(X,theta))
    log_1 = np.log(prediction)
    log_2 = np.log(1-prediction)
    error_1 = np.dot(-y.T,log_1)
    error_2 = np.dot((1-y).T, log_2)

    cost = (1/m) * (error_1 - error_2)
    grad = (1/m) * np.dot(X.T, prediction - y)

    return cost, grad

cost, grad = costFunction(initial_theta, X, y)

print(f'Cost at initial theta : {cost}, gradient at initial theta : {grad}')


"""Les deux fonctions suivantes ne servent qu'à mettre en oeuvre spicy.optimize"""
def costFunction_bis(theta, X, y):
    m, n = X.shape
    term1 = np.log(sigmoid(np.dot(X, theta)))
    term2 = np.log(1-sigmoid(np.dot(X,theta)))
    term1 = term1.reshape((m,1))
    term2 = term2.reshape((m,1))
    term = np.dot(-y.T, term1) - np.dot((1-y).T, term2)
    return(term/m)

def Gradient(theta, X, y):
    m, n = X.shape
    prediction = sigmoid(np.dot(X,theta))
    grad = (1/m) * np.dot(X.T, prediction - y)
    return grad.flatten()

theta = op.minimize(fun = costFunction_bis, x0 = initial_theta, args = (X,y), method = 'TNC', jac = Gradient)
theta = theta.x

prob = sigmoid(np.dot(np.array([1, 45, 85]),theta))
print(f'For a student with scores 45 and 85 we prediction an admission probability of : {prob}')

def predict(theta, X):
    prediction = sigmoid(np.dot(X, theta))
    p = np.zeros(X.shape[0])
    for it in range(0, X.shape[0]):
        if prediction[it] > 0.5:
            p[it] = 1
    return p
p = predict(theta, X)
prediction_true = np.array(np.where(p == y))
print(f'Train accuracy : {(prediction_true.shape[1]/y.shape[0])*100}%')