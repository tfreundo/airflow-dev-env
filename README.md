# etl_sandbox
A simple playground you can use to quickly try out ETL pipeline use cases and you can even use it as a development environment.

## How to set it up
Simply run `docker-compose up -d` and you're up and running.
If everything worked, your Airflow should be ready under `http://localhost:8080/`

### Adding sample datasets
If you quickly want to play around, you can insert sample datasets using the script `scripts/mongodb_datasets.sh`.

## Adding your own DAGs and Plugins
Your airflow instance is mounting the folders `airflow/dags` and `airflow/plugins` for you. So you can develop your scripts locally, and airflow will pick them up and automatically pull them.

## Troubleshooting
For known issues and their solutions see [Troubleshooting.md](Troubleshooting.md)