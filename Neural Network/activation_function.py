import matplotlib.pyplot as plt
import numpy as np

bias = 1.0 * + 1.5

def relu(x):
    a = []
    for item in x:
        a.append(item * (item > 0))
    return a

def sigmoid(x):
    a = []
    for item in x:
        a.append(1 + (np.exp(-item)))
    return a

x = np.arange(-10., 10., 0.2)
sig = sigmoid(x)

plt.plot(x,sig)
plt.show()