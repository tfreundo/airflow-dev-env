# simple_etl_playground
A simple ETL pipeline using a MongoDB as source database.

## How to set it up

### docker-compose Setup
TODO: Coming soon

### Start the local MongoDB
1. Change into the `/db` folder
1. Build the docker image using `docker build -t mongodb .`
1. Run the docker container using `docker run -d -p 27017:27017 --name mongodb mongodb`

#### Use a sample dataset
As a sample dataset you could e.g. use the [Zip Code Dataset](https://docs.mongodb.com/manual/tutorial/aggregation-zip-code-data-set/) for [MongoDB](https://www.mongodb.com/).
For this:
1. Run the MongoDB docker container (see above)
1. Attach a shell to your container using `docker exec -it mongodb`
1. Import the sample dataset using `mongoimport -v --file zips.json`
1. Have a look at your database and validate that everythings fine. You should now have a collection `test/zips` with around 29K samples

### Start Airflow
For Airflow the pretty popular repository [docker-airflow by puckel](https://github.com/puckel/docker-airflow) is used.
This repository is referenced as a [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) located under `/submodules/docker-airflow`.

See more information there on e.g. additional configuration possibilities etc.

To summarize:
1. If you **initially cloned this repo**, run `git submodule init` so that the airflow repo is also cloned into your local setup
1. Get the image using `docker pull puckel/docker-airflow`
1. Build the container with your desired configuration (for additional packages see [here](https://airflow.apache.org/docs/stable/installation.html#extra-package)):     `docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask,all_dbs" --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t puckel/docker-airflow .`
1. Start the containers using the **LocalExecutor** with `docker-compose -f docker-compose-LocalExecutor.yml up -d`

### Start a local Hadoop
TODO: See [here](https://clubhouse.io/developer-how-to/how-to-set-up-a-hadoop-cluster-in-docker/)