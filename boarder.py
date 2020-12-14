# Written by: Nick Gerend, @dataoutsider
# Viz: "On the Move", enjoy!

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from math import cos, sin, pi, sqrt, atan2

df_in_region = pd.read_csv(os.path.dirname(__file__) + '/In_Region.csv', engine='python')
df_in_region = df_in_region[['index', 'Region', 'Type']]
df_in_region['Type'] = df_in_region['Type'].str.lower()
df_poly = pd.read_csv(os.path.dirname(__file__) + '/poly_square.csv', engine='python')
df_poly['direction'] = ['out' if (o == 1) | (o == 2) else 'in' for o in df_poly['path']]
df_poly['poly'] = df_poly['index'].astype(str) + '_' + df_poly['direction']

class point:
    def __init__(self, index, side, region, x, y, path = -1, value = -1, direction = '', label = ''): 
        self.index = index
        self.side = side
        self.region = region
        self.x = x
        self.y = y
        self.path = path
        self.value = value
        self.direction = direction
        self.label = label
    def to_dict(self):
        return {
            'index' : self.index,
            'side' : self.side,
            'region' : self.region,
            'x' : self.x,
            'y' : self.y,
            'path' : self.path,
            'value' : self.value,
            'direction' : self.direction,
            'label' : self.label }

offset = 100000
width = 100000
df_poly['new_path'] = 0
df_poly_group = df_poly.groupby(['poly'])
newlist = []

def outer_xy(df_group):
    for name, group  in df_poly_group:
        
        group_s = group.sort_values(['path'], ascending=[True])

        x1 = group_s['x']._values[0]
        x2 = group_s['x']._values[1]
        y1 = group_s['y']._values[0]
        y2 = group_s['y']._values[1]

        side = group_s['side']._values[0]
        region = group_s['region']._values[0]
        value = group_s['value']._values[0]
        direction = group_s['direction']._values[0]
        index = group_s['index']._values[0]

        if side == 'LL':
            # x1 = #stuff
            # y1 = 0
            # x2 = #stuff
            # y2 = 0
            x3 = x1
            x4 = x2
            y3 = -offset - width
            y4 = -offset - width
            y1 = -offset
            y2 = -offset  
        if side == 'LR':
            # x1 = side_length
            # y1 = #stuff
            # x2 = side_length
            # y2 = #stuff
            y3 = y1
            y4 = y2
            x3 = x1 + offset + width
            x4 = x2 + offset + width
            x1 = x1 + offset
            x2 = x2 + offset   
        if side == 'UR':
            # x1 = side_length - #stuff
            # y1 = side_length
            # x2 = side_length - #stuff
            # y2 = side_length
            x3 = x1
            x4 = x2
            y3 = y1 + offset + width
            y4 = y2 + offset + width
            y1 = y1 + offset
            y2 = y2 + offset   
        if side == 'UL':
            # x1 = 0
            # y1 = side_length - #stuff
            # x2 = 0
            # y2 = side_length - #stuff
            y3 = y1
            y4 = y2
            x3 = x1 - offset - width
            x4 = x2 - offset - width
            x1 = x1 - offset
            x2 = x2 - offset
        
        newlist.append(point(name, side, region, x1, y1, 1, value, direction, index))
        newlist.append(point(name, side, region, x2, y2, 2, value, direction, index))
        newlist.append(point(name, side, region, x3, y3, 4, value, direction, index))
        newlist.append(point(name, side, region, x4, y4, 3, value, direction, index))

outer_xy(df_poly_group)

df_outer = pd.DataFrame.from_records([s.to_dict() for s in newlist])
df_outer = pd.merge(df_outer, df_in_region, how='left', left_on=['label', 'direction'], right_on=['index', 'Type'])
df_outer['region'] = df_outer['Region'].fillna(df_outer['region'])
df_outer.rename(columns={'index_x': 'index', 'Region_x': 'Region'}, inplace=True)
df_outer = df_outer[['index', 'side', 'region', 'x', 'y', 'path', 'value', 'direction', 'label']]

angle = 45
for i, row in df_outer.iterrows():
    x = row['x']
    y = row['y']
    df_outer.at[i,'x'] = x*cos(angle*pi/180) + y*sin(angle*pi/180)
    df_outer.at[i,'y'] = -x*sin(angle*pi/180) + y*cos(angle*pi/180)

df_curve = pd.read_csv(os.path.dirname(__file__) + '/poly_square_curve.csv', engine='python')
df_curve['label'] = df_curve['index']
print(df_outer)
print(df_curve)
df_all = pd.concat([df_curve, df_outer])

df_all.to_csv(os.path.dirname(__file__) + '/poly_square_boarder.csv', encoding='utf-8', index=False)

# import csv
# import os
# with open(os.path.dirname(__file__) + '/poly_square_boarder.csv', 'w',) as csvfile:
#     writer = csv.writer(csvfile, lineterminator = '\n')
#     writer.writerow(['index', 'side', 'region', 'x', 'y', 'path', 'value'])
#     for item in newlist:
#         writer.writerow([item.index, item.side, item.region, item.x, item.y, item.path, item.value])