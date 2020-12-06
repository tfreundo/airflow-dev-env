# Troubleshooting

## Behind a (corporate) proxy
In general it should be enough to configure your proxy via environment variables resp. the Docker proxy settings.
Alternatively, you can add the proxy settings explicitly:

Insert

    ENV HTTP_PROXY http://your-proxy.com:8080
    ENV HTTPS_PROXY http://your-proxy.com:8080
    ENV http_proxy http://your-proxy.com:8080
    ENV https_proxy http://your-proxy.com:8080

into the Dockerfiles located under [docker](/docker) and into the [.env file](/.env) (without the ENV part and an `=` sign in between).

## Docker Compose failed to build - Filesharing has been cancelled
**Problem:**
* An error like `ERROR: for docker-airflow_webserver_1  Cannot create container for service webserver: status code not OK but 500`

**Solution:**
* Add the directory of this repository in your Docker settings under "Resources" - "File Sharing"
* See also [here](https://stackoverflow.com/questions/60754297/docker-compose-failed-to-build-filesharing-has-been-cancelled).

## env: bash\r: No such file or directory
**Problem:**
* An error like `env: bash\r: No such file or directory` appears when starting the docker containers (e.g. via `docker-compose up`)
* This most likely means that you're running on Windows (which means you have windows-style line endings like `\r\n` which is incompatible with Linux machines)
* It can become a problem if you develop with others on different operating systems or when you use Docker4Windows with WSL2

**Solution:**
* If you're on Windows, check that `git config core.autocrlf` returns `true` or set it accordingly
* To set this on your IDE (here VSCode) see [this](https://qvault.io/2020/06/18/how-to-get-consistent-line-breaks-in-vs-code-lf-vs-crlf/)