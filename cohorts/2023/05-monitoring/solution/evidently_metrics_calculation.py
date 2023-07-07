import logging 
import pandas as pd
import psycopg

from datetime import datetime, timedelta

from prefect import task, flow

from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnQuantileMetric, ColumnValueListMetric

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")


create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
	timestamp timestamp,
	fare_amount_q50 float
)
"""

raw_data = pd.read_parquet('data/green_tripdata_2023-03.parquet')
raw_data['dt'] = raw_data.lpep_pickup_datetime.dt.date
dt_from, dt_till = datetime(2023, 3, 1), datetime(2023, 4, 1)

num_features = ['passenger_count', 'trip_distance', 'fare_amount', 'total_amount']
cat_features = ['PULocationID', 'DOLocationID']

column_mapping = ColumnMapping(
    target=None,
    prediction=None,
    numerical_features=num_features,
    categorical_features=cat_features,
)

report = Report(metrics=[
    ColumnQuantileMetric("fare_amount", quantile=0.5),
    ColumnValueListMetric("PULocationID", values=list(range(1, 266))),
])


@task(retries=2, retry_delay_seconds=5, name="prepare postgress db")
def prep_db():
	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
		if len(res.fetchall()) == 0:
			conn.execute("create database test;")
		with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn:
			conn.execute(create_table_statement)


@task(retries=2, retry_delay_seconds=5, name="calculate metrics", log_prints=True)
def calculate_metrics_postgresql(curr, dt):
	current_data = raw_data[raw_data['dt'] == dt.date()]
	print(current_data.shape)

	report.run(
		reference_data=None,
		current_data=current_data,
		column_mapping=column_mapping,
	)

	result = report.as_dict()

	fare_amount_q50 = result['metrics'][0]['result']['current']['value']
	print(f"insert date={dt:%Y-%m-%d} fare_amount_q50={fare_amount_q50}")

	curr.execute(
		"insert into dummy_metrics(timestamp, fare_amount_q50) values (%s, %s)",
		(dt, fare_amount_q50),
	)


@flow(log_prints=True)
def batch_monitoring_backfill():
	prep_db()

	with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example", autocommit=True) as conn:
		print(f"processing period: [{dt_from:%Y-%m-%d}, {dt_till:%Y-%m-%d}]")

		dt_curr = dt_from
		while dt_curr < dt_till:
			print(f"processing date = {dt_curr:%Y-%m-%d}")
			with conn.cursor() as curr:
				calculate_metrics_postgresql(curr, dt_curr)
			dt_curr += timedelta(days=1)


if __name__ == '__main__':
	batch_monitoring_backfill()
