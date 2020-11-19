read -p "[Q] Should I add the sample dataset 'zips.json' to your MongoDB? [y/n] " mongo_sampledataset_zips
if [ $mongo_sampledataset_zips == "y" ]; then
    echo "[STEP] Adding sample dataset ..."
    docker exec mongo mongoimport -v --file zips.json
fi