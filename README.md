# airflow-dev-env
Your extensible development environment for data projects with [Apache Airflow](https://airflow.apache.org/).

* Close to a production environment
* Easily extensible
* Convenient development

See also the [docker-compose.yml](docker-compose.yml)

## How to set it up
Simply run `docker-compose up -d` and you're up and running.
If everything worked, your Airflow should be ready under `http://localhost:8080/`

## Adding your own DAGs and Plugins
Your airflow instance is mounting the folders `airflow/dags` and `airflow/plugins` for you. So you can develop your scripts locally, and the Airflow docker container will pick them up and they are ready to use.

## Troubleshooting
For known issues and their solutions see [Troubleshooting.md](Troubleshooting.md)
