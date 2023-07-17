import pandas as pd
from datetime import datetime
from pathlib import Path

def dt(hour, minute, second: int = 0) -> datetime:
    return datetime(2022, 1, 1, hour, minute, second)


options = {
    'client_kwargs': {
        'endpoint_url': 'http://localhost:4566'
    }
}


if __name__ == "__main__":
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2), dt(1, 10)),
        (1, 2, dt(2, 2), dt(2, 3)),
        (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = [
        'PULocationID', 'DOLocationID',
        'tpep_pickup_datetime', 'tpep_dropoff_datetime'
    ]

    df = pd.DataFrame(data, columns=columns)
    path_dir = Path('./output')
    path_dir.mkdir(exist_ok=True)
    df.to_parquet(
        # path_dir / 'integration_file.parquet',
        's3://nyc-duration/in/2022-01.parquet',
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options,
    )