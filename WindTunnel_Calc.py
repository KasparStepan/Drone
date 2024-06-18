import numpy as np
import matplotlib.pyplot as plt

## Air properties
density = 1.225 #kg/m3
viscosity = 1.825e-5 #kg/ms

cruise_speed_real = 15 #m/s

mean_chord_real = 0.1365676722802403 #m
wingspan_real = 1.5 # m
aspect_ratio_real = wingspan_real/mean_chord_real #-
wing_area_real = mean_chord_real*wingspan_real #m2

Re_real = density*cruise_speed_real*mean_chord_real/viscosity
print(Re_real)
print()

velocity_WT = np.linspace(40,55,100)

mean_chord_WT = Re_real*viscosity/(density*velocity_WT)
wingspan_WT = aspect_ratio_real*mean_chord_WT

plt.subplot(1,2,1)
plt.plot(velocity_WT,mean_chord_WT)
plt.title('Mean aerodynamic chord (Real is 0.1366 m) ')
plt.xlabel('Wind tunnel velocity [m/s]')
plt.ylabel('Mean aerodynamic chord wind tunnel [m]')
plt.grid(which='both')

plt.subplot(1,2,2)
plt.plot(velocity_WT,wingspan_WT)
plt.title('Wingspan (Real is 1.5 m) ')
plt.xlabel('Wind tunnel velocity [m/s]')
plt.ylabel('Wingspan wind tunnel [m]')
plt.grid(which='both')

plt.show()