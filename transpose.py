# Written by: Nick Gerend, @dataoutsider
# Viz: "On the Move", enjoy!

import pandas as pd
import numpy as np
import os

df_matrix = pd.read_csv(os.path.dirname(__file__) + '/Migration_States.csv', engine='python')

df_matrix = df_matrix.set_index('State', ).T
df_matrix = df_matrix.reset_index()
df_matrix.rename(columns={'index': 'State'}, inplace=True)
print(df_matrix)
df_matrix.to_csv(os.path.dirname(__file__) + '/Migration_States_T.csv', encoding='utf-8', index=False)