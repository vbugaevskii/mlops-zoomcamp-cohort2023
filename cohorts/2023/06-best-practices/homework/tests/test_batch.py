import pandas as pd

from datetime import datetime
from batch import prepare_data

pd.set_option('display.max_columns', 10)


def dt(hour, minute, second=0):
    return datetime(2022, 1, 1, hour, minute, second)


def prep_test_inp():
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2), dt(1, 10)),
        (1, 2, dt(2, 2), dt(2, 3)),
        (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),     
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    return df


def prep_test_out():
    df_true = pd.DataFrame(data=[
        ('-1', '-1', dt(1, 2), dt(1, 10), 8.0),
        ( '1', '-1', dt(1, 2), dt(1, 10), 8.0),
        ( '1',  '2', dt(2, 2), dt(2,  3), 1.0),
    ], columns=['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'duration'])
    return df_true


def test_prepare_data():
    df_test = prep_test_inp()
    df_true = prep_test_out()

    categorical = ['PULocationID', 'DOLocationID']

    df_pred = prepare_data(df_test, categorical=categorical)

    assert df_true.shape == df_pred.shape
    assert (df_true.columns.sort_values() == df_pred.columns.sort_values()).all()
    assert (df_true.dtypes.sort_index() == df_pred.dtypes.sort_index()).all()

    columns = df_true.columns.sort_values()

    print(df_true.loc[:, columns])
    print(df_pred.loc[:, columns])

    print(df_true.dtypes)
    print(df_pred.dtypes)

    assert (df_true.loc[:, columns] == df_pred.loc[:, columns]).values.all()
