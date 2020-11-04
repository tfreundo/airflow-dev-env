# simple_etl
A simple ETL pipeline using a MongoDB as source database and Hadoop as destination.
As database the [Zip Code Dataset](https://docs.mongodb.com/manual/tutorial/aggregation-zip-code-data-set/) for a [MongoDB](https://www.mongodb.com/) is used.

For the connection between the MongoDB and Hadoop, the [mongo-hadoop Connector](https://github.com/mongodb/mongo-hadoop) resp. the Python wrapper [pymongo_hadoop](https://pypi.org/project/pymongo_hadoop/) is utilized.

## How to set it up

### Start the local MongoDB
1. Change into the `/db` folder
1. Build the docker image using `docker build -t mongodb .`
1. Run the docker container using `docker run -d -p 27017:27017 --name mongodb mongodb`
1. Attach a shell to your container using `docker exec -it mongodb`
1. Import the sample dataset using `mongoimport -v --file zips.json`
1. Have a look at your database and validate that everythings fine. You should now have a collection `test/zips` with around 29K samples

### Start a local Hadoop
TODO: See [here](https://clubhouse.io/developer-how-to/how-to-set-up-a-hadoop-cluster-in-docker/)
