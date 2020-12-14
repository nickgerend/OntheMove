# Written by: Nick Gerend, @dataoutsider
# Viz: "On the Move", enjoy!

import numpy as np
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, pi
plt.rcParams["figure.figsize"] = 12.8, 9.6

def tube(x, y):
    return (x**2+y**2)

N = 10
n = 1000
x = np.linspace(-N,N,n)
y = x
Xgrid, Ygrid = np.meshgrid(x, y)

Zgrid = tube(Xgrid, Ygrid)
Xout = np.reshape(Xgrid, -1)
Yout = np.reshape(Ygrid, -1)
Zout = np.reshape(Zgrid, -1)

angle = 45
length = len(Xout)

import csv
import os
# with open(os.path.dirname(__file__) + '/background.csv', 'w',) as csvfile:
#     writer = csv.writer(csvfile, lineterminator = '\n')
#     writer.writerow(['x', 'y', 'z'])
#     for i in range(length):
#         writer.writerow([Xout[i]*cos(angle*pi/180) + Yout[i]*sin(angle*pi/180), -Xout[i]*sin(angle*pi/180) + Yout[i]*cos(angle*pi/180), Zout[i]])

with open(os.path.dirname(__file__) + '/background_square.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['x', 'y', 'z'])
    for i in range(length):
        writer.writerow([Xout[i], Yout[i], Zout[i]])

print('finished')