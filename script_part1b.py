import roadster
import matplotlib.pyplot as plt
import numpy as np



x_1, s_1 = roadster.load_route('speed_anna.npz')
x_2, s_2 = roadster.load_route('speed_elsa.npz')


plt.scatter(x_1, s_1, color = "red", label = "Anna", s = 0.1, zorder = 2)
plt.scatter(x_2, s_2, color = "blue", label = "Elsa", s = 0.1, zorder = 2)
plt.plot(x_1, roadster.velocity(x_1, 'speed_anna.npz'), label = "kontinuerlig hastighet Anna", linewidth = 0.2, color = "red", zorder = 1)
plt.plot(x_2, roadster.velocity(x_2, 'speed_elsa.npz'), label = "kontinuerlig hastighet Elsa", linewidth = 0.2, color = "blue", zorder = 1)
plt.legend()
plt.xlabel("Sträcka x [km]")
plt.ylabel("Fart v(x) [km/h]")
plt.title("Fart som funktion av tillryggalagd sträcka")
plt.show()