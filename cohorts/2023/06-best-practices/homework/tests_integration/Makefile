build:
	docker-compose up --force-recreate --build

bucket:
	aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration
	aws --endpoint-url=http://localhost:4566 s3 ls