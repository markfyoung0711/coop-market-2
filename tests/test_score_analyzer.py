import json
import random
from io import StringIO

import pandas as pd

from src.score_analyzer import score_analyzer

RISK_1_GROUP_DATA = [[1.0, 1.0, 'Very High'],
                     [0.01, 0.24, 'Very Low'],
                     [0.12, 0.24, 'Medium'],
                     [0.30, 0.24, 'High'],
                     [0.40, 0.24, 'High'],
                     [0.90, 0.24, 'Very High']
                     ]

# raw data with expected results
RAW_TEST_DATA = '''score_1,score_2,expected_highlighted,expected_risk_1_group
0.71,0.4,False,High
0.52,0.85,False,High
0.18,0.7,True,Medium
0.11,0.55,True,Medium
0.74,0.08,False,High
0.9,0.34,False,Very High
0.96,0.17,False,Very High
0.59,0.14,False,High
0.56,0.03,False,High
0.05,0.62,True,Very Low
0.19,0.08,True,Medium
0.34,0.75,False,High
0.94,0.61,False,Very High
0.4,0.1,False,High
0.04,0.7,True,Very Low
0.37,0.19,False,High
0.82,0.17,False,Very High
0.69,0.36,False,High
0.18,0.61,True,Medium
0.27,0.23,True,Medium
0.22,0.76,False,Medium
0.73,0.7,False,High
0.22,0.77,False,Medium
0.74,0.14,False,High
0.84,0.6,False,Very High
0.20,0.6,False,Medium
0.15,0.6,True,Medium
0.35,0.35,False,High
0.35,0.34,False,High
0.34,0.35,False,High
0.34,0.90,False,High
0.34,0.80,False,High
0.10,0.80,True,Medium
0.30,0.80,False,High
0.80,0.80,False,Very High'''


def generate_test_data(num_rows=100):
    '''
    Purpose:
    --------
    Generate random score1 and score2 data probabilities
    To be run to generate a bunch of random data, then
    fill in boundary conditions manually into RAW_TEST_DATA
    for complete testing

    Returns:
    --------
    df - dataframe with columns 'score1', 'score2'
    '''
    data = []
    for _ in range(num_rows):
        score1 = round(random.uniform(0, 1), 2)
        score2 = round(random.uniform(0, 1), 2)
        data.append([score1, score2])

    return pd.DataFrame(data, columns=['score_1', 'score_2'])


def generate_raw_data():
    '''
    Create tempfile (csv) for opening with read_csv, and then use as fixture

    Returns:
    --------
    df: dataframe, with score_1 and score_2 inputs, and associated expected
        result fields/values

    '''
    with StringIO(RAW_TEST_DATA) as temp:
        df = pd.read_csv(temp, dtype=str)
        df['score_1'] = df['score_1'].astype(float)
        df['score_2'] = df['score_2'].astype(float)
        df.loc[df['expected_highlighted'] == 'True', 'expected_highlighted'] = True
        df.loc[df['expected_highlighted'] == 'False', 'expected_highlighted'] = False
        return df


def test_score_analyzer():

    # One Time: generate random data, then check for missing test conditions
    # see data file: test.results.csv
    # test_df = generate_test_data(25)
    # result = score_analyzer(test_df)

    test_df = generate_raw_data()
    config = json.loads(open('sample.json').read())
    results = score_analyzer(test_df, config)
    assert((results['expected_highlighted'] == results['highlighted']).all())
    assert((results['expected_risk_1_group'] == results['risk_1_group']).all())
