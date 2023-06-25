## Deployment

Command to convert `.ipynb` to `.py` script:
```bash
jupyter nbconvert --to script starter.ipynb
```

Create env with pipenv:
```bash
pip install pipenv
pipenv install scikit-learn==1.2.2 pandas pyarrow numpy scipy --python=3.10
pipenv shell
```

Run your code:
```bash
python starter.py -y 2022 -m 3 -c yellow
```

Run yout code in docker:
```bash
docker build -t mlops-zoomcamp-model:v1 .
docker run -it --rm mlops-zoomcamp-model:v1
```

