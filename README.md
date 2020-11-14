# simple_etl_playground
A simple ETL pipeline using a MongoDB as source database.

## How to set it up

### get_me_ready.sh
If you just want to get it running fast, use the shell scripts `get_me_ready.sh` (e.g. using Git Bash if you're on Windows).
You can also adapt the configuration there to your needs or extract the steps and execute them manually if you like.

The script will:
* (optional) Start a local MongoDB for you
* (optional) Insert the [Zip Code Dataset](https://docs.mongodb.com/manual/tutorial/aggregation-zip-code-data-set/) into that MongoDB
* Build and start Apache Airflow with the default configuration

If everything worked, your Airflow should be ready under `http://localhost:8080/`

## Configure Airflow
For Airflow the pretty popular repository [docker-airflow by puckel](https://github.com/puckel/docker-airflow) is used.
See more information there on e.g. additional configuration possibilities etc.
This repository is referenced as a [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) located under `/submodules/docker-airflow`.

## Adding your own DAGs
Per default, Airflow will scan the configured DAG-folder `/submodules/docker-airflow/dags` periodically. You can configure the filecheck interval in the `/submodules/docker-airflow/config/airflow.cfg` parameter `dag_dir_list_interval`.

Meaning, if you add your own DAG python files there, after some time they will magically appear in your running Airflow instance. You don't even have to rebuild or restart your Docker container.

I added for convenience the folder `/dags`. Put your own DAGs in there, code and if you want to push them to your airflow instance, call the shell script `push_dags.sh`.
This will copy the content of the `/dags` folder to `/submodules/docker-airflow/dags` and then your DAGs will appear in your airflow instance.

## Troubleshooting
For known issues and their solutions see [Troubleshooting.md](Troubleshooting.md)