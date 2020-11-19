# datapipe-sandbox
A sandbox where you can easily try out ETL pipeline use cases and use it as a ready-to-go development environment for data projects.

## How to set it up
Simply run `docker-compose up -d` and you're up and running.
If everything worked, your Airflow should be ready under `http://localhost:8080/`

### Adding sample datasets to MongoDB
If you quickly want to play around, you can insert sample datasets using the script [mongodb_datasets.sh](scripts/mongodb_datasets.sh).

### Getting the mongo_hook
You need the [mongo_hook from the mongo_plugin](https://github.com/airflow-plugins/mongo_plugin) to access your MongoDB.
For convencience, you can just execute [download_mongo_hook.sh](scripts/download_mongo_hook.sh) which downloads the `mongo_hook` and stores it in your local airflow hooks and therefore is available for usage in your operators and DAGs.

## Adding your own DAGs and Plugins
Your airflow instance is mounting the folders `airflow/dags` and `airflow/plugins` for you. So you can develop your scripts locally, and airflow will pick them up and automatically pull them.

## Troubleshooting
For known issues and their solutions see [Troubleshooting.md](Troubleshooting.md)
