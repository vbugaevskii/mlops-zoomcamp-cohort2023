## Prefect

Unfortunatelly Google Cloud and AWS are not available in my country, so I will use Yandex.Cloud.

### Useful Tips

1. Create environment to run Prefect:
```bash
conda create -n prefect-py38 python=3.8 -y
conda activate prefect-py38
pip install -r requirements.txt
```

2. Prefect Commands
```bash
# start web viewer
prefect orion start
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

# start prefect agent for running deployments
prefect agent start --work-queue "default"

# create deploymnet with cron schedule
# https://crontab.guru/
prefect deployment build flows/orchestrate.py:main_flow -n main_flow --cron '0 9 3 * *'
prefect deployment apply main_flow-deployment.yaml

prefect deployment build flows/orchestrate.py:main_flow -n main_flow_feb \
    --param train_path="./data/green_tripdata_2023-02.parquet" \
    --param val_path="./data/green_tripdata_2023-03.parquet"
prefect deployment apply main_flow-deployment.yaml

# register
prefect block register -m prefect_email
```

3. I used different email service for sending emails, usually you have to create special codes for external applications:
- https://help.mail.ru/mail/mailer/popsmtp
- https://help.mail.ru/mail/security/protection/external
- https://yandex.ru/support/mail/mail-clients/others.html
- https://support.google.com/accounts/answer/185833
