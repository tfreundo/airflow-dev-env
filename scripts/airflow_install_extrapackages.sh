# See extra packages that are available for installation here: https://airflow.apache.org/docs/stable/installation.html
read -p "[Q] Type extra package to install (e.g. all_dbs) " pkg_to_install

echo "[STEP] Installing package [$pkg_to_install] ..."
docker exec airflow_webserver pip install "apache-airflow[$pkg_to_install]"
