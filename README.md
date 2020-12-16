# airflow-dev-env
Your extensible development environment for data projects with [Apache Airflow](https://airflow.apache.org/).

* Close to a production environment
* Easily extensible
* Convenient development

**Alternatives** to this approach:
* Use Airflow natively via pip (not really an option on Windows)
* Use Airflow natively via WSL (works ok but not really convenient in my opinion)

**Advantages of this solution**:
* Having a local environment that is way closer to an actual production deployment
* Great development experience as DAGs and Plugins are directly mounted to the Airflow Docker Container. Develop on the host with your preferred IDE and directly see the results in your Docker environment

![airflow-dev-env-overview-v1.0.png](https://raw.githubusercontent.com/tfreundo/airflow-dev-env/feature/improve-docs/images/airflow-dev-env-overview-v1.0.png)

## Installation
Simply run `docker-compose up -d` and you're up and running.
If everything worked, your Airflow should be ready under `http://localhost:8080/`. You can further evaluate that everything works as expected, by executing the `example_dag`.

## Usage
For the developer documentation have a look at the [Wiki](https://github.com/tfreundo/airflow-dev-env/wiki).

## Troubleshooting
For known issues and their solutions see [Troubleshooting.md](Troubleshooting.md)

## License
See [License](LICENSE)
