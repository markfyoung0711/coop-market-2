def score_analyzer(df):
    '''
    Purpose:
    --------
    Apply score analyzer rules per requirements in README.md for Task 1

    Parameters:
    -----------
    df: dataframe, with two columns with score data in them
        - 'score_1' must be a float between 0 and 1
        - 'score_2' must be a float between 0 and 1

    Returns:
    --------
    df: dataframe, with original columns
        and additional columns: 'highlighted', and 'risk_1_group'

    Column Descriptions:
    --------------------

    'highlighted' - bool
        True if:
            both columns (score_1 and score_2) are below 0.35 OR
            score_1 is below 0.20 and score_2 is below 0.90, OR
            score_1 is below 0.15 and score_2 is below 0.80
        else False

    'risk_1_group' - str, 'Very Low', 'Medium', 'High', 'Very High'

        'Very Low' - score_1 < 0.10
        'Medium' - 0.10 <= score_1 < 0.30
        'High' - 0.30 <= score_1 < 0.80
        'Very High' - score_1 >= 0.80

    '''
    # do some error checks on assumptions
    for col in df.columns:
        if df[col].isnull().any():
            raise Exception(f'There are null values for {col}')

    idx = (((df['score_1'] < 0.35) & (df['score_2'] < .35)) |
           ((df['score_1'] < 0.20) & (df['score_2'] < .90)) |
           ((df['score_1'] < 0.15) & (df['score_2'] < .80)))
    df.loc[idx, 'highlighted'] = True
    df.loc[~idx, 'highlighted'] = False

    errors_idx = df['highlighted'].isnull()
    if errors_idx.any():
        raise Exception(f'"highlighted" values null: {df[errors_idx]}')

    scoring_dict = {}
    scoring_dict['Very Low'] = (df['score_1'] < 0.10)
    scoring_dict['Medium'] = (0.10 <= df['score_1']) & (df['score_1'] < 0.30)
    scoring_dict['High'] = (0.30 <= df['score_1']) & (df['score_1'] < 0.80)
    scoring_dict['Very High'] = (df['score_1'] >= 0.80)

    for score_group, idx in scoring_dict.items():
        df.loc[idx, 'risk_1_group'] = score_group

    errors_idx = df['risk_1_group'].isnull()
    if errors_idx.any():
        raise Exception(f'"risk_group_1" values null: {df[errors_idx]}')

    # for risk group 1 scores, create columns for each of the categories so they can be plotted against one another
    risk_group_names = df['risk_1_group'].unique()
    for group_name in risk_group_names:
        idx = df['risk_1_group'] == group_name
        df.loc[idx, group_name] = df.loc[idx, 'score_1']

    return df
