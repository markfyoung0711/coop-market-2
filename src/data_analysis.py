import pandas as pd


class ZeroForAll(Exception):
    '''this is a class of errors where we have no idea what a good Ads_Run might be.  Need manual override logic.'''
    pass


df = pd.read_csv('data/task3_dateset.csv', dtype=str)


def fix(name, df):
    '''
    fix the dataframe
    '''

    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
    df['Ads_Run'] = df['Ads_Run'].fillna(0)
    df['Ads_Run'] = df['Ads_Run'].astype(int)
    df = df.sort_values(by=['Site', 'Date'])

    # renumber indexes starting at zero
    df = df.reset_index(drop=True)

    # make an "index" column
    df = df.reset_index()

    if not (df['Ads_Run'] == 0).any():
        # still need to check if any are out of sequence.
        if sorted(df['Ads_Run'].tolist()) == df['Ads_Run'].tolist():
            # the data does not have any issues
            return df
        else:
            # there is a sequence problem the code cannot handle yet.
            # do a shift to find which values are in sequence
            ads_run_anchor = df[df['Ads_Run'] == df.shift(1)['Ads_Run'] + 1].head(1)['Ads_Run'].values[0]
            sample_idx = (df['Ads_Run'] == ads_run_anchor)
            offset = df.loc[sample_idx, 'index'].values[0] - df.loc[sample_idx, 'Ads_Run'].values[0]
            df.loc[:, 'Corrected_Ads_Run'] = df.loc[:, 'index'] - offset
            return df

    if (df['Ads_Run'] == 0).all():
        raise ZeroForAll(f'for {name}, we cannot infer an index offset value. Need to manually override')

    sample = df[df['Ads_Run'] != 0].head(1)
    offset = sample.index.values[0] - sample['Ads_Run'].values[0]
    fix_idx = (df['index'] + offset) != df['Ads_Run']
    df.loc[fix_idx, 'Corrected_Ads_Run'] = df.loc[fix_idx, 'index'] - offset
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
