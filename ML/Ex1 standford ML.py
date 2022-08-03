import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('ex1data1.csv')
X=df.iloc[:,0]
y = df.iloc[:,1]

"""plt.xlabel('Profit in $10,000s')
plt.ylabel('Population of City in 10,000s')
plt.plot(X,y, 'rx')
plt.show()"""

"""Linear regression for 1 feature"""

m = X.shape[0]
X = np.c_[np.ones(X.shape[0]),X]
theta = np.zeros(2)
iterations = 1500
alpha = 0.01

def cost_function(X, y, m, theta):
    prediction = np.dot(X, theta)
    error = prediction - y
    return np.dot(error.T, error)/(2*m)

"""print(cost_function(X, y, m, theta))
print(cost_function(X, y, m, [-1,2]))"""

def gradient_descent(X, y, theta, alpha, m, iterations):
    for i in range(iterations):
        prediction = np.dot(X,theta)
        error = prediction - y
        theta = theta - (alpha/m) * np.dot(X.T, error)
    return theta

"""theta = gradient_descent(X,y, theta, alpha, m, iterations)
print(f'Theta computed from gradient descent : {theta[0]}, {theta[1]}')"""


"""plt.xlabel('Profit in $10,000s')
plt.ylabel('Population of City in 10,000s')
plt.plot(X[:,1],y, 'rx')
plt.plot(X[:,1], np.dot(X,theta), 'b')
plt.show()"""

"""predict1 = np.dot([1, 3.5], theta)
print(f'For population = 35 000, we predict a profit of : {predict1*10000}')"""

"""Linear regression with multiple features"""

df = pd.read_csv("ex1data2.csv")
print(df.head())
X=df.iloc[:,[0,1]]
y = df.iloc[:,2]
y = y.to_numpy() #to prevent error of dimension
m = X.shape[0]


def featureNormalize(X):
    X = (X-X.mean())/X.std()
    return (X)

X=featureNormalize(X)

alpha=0.1
iterations = 400
X = np.c_[np.ones(X.shape[0]),X]
theta = np.zeros(3)

def gradient_descent_multi(X, y, theta, alpha, m, iterations):
    cost = []
    for i in range(iterations):
        cost.append(cost_function(X, y, m, theta))
        prediction = np.dot(X,theta)
        error = prediction - y
        theta = theta - (alpha/m) * np.dot(X.T, error)
    cost.append(cost_function(X, y, m, theta))
    return theta, cost

"""theta, cost = gradient_descent_multi(X, y, theta, alpha, m, iterations)

plt.xlabel('Number of iterations')
plt.ylabel('Cost J')
plt.plot(np.arange(iterations+1),cost, 'b')
plt.show()"""


"""Normal equation"""
X=df.iloc[:,[0,1]]
y = df.iloc[:,2]
X = np.c_[np.ones(X.shape[0]),X]

def normalEqn(X,y):
    square = np.dot(X.T, X)
    other = np.dot(X.T, y)
    inv = np.linalg.inv(square)
    total = np.dot(inv, other)
    return total

theta = normalEqn(X,y)
print(theta)