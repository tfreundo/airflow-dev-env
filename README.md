# datapipe-sandbox
A sandbox for data projects where you can easily develop data pipelines in a close to production environment.

The current setup includes:
* Airflow
* MongoDB

See also the [docker-compose.yml](docker-compose.yml)

## How to set it up
Simply run `docker-compose up -d` and you're up and running.
If everything worked, your Airflow should be ready under `http://localhost:8080/`

### Adding sample datasets to MongoDB
If you quickly want to play around, you can insert sample datasets using the script [mongodb_datasets.sh](scripts/mongodb_datasets.sh).

If you want to add your own datasets (e.g. an export of a production database) you can use the script [mongodb_custom_datasets.sh](scripts/mongodb_custom_datasets.sh).

## Adding your own DAGs and Plugins
Your airflow instance is mounting the folders `airflow/dags` and `airflow/plugins` for you. So you can develop your scripts locally, and the Airflow docker container will pick them up and they are ready to use.

## Troubleshooting
For known issues and their solutions see [Troubleshooting.md](Troubleshooting.md)
