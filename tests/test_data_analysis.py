from io import StringIO

import pandas as pd
import pytest

from src.data_analysis import fix, ZeroForAll


RAW_DATA = '''Site,Date,Ads_Run
A,9/24/20,0
A,9/23/20,0
A,9/22/20,0
A,9/21/20,0
A,9/20/20,10
B,9/19/20,5
B,9/18/20,4
B,9/17/20,1
B,9/16/20,2
B,9/15/20,1
C,9/19/20,0
C,9/18/20,0
C,9/17/20,0
D,9/19/20,12
D,9/18/20,11
D,9/17/20,10
'''


def test_fix():

    df_test = pd.read_csv(StringIO(RAW_DATA), dtype=str)
    df_A = df_test[df_test['Site'] == 'A']
    df_B = df_test[df_test['Site'] == 'B']
    df_C = df_test[df_test['Site'] == 'C']
    df_D = df_test[df_test['Site'] == 'D']

    df_fixedA = fix('A', df_A)
    assert(df_fixedA['Corrected_Ads_Run'].tolist() == [10, 11, 12, 13, 14])

    df_fixedB = fix('B', df_B)
    assert(df_fixedB['Corrected_Ads_Run'].tolist() == [1, 2, 3, 4, 5])

    with pytest.raises(ZeroForAll):
        _ = fix('C', df_C)

    df_fixedD = fix('D', df_D)
    assert('Corrected_Ads_Run' not in df_fixedD.columns)
