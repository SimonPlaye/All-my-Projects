import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


df = pd.read_csv("DF.csv")
y = df["Price"]
X = df[["Area", "Rooms", "Bedrooms"]]

def sklearn_linear(X,y):
    reg = LinearRegression().fit(X, y)
    print(reg.coef_)
    print(reg.score(X,y))

#Normalization of X
X = (X - X.mean())/ X.std()
#Add of an extra column with 1
X = np.c_[np.ones(X.shape[0]),X]
sklearn_linear(X,y)
#Parameters
alpha=0.1
iterations = 2000
m = y.size
np.random.seed(123)
theta = np.random.rand(X.shape[1])


def gradient_descent(X, y, theta, iterations, alpha):
    past_costs = []
    past_thetas = [theta]
    for i in range(iterations):
        prediction = np.dot(X, theta)
        error = prediction - y
        cost = 1 / (2 * m) * np.dot(error.T, error)
        past_costs.append(cost)
        theta = theta - (alpha * (1 / m) * np.dot(X.T, error))
        past_thetas.append(theta)

    return past_thetas, past_costs


# Pass the relevant variables to the function and get the new values back...
past_thetas, past_costs = gradient_descent(X, y, theta, iterations, alpha)
theta = past_thetas[-1]


for i in range(len(theta)):
    print(f'The {i}e value of theta is : {theta[i]}')


