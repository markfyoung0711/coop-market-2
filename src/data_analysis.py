import pandas as pd


df = pd.read_csv('data/task3_dateset.csv', dtype=str)
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
df['Ads_Run'] = df['Ads_Run'].fillna(0)
df['Ads_Run'] = df['Ads_Run'].astype(int)
df = df.sort_values(by=['Site', 'Date'])


def fix(name, df):
    '''
    fix the dataframe
    '''

    # renumber indexes starting at zero
    df = df.reset_index(drop=True)

    # make an "index" column
    df = df.reset_index()

    if not (df['Ads_Run'] != 0).any():
        raise Exception(f'for {name}, we cannot infer a value')

    sample = df[df['Ads_Run'] != 0].head(1)
    offset = sample.index.values[0] - sample['Ads_Run'].values[0]
    df.loc[df['Ads_Run'] == 0, 'Corrected_Ads_Run'] = df.loc[df['Ads_Run'] == 0, 'index'] - offset
    df.loc[df['Corrected_Ads_Run'] == 0, 'Corrected_Ads_Run'] = 1
    df.loc[df['Corrected_Ads_Run'] < 0, 'Corrected_Ads_Run'] = 1
    df.loc[df['Corrected_Ads_Run'].isnull(), 'Corrected_Ads_Run'] = df.loc[df['Corrected_Ads_Run'].isnull(), 'Ads_Run']
    df['Corrected_Ads_Run'] = df['Corrected_Ads_Run'].astype(int)
    return df


results = []
dfg = df.groupby('Site')
for name, df_single in dfg:
    # For the optimization: use multiprocessing for the "fix" function. One process per Group
    fixed_result = fix(name, df_single)
    results.append(fixed_result)

final_result = pd.concat(results, ignore_index=True)
final_result = final_result.drop(columns=['index'])
outfile = 'corrected.csv'
final_result.to_csv(outfile, index=False)
print(f'corrected data written to {outfile}')
