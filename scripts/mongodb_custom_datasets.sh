read -p "[Q] Enter your (local) path to the JSON file you want to import into your MongoDB: " mongo_from_file
echo "[STEP] Copying file ..."
docker cp $mongo_from_file mongo:/home/
read -p "[Q] Database name: " mongo_database
read -p "[Q] Collection name: " mongo_collection

docker exec mongo mongoimport --db $mongo_database --collection $mongo_collection --type json --file $mongo_from_file