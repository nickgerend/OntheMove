# Written by: Nick Gerend, @dataoutsider
# Viz: "On the Move", enjoy!

import pandas as pd
import numpy as np
import os

df_io = pd.read_csv(os.path.dirname(__file__) + '/Region_In_Out.csv', engine='python')
df_c = pd.read_csv(os.path.dirname(__file__) + '/Region_Connection.csv', engine='python')
df_rc_group = df_c.groupby(['Region_x', 'Region_y', 'Diamond_x', 'Diamond_y', 'direction'])['value'].apply(lambda o: o.sum()).reset_index()
diamond_regions = df_rc_group.loc[df_rc_group['direction'] == 'out'].reset_index(drop = True)

diamond_regions['out_1'] = 0
diamond_regions['out_2'] = 0
diamond_regions['in_1'] = 0
diamond_regions['in_2'] = 0
diamond_regions['out_rank'] = 0
diamond_regions['in_rank'] = 0
df_r_group = diamond_regions.groupby('Region_x')

def rankdf(df, grp, col, val, sum_col_start, sum_col_end):
    df_group  = df.groupby(grp)
    rank = 1
    data = []
    rank_sum_start = 0
    rank_sum_end = 0
    for name, group in df_group:
        sorted_group = group.sort_values(val)
        for index, row in sorted_group.iterrows():
            row[col] = rank
            row[sum_col_start] = rank_sum_start
            rank_sum_end += row[val]
            row[sum_col_end] = rank_sum_end
            data.append(row)
            rank += 1
            rank_sum_start += row[val]
        rank = 1
        rank_sum_start = 0
        rank_sum_end = 0
    return data

data_x = rankdf(diamond_regions, 'Region_x', 'out_rank', 'value', 'out_1', 'out_2')
df_new = pd.DataFrame(data=data_x, columns=diamond_regions.columns)
data_y = rankdf(df_new, 'Region_y', 'in_rank', 'value', 'in_1', 'in_2')
df_new = pd.DataFrame(data=data_y, columns=diamond_regions.columns)
df_new.reset_index(inplace = True)
df_new = df_new.sort_values(['Region_x', 'out_rank'], ascending=[True, True])
print(df_new)

Out_Sum = df_new.groupby('Diamond_x')['value'].sum().reset_index()
Out_Sum.rename(columns={'Diamond_x': 'Diamond'}, inplace=True)
Out_Sum['Type'] = 'Out'
In_Sum = df_new.groupby('Diamond_y')['value'].sum().reset_index()
In_Sum.rename(columns={'Diamond_y': 'Diamond'}, inplace=True)
In_Sum['Type'] = 'In'
All_Sum = pd.concat([Out_Sum, In_Sum])
print(All_Sum)

#region Outer Polygons
Out_Sum_Region = df_new.groupby(['Diamond_x', 'Region_x'])['value'].sum().reset_index()
Out_Sum_Region.rename(columns={'Diamond_x': 'Diamond', 'Region_x': 'Region'}, inplace=True)
Out_Sum_Region['Type'] = 'Out'
In_Sum_Region = df_new.groupby(['Diamond_y', 'Region_y', 'Region_x', 'index'])['value'].sum().reset_index()
In_Sum_Region.rename(columns={'Diamond_y': 'Diamond', 'Region_x': 'Region'}, inplace=True)
In_Sum_Region['Type'] = 'In'
In_Sum_Region = In_Sum_Region[['index', 'Diamond', 'Region', 'value', 'Type']]
All_Sum_Region = pd.concat([Out_Sum_Region, In_Sum_Region])
print(In_Sum_Region)
In_Sum_Region.to_csv(os.path.dirname(__file__) + '/In_Region.csv', encoding='utf-8', index=False)
#endregion

All_Sum_Group = All_Sum.groupby('Diamond')['value'].sum().reset_index()
spacing = 1e6/2
side_length = All_Sum_Group['value'].max() + spacing * 3
print(side_length)

class point:
    def __init__(self, index, side, region, x, y, path = -1, value = -1): 
        self.index = index
        self.side = side
        self.region = region
        self.x = x
        self.y = y
        self.path = path
        self.value = value

position_list = []
out_dict = Out_Sum.set_index('Diamond').T.to_dict('list')

def calc_xy_square(newlist, df, r_col, dia_col, val, dir_, spacing, opp_d = None):
    path1 = 1
    path2 = 2
    mult = 1
    if dir_ == 'in':
        path1 = 3
        path2 = 4
        mult = 2
    spacing *= mult
    dir_ = dir_ + '_'
    for i, row in df.iterrows():
        index = row['index']
        side = row[dia_col]
        region = row[r_col]
        value = row[val]       
        prior_sum = 0
        if opp_d is not None:
            if dir_ == 'in_':
                prior_sum = opp_d[side][0]

        if side == 'LL':
            x1 = spacing + row[dir_  + '1'] + prior_sum
            y1 = 0
            x2 = spacing + row[dir_+ '2'] + prior_sum
            y2 = 0
        if side == 'LR':
            x1 = side_length
            y1 = spacing + row[dir_ + '1'] + prior_sum
            x2 = side_length
            y2 = spacing + row[dir_ + '2'] + prior_sum
        if side == 'UR':
            x1 = side_length - spacing - row[dir_ + '1'] - prior_sum
            y1 = side_length
            x2 = side_length - spacing - row[dir_ + '2'] - prior_sum
            y2 = side_length
        if side == 'UL':
            x1 = 0
            y1 = side_length - spacing - row[dir_ + '1'] - prior_sum
            x2 = 0
            y2 = side_length - spacing - row[dir_ + '2'] - prior_sum
        
        newlist.append(point(index, side, region, x1, y1, path1, value))
        newlist.append(point(index, side, region, x2, y2, path2, value))

calc_xy_square(position_list, df_new, 'Region_x', 'Diamond_x', 'value', 'out', spacing)
calc_xy_square(position_list, df_new, 'Region_y', 'Diamond_y', 'value', 'in', spacing, out_dict)

# import csv
# import os
# with open(os.path.dirname(__file__) + '/poly_square.csv', 'w',) as csvfile:
#     writer = csv.writer(csvfile, lineterminator = '\n')
#     writer.writerow(['index', 'side', 'region', 'x', 'y', 'path', 'value'])
#     for item in position_list:
#         writer.writerow([item.index, item.side, item.region, item.x, item.y, item.path, item.value])