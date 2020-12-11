"""
A CLI that allows you to easily manage your airflow-dev-env
"""
import sys
from PyInquirer import style_from_dict, prompt, Separator
import subprocess
from manage_config import *

banner = """
                ___ _                               _
       _      / ___)_ )                            ( )
   _ _(_)_ __| (__  | |   _   _   _   _  ______   _| |  __  _   _  ______   __   ___  _   _
 / _  ) |  __)  __) | | / _ \( ) ( ) ( )(______)/ _  |/ __ \ ) ( )(______)/ __ \  _  \ ) ( )
( (_| | | |  | |    | |( (_) ) \_/ \_/ |       ( (_| |  ___/ \_/ |       (  ___/ ( ) | \_/ |
 \__ _)_)_)  (_)   (___)\___/ \__/\___/         \__ _)\____)\___/         \____)_) (_)\___/
"""


def manage_extensions_selection():
    extension_selection_prompt = {
        "type": "list",
        "name": "extension_selection",
        "message": "Which extension?",
        "choices": [EXTENSION_MONGODB_NAME]
    }
    answers = prompt(extension_selection_prompt)
    manage_extension(answers["extension_selection"])


def manage_extension(extension_name):
    mgmt_selection_prompt = {
        "type": "list",
        "name": "mgmt_selection",
        "message": "What to do?",
        "choices": [CHOICE_EXTENSION_GETREPO, CHOICE_EXTENSION_BUILDCONTAINER, CHOICE_EXTENSION_STARTCONTAINER, CHOICE_BACKTO_MAINMENU]
    }
    answer = prompt(mgmt_selection_prompt)["mgmt_selection"]

    if answer == CHOICE_EXTENSION_GETREPO:
        if extension_name == EXTENSION_MONGODB_NAME:
            subprocess.call(["git", "clone",
                             "https://github.com/tfreundo/airflow-dev-env-mongodb", EXTENSION_MONGODB_REPO_FOLDER], cwd="../../", shell=True)
        manage_extension(extension_name)
    elif answer == CHOICE_EXTENSION_BUILDCONTAINER:
        if extension_name == EXTENSION_MONGODB_NAME:
            subprocess.call(["docker", "build", "--tag", EXTENSION_MONGODB_DOCKER_IMAGE_NAME,
                             "."], cwd=f"../../{EXTENSION_MONGODB_REPO_FOLDER}", shell=True)
        manage_extension(extension_name)
    elif answer == CHOICE_EXTENSION_STARTCONTAINER:
        if extension_name == EXTENSION_MONGODB_NAME:
            subprocess.call(["docker", "run", "-d", "--publish",
                             "27017:27017", "--network", "airflow-dev-env", "--name", "mongo", EXTENSION_MONGODB_DOCKER_IMAGE_NAME], cwd=f"../../{EXTENSION_MONGODB_REPO_FOLDER}", shell=True)
            print("### HINT ###")
            print("Be aware, that your Airflow Setup needs pymongo in order to work with this extension. Activate 'all_dbs' in your Airflow Extra Packages in the Docker file (or via this CLI)!")
        manage_extension(extension_name)
    elif answer == CHOICE_BACKTO_MAINMENU:
        main()


def get_checked_extrapackages():
    """
    Reads the Airflow Dockerfile and returns all lines and which packages are currently set
    """
    with open("../../docker/airflow/Dockerfile") as f:
        while True:
            line = f.readline()

            if not line:
                break
            if "RUN pip install --no-cache-dir --user" in line:
                pkgs = line.strip().split("[")[1].split("]")[0].split(",")
                return [pkg.strip().lstrip() for pkg in pkgs]
    return []


def is_extrapackages_checked(active_packages, package_name):
    """
    Checks if the given package_name is under the already activate packages
    """
    if package_name in active_packages:
        return True
    else:
        return False


def write_extrapackages(packages):
    lines = []
    with open("../../docker/airflow/Dockerfile", "r") as fin:
        lines = fin.readlines()

    lines_without_pipinstall = []
    # Remove the old pip install
    for line in lines:
        if not "RUN pip install --no-cache-dir --user" in line:
            lines_without_pipinstall.append(line)
    # Add the new pip install
    if len(packages) > 0:
        lines_without_pipinstall.append(
            f"RUN pip install --no-cache-dir --user \"apache-airflow[{','.join(packages)}]\"")

    with open("../../docker/airflow/Dockerfile", "w") as fout:
        fout.writelines(lines_without_pipinstall)


def manage_extrapackages():
    # Read current setting
    active_pkgs = get_checked_extrapackages()
    print(f"Already selected Airflow extra packages: {active_pkgs}")

    mgmt_extrapkgs_prompt = [
        {
            'type': 'checkbox',
            'message': 'Select Airflow Extra Packages',
            'name': 'airflow_extrapkgs',
            'choices': [
                Separator('= Fundamentals ='),
                {
                    'name': 'all',
                    "checked": is_extrapackages_checked(active_pkgs, "all")
                },
                {
                    'name': 'all_dbs',
                    "checked": is_extrapackages_checked(active_pkgs, "all_dbs")
                },
                {
                    'name': 'devel',
                    "checked": is_extrapackages_checked(active_pkgs, "devel")
                },
                {
                    'name': 'devel_all',
                    "checked": is_extrapackages_checked(active_pkgs, "devel_all")
                },
                {
                    'name': 'devel_azure',
                    "checked": is_extrapackages_checked(active_pkgs, "devel_azure")
                },
                {
                    'name': 'devel_ci',
                    "checked": is_extrapackages_checked(active_pkgs, "devel_ci")
                },
                {
                    'name': 'devel_hadoop',
                    "checked": is_extrapackages_checked(active_pkgs, "devel_hadoop")
                },
                {
                    'name': 'doc',
                    "checked": is_extrapackages_checked(active_pkgs, "doc")
                },
                {
                    'name': 'password',
                    "checked": is_extrapackages_checked(active_pkgs, "password")
                },
                Separator('= Apache Software ='),
                {
                    'name': 'apache.atlas',
                    "checked": is_extrapackages_checked(active_pkgs, "apache.atlas")
                },
                {
                    'name': 'apache.cassandra',
                    "checked": is_extrapackages_checked(active_pkgs, "apache.cassandra")
                },
                {
                    'name': 'apache.druid',
                    "checked": is_extrapackages_checked(active_pkgs, "apache.druid")
                },
                {
                    'name': 'apache.hdfs',
                    "checked": is_extrapackages_checked(active_pkgs, "apache.hdfs")
                },
                {
                    'name': 'apache.hive',
                    "checked": is_extrapackages_checked(active_pkgs, "apache.hive")
                },
                {
                    'name': 'apache.presto',
                    "checked": is_extrapackages_checked(active_pkgs, "apache.presto")
                },
                {
                    'name': 'webhdfs',
                    "checked": is_extrapackages_checked(active_pkgs, "webhdfs")
                },
                Separator('= Services ='),
                {
                    'name': 'amazon',
                    "checked": is_extrapackages_checked(active_pkgs, "amazon")
                },
                {
                    'name': 'microsoft.azure',
                    "checked": is_extrapackages_checked(active_pkgs, "microsoft.azure")
                },
                {
                    'name': 'azure_blob_storage',
                    "checked": is_extrapackages_checked(active_pkgs, "azure_blob_storage")
                },
                {
                    'name': 'azure_cosmos',
                    "checked": is_extrapackages_checked(active_pkgs, "azure_cosmos")
                },
                {
                    'name': 'azure_container_instances',
                    "checked": is_extrapackages_checked(active_pkgs, "azure_container_instances")
                },
                {
                    'name': 'azure_data_lake',
                    "checked": is_extrapackages_checked(active_pkgs, "azure_data_lake")
                },
                {
                    'name': 'azure_secrets',
                    "checked": is_extrapackages_checked(active_pkgs, "azure_secrets")
                },
                {
                    'name': 'cloudant',
                    "checked": is_extrapackages_checked(active_pkgs, "cloudant")
                },
                {
                    'name': 'databricks',
                    "checked": is_extrapackages_checked(active_pkgs, "databricks")
                },
                {
                    'name': 'datadog',
                    "checked": is_extrapackages_checked(active_pkgs, "datadog")
                },
                {
                    'name': 'gcp',
                    "checked": is_extrapackages_checked(active_pkgs, "gcp")
                },
                {
                    'name': 'github_enterprise',
                    "checked": is_extrapackages_checked(active_pkgs, "github_enterprise")
                },
                {
                    'name': 'google',
                    "checked": is_extrapackages_checked(active_pkgs, "google")
                },
                {
                    'name': 'google_auth',
                    "checked": is_extrapackages_checked(active_pkgs, "google_auth")
                },
                {
                    'name': 'hashicorp',
                    "checked": is_extrapackages_checked(active_pkgs, "hashicorp")
                },
                {
                    'name': 'jira',
                    "checked": is_extrapackages_checked(active_pkgs, "jira")
                },
                {
                    'name': 'qds',
                    "checked": is_extrapackages_checked(active_pkgs, "qds")
                },
                {
                    'name': 'salesforce',
                    "checked": is_extrapackages_checked(active_pkgs, "salesforce")
                },
                {
                    'name': 'sendgrid',
                    "checked": is_extrapackages_checked(active_pkgs, "sendgrid")
                },
                {
                    'name': 'segment',
                    "checked": is_extrapackages_checked(active_pkgs, "segment")
                },
                {
                    'name': 'sentry',
                    "checked": is_extrapackages_checked(active_pkgs, "sentry")
                },
                {
                    'name': 'slack',
                    "checked": is_extrapackages_checked(active_pkgs, "slack")
                },
                {
                    'name': 'snowflake',
                    "checked": is_extrapackages_checked(active_pkgs, "snowflake")
                },
                {
                    'name': 'vertica',
                    "checked": is_extrapackages_checked(active_pkgs, "vertica")
                },
                Separator('= Software ='),
                {
                    'name': 'async',
                    "checked": is_extrapackages_checked(active_pkgs, "async")
                },
                {
                    'name': 'Olives',
                    "checked": is_extrapackages_checked(active_pkgs, "Olives")
                },
                {
                    'name': 'celery',
                    "checked": is_extrapackages_checked(active_pkgs, "celery")
                },
                {
                    'name': 'dask',
                    "checked": is_extrapackages_checked(active_pkgs, "dask")
                },
                {
                    'name': 'docker',
                    "checked": is_extrapackages_checked(active_pkgs, "docker")
                },
                {
                    'name': 'elasticsearch',
                    "checked": is_extrapackages_checked(active_pkgs, "elasticsearch")
                },
                {
                    'name': 'cncf.kubernetes',
                    "checked": is_extrapackages_checked(active_pkgs, "cncf.kubernetes")
                },
                {
                    'name': 'mongo',
                    "checked": is_extrapackages_checked(active_pkgs, "mongo")
                },
                {
                    'name': 'microsoft.mssql',
                    "checked": is_extrapackages_checked(active_pkgs, "microsoft.mssql")
                },
                {
                    'name': 'mysql',
                    "checked": is_extrapackages_checked(active_pkgs, "mysql")
                },
                {
                    'name': 'oracle',
                    "checked": is_extrapackages_checked(active_pkgs, "oracle")
                },
                {
                    'name': 'pinot',
                    "checked": is_extrapackages_checked(active_pkgs, "pinot")
                },
                {
                    'name': 'postgres',
                    "checked": is_extrapackages_checked(active_pkgs, "postgres")
                },
                {
                    'name': 'rabbitmq',
                    "checked": is_extrapackages_checked(active_pkgs, "rabbitmq")
                },
                {
                    'name': 'redis',
                    "checked": is_extrapackages_checked(active_pkgs, "redis")
                },
                {
                    'name': 'samba',
                    "checked": is_extrapackages_checked(active_pkgs, "samba")
                },
                {
                    'name': 'statsd',
                    "checked": is_extrapackages_checked(active_pkgs, "statsd")
                },
                {
                    'name': 'virtualenv',
                    "checked": is_extrapackages_checked(active_pkgs, "virtualenv")
                },
                Separator('= Other ='),
                {
                    'name': 'cgroups',
                    "checked": is_extrapackages_checked(active_pkgs, "cgroups")
                },
                {
                    'name': 'crypto',
                    "checked": is_extrapackages_checked(active_pkgs, "crypto")
                },
                {
                    'name': 'grpc',
                    "checked": is_extrapackages_checked(active_pkgs, "grpc")
                },
                {
                    'name': 'jdbc',
                    "checked": is_extrapackages_checked(active_pkgs, "jdbc")
                },
                {
                    'name': 'kerberos',
                    "checked": is_extrapackages_checked(active_pkgs, "kerberos")
                },
                {
                    'name': 'ldap',
                    "checked": is_extrapackages_checked(active_pkgs, "ldap")
                },
                {
                    'name': 'papermill',
                    "checked": is_extrapackages_checked(active_pkgs, "papermill")
                },
                {
                    'name': 'ssh',
                    "checked": is_extrapackages_checked(active_pkgs, "ssh")
                },
                {
                    'name': 'microsoft.winrm',
                    "checked": is_extrapackages_checked(active_pkgs, "microsoft.winrm")
                }
            ]
        }
    ]

    pkgs_to_add = prompt(mgmt_extrapkgs_prompt)["airflow_extrapkgs"]
    print(f"Adding Airflow extra packages to Dockerfile: {pkgs_to_add}")
    write_extrapackages(pkgs_to_add)

    print("### HINT ###")
    print("Rebuild the Airflow Docker Container!")

def main():
    print(banner)

    main_menu_prompt = {
        "type": "list",
        "name": "main_menu",
        "message": "How can I help?",
        "choices": [CHOICE_MAINMENU_MANAGEEXTENSIONS, CHOICE_MAINMENU_MANAGEAIRFLOWEXTRAS, CHOICE_MAINMENU_EXIT]
    }
    answers = prompt(main_menu_prompt)
    main_menu_answer = answers["main_menu"]

    if main_menu_answer == CHOICE_MAINMENU_MANAGEEXTENSIONS:
        manage_extensions_selection()
    elif main_menu_answer == CHOICE_MAINMENU_MANAGEAIRFLOWEXTRAS:
        manage_extrapackages()
        main()
    elif main_menu_answer == CHOICE_MAINMENU_EXIT:
        sys.exit()

if __name__ == "__main__":
    main()