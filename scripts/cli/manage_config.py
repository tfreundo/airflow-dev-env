"""
Configs and constants used by manage.py
"""
# User choices via CLI
CHOICE_EXTENSION_GETREPO = "1. Get the Repository"
CHOICE_EXTENSION_BUILDCONTAINER = "2. Build the Container"
CHOICE_EXTENSION_STARTCONTAINER = "3. Start the Container"
CHOICE_BACKTO_MAINMENU = "Back to Main Menu"
CHOICE_MAINMENU_MANAGEEXTENSIONS = "Manage airflow-dev-env Extension"
CHOICE_MAINMENU_MANAGEAIRFLOWEXTRAS = "Manage Airflow Extra Packages"
CHOICE_MAINMENU_WATCHDOG = "Watchdog"
CHOICE_MAINMENU_EXIT = "Exit"
CHOICE_WATCHDOG_TRIGGERONCE = "Trigger a sync once"

# Extensions
EXTENSION_MONGODB_NAME = "MongoDB"
EXTENSION_MONGODB_REPO_FOLDER = "airflow-dev-env-extensions/airflow-dev-env-mongodb"
EXTENSION_MONGODB_DOCKER_IMAGE_NAME = "custom_mongo:latest"