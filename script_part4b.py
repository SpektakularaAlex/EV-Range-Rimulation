#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import route_nyc 

time_h_4_00 = route_nyc.nyc_route_traveler_euler(4, 0.01)[0]
distance_km_4_00 = route_nyc.nyc_route_traveler_euler(4, 0.01)[1]
time_h_9_30 = route_nyc.nyc_route_traveler_euler(9.5, 0.01)[0]
distance_km_9_30 = route_nyc.nyc_route_traveler_euler(9.5, 0.01)[1]

### Given contour plot ###
n_fine = 100
t_fine = np.linspace(0, 24, n_fine)
x_fine = np.linspace(0, 60, n_fine)
tt_fine, xx_fine = np.meshgrid(t_fine, x_fine)
zz_fine = route_nyc.route_nyc(tt_fine,xx_fine)
w, h = plt.figaspect(0.4)
fig = plt.figure(figsize=(w, h))
plt.axes().set_aspect(0.2, adjustable='box')
cs = plt.contourf(tt_fine,xx_fine,zz_fine, 50, cmap='jet')
### Tillägg start
plt.plot(time_h_4_00, distance_km_4_00, color = 'white', label = 'Ruttfärd med start kl. 04:00')
plt.plot(time_h_9_30, distance_km_9_30, color = 'black', label = 'Ruttfärd med start kl. 09:30')
plt.legend()
### Tillägg slut
plt.xlabel('Time [hour of day]',fontsize=18)
plt.ylabel('Distance [km]',fontsize=18)
plt.title('Speed [km/h]',fontsize=18)
fig.colorbar(cs)
plt.savefig("speed-data-nyc.eps", bbox_inches='tight')
plt.show()