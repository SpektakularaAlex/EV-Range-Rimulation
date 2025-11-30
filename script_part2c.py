import roadster
import matplotlib.pyplot as plt
import numpy as np


###PART 2C###
#Noggrannhetsordning och integrationsfel för trapetsmetoden: total konsumption för annas rutt

distance_km, speed_kmph = roadster.load_route('speed_anna.npz')
x = distance_km[-1]

#Skapa funktioner för integrationsfel och hjälplinje
def E(n):
    exakt = roadster.total_consumption(distance_km[-1], 'speed_anna.npz', 10000000)
    numeriskt = roadster.total_consumption(distance_km[-1], 'speed_anna.npz', n)
    E = numeriskt - exakt
    return E

def O(n):
    O = 1e7*1/(n**2)
    return O

n = 6
n_array = 2**np.linspace(0, n, n).astype(int) * 10000
E_array = np.array([E(i) for i in n_array])
O_array = np.array([O(i) for i in n_array])

#Plotta integrationsfelet och hjälplinje
plt.loglog(n_array, E_array, label = "E(n)")
plt.loglog(n_array, O_array, label = "O(1/n^2)")
plt.xlabel("Delintervall [n]")
plt.ylabel("Integrationsfel [Wh]")
plt.legend()
plt.show()