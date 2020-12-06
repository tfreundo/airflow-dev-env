"""
A CLI that allows you to easily manage your airflow-dev-env
"""
import sys
from PyInquirer import style_from_dict, prompt
import subprocess

banner = """
                ___ _                              _
       _      / ___)_ )                           ( )
   _ _(_)_ __| (__  | |   _   _   _   _ ______   _| |  __  _   _ ______   __   ___  _   _
 / _  ) |  __)  __) | | / _ \( ) ( ) ( )______)/ _  |/ __ \ ) ( )______)/ __ \  _  \ ) ( )
( (_| | | |  | |    | |( (_) ) \_/ \_/ |      ( (_| |  ___/ \_/ |      (  ___/ ( ) | \_/ |
 \__ _)_)_)  (_)   (___)\___/ \__/\___/        \__ _)\____)\___/        \____)_) (_)\___/
"""

def manage_extensions_selection():
  extension_selection_prompt = {
    "type": "list",
    "name": "extension_selection",
    "message": "Which extension?",
    "choices": ["MongoDB"]
  }
  answers = prompt(extension_selection_prompt)
  manage_extension(answers["extension_selection"])

def manage_extension(extension_name):
  mgmt_selection_prompt = {
    "type": "list",
    "name": "mgmt_selection",
    "message": "What to do?",
    "choices": ["1. Get the Repository", "2. Build the Container", "3. Start the Container", "Back to Main Menu"]
  }
  answer = prompt(mgmt_selection_prompt)["mgmt_selection"]
  
  mongodb_repo_foldername = "airflow-dev-env-extensions/airflow-dev-env-mongodb"
  mongodb_image_name = "custom_mongo:latest"

  if answer == "1. Get the Repository":
    if extension_name == "MongoDB":
      subprocess.call(["cd", "../..", "&&", "git", "clone", "https://github.com/tfreundo/airflow-dev-env-mongodb", mongodb_repo_foldername], shell = True)
    manage_extension(extension_name)
  elif answer == "2. Build the Container":
    if extension_name == "MongoDB":
      subprocess.call(["cd", "../../" + mongodb_repo_foldername, "&&", "docker", "build", "--tag", mongodb_image_name, "."], shell = True)
    manage_extension(extension_name)
  elif answer == "3. Start the Container":
    if extension_name == "MongoDB":
      subprocess.call(["cd", "../../" + mongodb_repo_foldername, "&&", "docker", "run", "-d", "--publish", "27017:27017", "--network", "airflow-dev-env", "--name", "mongo", mongodb_image_name], shell = True)
      print("### HINT ###")
      print("Be aware, that your Airflow Setup needs pymongo in order to work with this extension. Activate 'all_dbs' in your Airflow Extra Packages in the Docker file (or via this CLI)!")
    manage_extension(extension_name)
  elif answer == "Back to Main Menu":
    main()

def main():
  print(banner)

  main_menu_prompt = {
    "type": "list",
    "name": "main_menu",
    "message": "How can I help?",
    "choices": ["Manage airflow-dev-env Extension", "Manage Airflow Extra Packages", "Exit"]
  }
  answers = prompt(main_menu_prompt)
  main_menu_answer = answers["main_menu"]

  if main_menu_answer == "Manage airflow-dev-env Extension":
    manage_extensions_selection()
  elif main_menu_answer == "Manage Airflow Extra Packages":
    print("Sorry, this is not implemented yet!")
    main()
  else:
    sys.exit()

if __name__ == "__main__":
    main()