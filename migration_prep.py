# Written by: Nick Gerend, @dataoutsider
# Viz: "On the Move", enjoy!

import pandas as pd
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
import numpy as np
import os

def dfmatrix_to_df(dfmatrix, val_col_text):
    
    #region gather 1at column's name and data
    df_names = dfmatrix[[dfmatrix.columns[0]]]
    df_names.rename(columns={dfmatrix.columns[0]: 'var1_name'}, inplace=True)
    df_names = df_names.reset_index()
    df_names.rename(columns={'index': 'var1'}, inplace=True)
    #print(df_names)
    #endregion

    #region triangle select and merge
    bi_corrs = dfmatrix.where(np.tril(np.ones(dfmatrix.shape), k=1).astype(np.bool)).stack()
    df_bi_corrs = pd.DataFrame(data = bi_corrs)
    #print(df_bi_corrs)
    #print(df_bi_corrs.sort_index().loc[pd.IndexSlice[0,:][:]])
    df_bi_corrs['1'] = np.array(df_bi_corrs.index.to_frame(index = False)[0])
    df_bi_corrs['2'] = np.array(df_bi_corrs.index.to_frame(index = False)[1])
    df_bi_corrs.columns = [val_col_text, 'var1', 'var2']
    df_bi_corrs = df_bi_corrs.reset_index(drop=True)
    df_bi_corrs = df_bi_corrs[['var1', 'var2', val_col_text]]

    df_bi_corrs = pd.merge(df_bi_corrs, df_names, on=['var1'], how='left')
    with pd.option_context('display.max_rows', 5000):
        print(df_bi_corrs.loc[df_bi_corrs['var1_name'] == 'Alabama'])
    #endregion
    
    return df_bi_corrs

df_matrix = pd.read_csv(os.path.dirname(__file__) + '/Migration_States.csv', engine='python')
df_matrix_T = pd.read_csv(os.path.dirname(__file__) + '/Migration_States_T.csv', engine='python')
df_region = pd.read_csv(os.path.dirname(__file__) + '/Migration_Regions.csv', engine='python')

#region Upper
df_final = dfmatrix_to_df(df_matrix, 'val')
#print(df_final.loc[df_final['var1_name'] == 'Wyoming'])
df_final = pd.merge(df_final, df_region, how='left', left_on='var1_name', right_on='State')
df_final = pd.merge(df_final, df_region, how='left', left_on='var2', right_on='State')
df_final = df_final[['var1_name', 'Region_x', 'Diamond_x', 'var2', 'Region_y', 'Diamond_y', 'val']]
df_final.rename(columns={'var1_name': 'State_x', 'var2': 'State_y'}, inplace=True)
print(df_final.loc[df_final['State_x'] == 'Wyoming'])
df_states = df_final.loc[df_final['Region_x'].notnull() & df_final['Region_y'].notnull()]
df_extra = df_final.loc[df_final['Region_x'].isnull() | df_final['Region_y'].isnull()]
#endregion

#region Lower
df_final_2 = dfmatrix_to_df(df_matrix_T, 'val')
df_final_2 = pd.merge(df_final_2, df_region, how='left', left_on='var1_name', right_on='State')
df_final_2 = pd.merge(df_final_2, df_region, how='left', left_on='var2', right_on='State')
df_final_2 = df_final_2[['var1_name', 'Region_x', 'Diamond_x', 'var2', 'Region_y', 'Diamond_y', 'val']]
df_final_2.rename(columns={'var1_name': 'State_x', 'var2': 'State_y'}, inplace=True)
df_states_2 = df_final_2.loc[df_final_2['Region_x'].notnull() & df_final_2['Region_y'].notnull()]
df_extra_2 = df_final_2.loc[df_final_2['Region_x'].isnull() | df_final_2['Region_y'].isnull()]
#endregion

df_states.to_csv(os.path.dirname(__file__) + '/State_Pairs_Out.csv', encoding='utf-8', index=False)
df_extra.to_csv(os.path.dirname(__file__) + '/Extra_Pairs_Out.csv', encoding='utf-8', index=False)
df_states_2.to_csv(os.path.dirname(__file__) + '/State_Pairs_In.csv', encoding='utf-8', index=False)
df_extra_2.to_csv(os.path.dirname(__file__) + '/Extra_Pairs_In.csv', encoding='utf-8', index=False)