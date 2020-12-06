FROM apache/airflow:1.10.12
USER root
RUN apt-get update \
    && apt-get install -y build-essential \ 
    libsasl2-2 \
    libsasl2-dev \
    libsasl2-modules \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
USER airflow
# TODO Update this via CLI
# RUN pip install --no-cache-dir --user "apache-airflow[all_dbs]"