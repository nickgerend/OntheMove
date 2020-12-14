# Written by: Nick Gerend, @dataoutsider
# Viz: "On the Move", enjoy!

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from math import cos, sin, pi, sqrt, atan2

df_poly = pd.read_csv(os.path.dirname(__file__) + '/poly_square.csv', engine='python')
df_poly['segment'] = df_poly.apply(lambda x: 'a' if (x['path'] == 1) | (x['path'] == 4) else 'b', axis=1)

class point:
    def __init__(self, index, side, region, x, y, path = -1, value = -1, segment = ''): 
        self.index = index
        self.side = side
        self.region = region
        self.x = x
        self.y = y
        self.path = path
        self.value = value
        self.segment = segment

def LnToPntDst(x0, y0, x1, y1, x2, y2):
    n = abs((y1-y2)*x0+(x2-x1)*y0+x1*y2-x2*y1)
    d = sqrt((x2-x1)**2+(y2-y1)**2)
    return n/d

def DistBtwTwoPnts(x1, y1, x2, y2):
    return sqrt((x2-x1)**2+(y2-y1)**2)

def Ellipse_y(x, width, height):
    a = width/2
    b = height/2
    return (b/a)*sqrt(a**2-x**2)

def Rotate(x, y, angledeg, x_offset, y_offset):
    xa = x*cos(angledeg*pi/180) + y*sin(angledeg*pi/180)
    ya = -x*sin(angledeg*pi/180) + y*cos(angledeg*pi/180)
    xa -= x_offset
    ya -= y_offset
    return xa, ya

def AngleByTwoPnts(x1, y1, x2, y2):
    return atan2(x2-x1, y2-y1)*180/pi - 90

# xc = df_poly['x'].max()/2 
# yc = df_poly['y'].max()/2

xc = 7464530.0 / 2
yc = xc

df_poly_group_i = df_poly.groupby(['index'])
numpoints = 1001
final_list = []
ite = 1
for name_i, group_i in df_poly_group_i:
    index = name_i
    side = group_i['side']._values[0]
    region = group_i['region']._values[0]
    value = group_i['value']._values[0]

    switch = 0
    order = False
    if index in [15,10,5,0,14,9,4,3]:
        order = True
    for name_s, group_s in group_i.sort_values(['segment', 'path'], ascending=[True, order]).groupby(['segment']):

        x1 = group_s['x']._values[0]
        x2 = group_s['x']._values[1]
        y1 = group_s['y']._values[0]
        y2 = group_s['y']._values[1]

        cd = LnToPntDst(xc, yc, x1, y1, x2, y2)
        d = DistBtwTwoPnts(x1, y1, x2, y2)
        a = AngleByTwoPnts(x1, y1, x2, y2)
        zerohalf = d/2
        factor = (d/(xc*3))**0.2
        xe = np.linspace(-zerohalf, zerohalf, num=numpoints).tolist()
        ye = [Ellipse_y(x, d, cd*factor*1.5) for x in xe]
        xye =  list(zip(xe,ye))

        xt, yt = Rotate(xye[0][0], xye[0][1], a, 0, 0)
        x_offset = xt - x1
        y_offset = yt - y1
        
        ellipse = [Rotate(point[0], point[1], a, x_offset, y_offset) for point in xye]
        
        if switch == 0:
            for e in ellipse:
                final_list.append(point(index, side, region, e[0], e[1], ite, value))
                ite += 1
        else:
            for e in reversed(ellipse):
                final_list.append(point(index, side, region, e[0], e[1], ite, value))
                ite += 1
        switch = 1
    ite = 1

angle = 45
for item in final_list:
    x = item.x
    y = item.y
    item.x = x*cos(angle*pi/180) + y*sin(angle*pi/180)
    item.y = -x*sin(angle*pi/180) + y*cos(angle*pi/180)

import csv
import os
with open(os.path.dirname(__file__) + '/poly_square_curve.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['index', 'side', 'region', 'x', 'y', 'path', 'value', 'segment'])
    for item in final_list:
        writer.writerow([item.index, item.side, item.region, item.x, item.y, item.path, item.value, item.segment])