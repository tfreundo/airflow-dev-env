# Troubleshooting

## Behind a (corporate) proxy
In general it should be enough to configure your proxy via environment variables resp. the Docker proxy settings.
Alternatively, you can add the proxy settings explicitly:

Insert

    ENV HTTP_PROXY http://your-proxy.com:8080
    ENV HTTPS_PROXY http://your-proxy.com:8080
    ENV http_proxy http://your-proxy.com:8080
    ENV https_proxy http://your-proxy.com:8080

into the following files:
* `/db/Dockerfile`

## Docker Compose failed to build - Filesharing has been cancelled
Problem: An error like `ERROR: for docker-airflow_webserver_1  Cannot create container for service webserver: status code not OK but 500`

Solution: Add the directory of this repository in your Docker settings under "Resources" - "File Sharing"

See also [here](https://stackoverflow.com/questions/60754297/docker-compose-failed-to-build-filesharing-has-been-cancelled)
