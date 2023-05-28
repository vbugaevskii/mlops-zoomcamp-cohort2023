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
