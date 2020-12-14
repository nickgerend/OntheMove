# Written by: Nick Gerend, @dataoutsider
# Viz: "On the Move", enjoy!

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from math import cos, sin, pi

class point:
    def __init__(self, side, region, x, y, path = -1, value = -1, state = ''): 
        self.side = side
        self.region = region
        self.x = x
        self.y = y
        self.path = path
        self.value = value
        self.state = state
    def to_dict(self):
        return {
            'side' : self.side,
            'region' : self.region,
            'x' : self.x,
            'y' : self.y,
            'path' : self.path,
            'value' : self.value,
            'state' : self.state }

#region Load Data
df_states_data = pd.read_csv(os.path.dirname(__file__) + '/state_data.csv', engine='python')
df_state_id = pd.read_csv(os.path.dirname(__file__) + '/Migration_States.csv', engine='python')
df_state_id.reset_index(inplace=True)
df_state_id = df_state_id[['index', 'State']]
df_region = pd.read_csv(os.path.dirname(__file__) + '/Migration_Regions.csv', engine='python')

df_final = pd.merge(df_states_data, df_state_id, how='left', left_on='state_id', right_on='index')
df_final = pd.merge(df_final, df_state_id, how='left', left_on='state_id_source', right_on='index')
df_final = pd.merge(df_final, df_region, how='left', left_on='State_x', right_on='State')
df_final = pd.merge(df_final, df_region, how='left', left_on='State_y', right_on='State')

#df_final.to_csv(os.path.dirname(__file__) + '/Region_Connection.csv', encoding='utf-8', index=False)

df_states_in = df_final.loc[df_final['direction'] == 'in']
df_states_in = df_states_in.loc[df_final['Region_x'].notnull() & df_final['Region_y'].notnull()]
df_states_in = df_states_in[['State_x',	'Region_x',	'Diamond_x', 'State_y',	'Region_y',	'Diamond_y', 'value']]
df_states_in = df_states_in.loc[:,~df_states_in.columns.duplicated()]

df_states_out = df_final.loc[df_final['direction'] == 'out']
df_states_out = df_states_out.loc[df_final['Region_x'].notnull() & df_final['Region_y'].notnull()]
df_states_out = df_states_out[['State_x',	'Region_x',	'Diamond_x', 'State_y',	'Region_y',	'Diamond_y', 'value']]
df_states_out = df_states_out.loc[:,~df_states_out.columns.duplicated()]

df_states_in_group = df_states_in.groupby(['State_x'])['value'].sum().reset_index()
df_states_out_group = df_states_out.groupby(['State_x'])['value'].sum().reset_index()

df_final = pd.merge(df_states_in_group, df_states_out_group, how='left', on='State_x')
df_final = pd.merge(df_final, df_region, how='left', left_on='State_x', right_on='State')
df_final.rename(columns={'value_x': 'In', 'value_y': 'Out'}, inplace=True)
df_final = df_final[['State', 'Region', 'Diamond', 'In', 'Out']]

#endregion

#region Initialize Diamond
spacing = 10e4/2
col_val = 'Net'
#totals
df_final['Total'] = df_final['In'] + df_final['Out']
df_final['Net'] = df_final['In'] - df_final['Out']
#df_final.to_csv(os.path.dirname(__file__) + '/Region_In_Out.csv', encoding='utf-8', index=False)
#group by side and collect sums and counts, get longest side and add spacing (side_length)
#sum
Region_Diamond_Sum = df_final.groupby('Diamond')[col_val].apply(lambda o: o.abs().sum()).reset_index()
region_max = Region_Diamond_Sum[col_val].max()
side_max = Region_Diamond_Sum.loc[Region_Diamond_Sum[col_val] == region_max]['Diamond'][1]
#count and length
Region_Diamond_Count = df_final.groupby('Diamond')[col_val].count().reset_index()
region_count = Region_Diamond_Count.loc[Region_Diamond_Count['Diamond'] == side_max][col_val][1]
side_length = Region_Diamond_Sum[col_val].max() + (region_count + 1)*spacing
#endregion

#region Test Boundries

#Region_Diamond_Sum = df_final.groupby('Diamond')['Total'].sum().reset_index()
#side = Region_Diamond_Sum['Total'].max()

# square_x = [0, side, side, 0]
# square_y = [0, 0, side, side]

# angle = 45
# diam_x = [square_x[i]*cos(angle*pi/180) + square_y[i]*sin(angle*pi/180) for i in range(0, len(square_x))]
# diam_y = [-square_x[i]*sin(angle*pi/180) + square_y[i]*cos(angle*pi/180) for i in range(0, len(square_x))]

# plt.scatter(diam_x, diam_y)
# plt.gca().set_aspect('equal', adjustable='box')
# plt.show()

#endregion

#region Draw States
Region_Diamond_Group = df_final.groupby('Diamond')
outer_list = []
x = spacing
y = 0
val = 0
for side, group in Region_Diamond_Group:   
    group_sort = group.sort_values(by=[col_val], ascending=False)
    if side == 'LL':
        x = spacing
        y = 0
    if side == 'LR':
        x = side_length
        y = spacing
    if side == 'UR':
        x = side_length - spacing
        y = side_length
    if side == 'UL':
        x = 0
        y = side_length - spacing
    x = abs(x)
    for i, row in group_sort.iterrows():
        val = abs(row[col_val])
        outer_list.append(point(side, row['Region'], x, y, 1, row[col_val], row['State']))
        if side == 'LL':
            x += val
            y = 0
        if side == 'LR':
            x = side_length
            y += val
        if side == 'UR':
            x -= val
            y = side_length
        if side == 'UL':
            x = 0
            y -= val
        outer_list.append(point(side, row['Region'], x, y, 2, row[col_val], row['State']))
        if side == 'LL':
            x += spacing
        if side == 'LR':
            y += spacing
        if side == 'UR':
            x -= spacing
        if side == 'UL':
            y -= spacing

# x = [o.x for o in outer_list]
# y = [o.y for o in outer_list]
# plt.scatter(x, y)
# plt.gca().set_aspect('equal', adjustable='box')
# plt.show()

#endregion

# df_states = pd.DataFrame.from_records([s.to_dict() for s in outer_list])
print(7864530/side_length)
# print(df_states)

angle = 45
for item in outer_list:
    x = (item.x * 5.39541530372549) * 1.1 - 393226.5 - 200000
    y = (item.y * 5.39541530372549) * 1.1 - 393226.5 - 200000
    item.x = x*cos(angle*pi/180) + y*sin(angle*pi/180)
    item.y = -x*sin(angle*pi/180) + y*cos(angle*pi/180)

import csv
import os
with open(os.path.dirname(__file__) + '/test_square2.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['side', 'region', 'x', 'y', 'path', 'value', 'state'])
    for item in outer_list:
        writer.writerow([item.side, item.region, item.x, item.y, item.path, item.value, item.state])