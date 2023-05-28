## mlflow

### Useful tips

1. Create environment to run mlflow
```bash
conda create -n mlflow python=3.8 -y
conda activate mlflow
pip install -r requirements.txt
```

2. Prepare data
```bash
mkdir -p data

wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-01.parquet \
    -O data/green_tripdata_2022-01.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-02.parquet \
    -O data/green_tripdata_2022-02.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-03.parquet \
    -O data/green_tripdata_2022-03.parquet
    
python homework/preprocess_data.py --raw_data_path data --dest_path output

ll -lsh output
```

3. Run MLflow:
```bash
mlflow server --backend-store-uri sqlite:///backend.db
```

4. Configure scripts using `.env` and run them:
```bash
python homework/train.py
python homework/hpo.py
python homework/register_model.py 
```

5. If you occasionaly deleted an experiment, you can restore it using `MLflowClient`:
```python
from mlflow.tracking import MlflowClient

client = MlflowClient()
# client.delete_experiment(1)
client.restore_experiment(1)
```

### Remote Configuration

Unfortunatelly AWS or Google Cloud are not available in my country, so I will use Yandex.Cloud.

1. Create Virtual Machine for MLflow.
2. Create Managed Service for PostgreSQL:
   - `mlflow_db` – name of database;
   - `mlflow` – name of user;
   - `mlflowpass` – password.
3. Create Bucket in Object Storage (it's not allowed to create a bucket named `mlflow-artifacts`).
4. Create Service Account for S3 bucket with permissions: `storage.viewer`, `storage.uploader`.
5. Configure [S3 connection](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#using-environment-variables) for MLflow according to `.env.example`. [See](
https://cloud.yandex.ru/docs/storage/tools/boto) boto3 configuration instruction fot Yandex.Cloud.
6. Run MLflow on VM:
```bash
# change db_endpoint according to your configuration

mlflow server -h 0.0.0.0 -p 5000 \
    --backend-store-uri postgresql://mlflow:mlflowpass@rc1b-z6wiknqrs6fy8nta.mdb.yandexcloud.net:6432/mlflow_db \
    --default-artifact-root s3://mlflow-artifacts-dev
```

Or you can use VK Cloud instructions:
- https://mcs.mail.ru/blog/mlflow-in-the-cloud#fromHistory
- https://mcs.mail.ru/docs/ru/ml/mlplatform/mlflow
- https://www.youtube.com/watch?v=1cI_bonO2Vo
