import matplotlib.pyplot as plt
import numpy as np


dN=1000
x=np.linspace(0,5,dN)
A=4


def f(A,x):
    return A*np.cos(2*np.pi*x)*np.exp(-x)
plt.ylim([-4.5,4.5])
plt.title("Oscillation amortie")
plt.xlabel("Temps (t)")
plt.ylabel("Amplitude")
plt.plot(x,f(A,x), color="red")
plt.text(3,-4,"$A \cos(2 \pi t ) e^{-t}$",color="red", fontsize=20,bbox={"facecolor":"red","alpha":0.1})
plt.plot(x,A*np.exp(-x),color="blue")
plt.plot(x,-A*np.exp(-x),color="blue")
plt.show()
