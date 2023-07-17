#!/usr/bin/env python
# coding: utf-8

import os
import sys
import pickle
import pandas as pd


options = {
    'client_kwargs': {
        'endpoint_url': os.getenv('AWS_ENDPOINT_URL')
    }
}


def read_data(filename, categorical):
    df = pd.read_parquet(filename, storage_options=options)
    return prepare_data(df, categorical=categorical)


def save_data(df: pd.DataFrame, output_path: str) -> None:
    df.to_parquet(
        output_path,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options,
    )


def prepare_data(df, categorical):
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = 's3://nyc-duration-prediction-alexey/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)


def main(year, month):
    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)

    print(input_file)
    print(output_file)

    categorical = ['PULocationID', 'DOLocationID']
    df = read_data(input_file, categorical=categorical)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print('predicted mean duration:', y_pred.mean())

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    print('duration_sum:', df_result.predicted_duration.sum())

    save_data(df_result, output_file)


if __name__ == '__main__':
    main(year=int(sys.argv[1]), month=int(sys.argv[2]))