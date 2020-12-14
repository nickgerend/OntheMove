# Written by: Nick Gerend, @dataoutsider
# Viz: "On the Move", enjoy!

import pandas as pd
import numpy as np
import os
import numbers

class flow:
    def __init__(self, state_id = -1, state_id_source = -1, value = -1, direction = ''): 
        self.state_id = state_id
        self.state_id_source = state_id_source
        self.value = value
        self.direction = direction

df_matrix = pd.read_csv(os.path.dirname(__file__) + '/Migration_States.csv', engine='python').fillna(0)
df_matrix_data = df_matrix.drop('State', axis=1)
df_matrix_data = df_matrix_data.apply(lambda o: o.str.replace(',', '').astype(float))

data_list = []
value = 0
for i, row in df_matrix_data.iterrows():
    for col in enumerate(row):
        value = col[1]
        icol = col[0]
        if isinstance(value, numbers.Number):
            if value > 0:
                data_list.append(flow(i, icol, value, 'in')) # in
                data_list.append(flow(icol, i, value, 'out')) # out

import csv
import os
with open(os.path.dirname(__file__) + '/state_data.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['state_id', 'state_id_source', 'value', 'direction'])
    for item in data_list:
        writer.writerow([item.state_id, item.state_id_source, item.value, item.direction])