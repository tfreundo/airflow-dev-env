echo
echo "### MongoDB Setup ###"
read -p "[Q] Should I start a local MongoDB for you? [y/n] " start_mongo
if [ $start_mongo == "y" ]; then
    echo "[STEP] Starting MongoDB ..."
    cd ./db
    docker build -t mongodb .
    docker run -d -p 27017:27017 --name mongodb mongodb
    cd ..
fi
read -p "[Q] Should I additionally add the sample dataset to that MongoDB? [y/n] " mongo_sampledataset
if [ $mongo_sampledataset == "y" ]; then
    echo "[STEP] Adding the sample dataset ..."
    docker exec mongodb mongoimport -v --file zips.json
fi

echo
echo "### Airflow Setup ###"
read -p "[Q] First run? (If yes, I will also init and update the submodules) [y/n] " first_run_init_submodules
if [ $first_run_init_submodules == "y" ]; then
    echo "[STEP] Init Submodules ..."
    git submodule init
    echo "[STEP] Update Submodules ..."
    git submodule update
fi
echo "[STEP] Pulling Airflow Image ..."
docker pull puckel/docker-airflow
echo "[STEP] Building docker Container ..."
cd ./submodules/docker-airflow
docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask,all_dbs" --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t puckel/docker-airflow .
docker-compose -f docker-compose-LocalExecutor.yml up -d