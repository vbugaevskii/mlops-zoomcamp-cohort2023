#!/usr/bin/env python
# coding: utf-8

import argparse
import pickle
import pandas as pd


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


categorical = ['PULocationID', 'DOLocationID']


def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-y', '--year', type=int, default=2022)
    parser.add_argument('-m', '--month', type=int, default=1)
    parser.add_argument('-c', '--color', type=str, default='yellow')

    args = parser.parse_args()

    url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year:d}-{month:02d}.parquet'.format(
        color=args.color,
        year=args.year,
        month=args.month,
    )

    print("Load dataset")    
    df = read_data(url)
    df['ride_id'] = f'{args.year:04d}/{args.month:02d}_' + df.index.astype('str')
    print("df.shape =", df.shape)

    print("Prepare dataset")
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)

    print("Make predicition")
    df_result = pd.DataFrame({
        'ride_id': df['ride_id'],
        'predictions': model.predict(X_val),
    })

    print("Save results")
    df_result.to_parquet(
        'predictions.parquet',
        engine='pyarrow',
        compression=None,
        index=False
    )

    print(df_result['predictions'].mean())

