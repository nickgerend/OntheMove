# Written by: Nick Gerend, @dataoutsider
# Viz: "On the Move", enjoy!

import pandas as pd
import numpy as np
import os

df_states = pd.read_csv(os.path.dirname(__file__) + '/test_square2.csv', engine='python')
df_boarder = pd.read_csv(os.path.dirname(__file__) + '/poly_square_boarder.csv', engine='python')
df_all = pd.concat([df_boarder, df_states])
print(df_all)
print(df_all['index'].unique())
df_all.to_csv(os.path.dirname(__file__) + '/chord2.csv', encoding='utf-8', index=False)
print('finished')