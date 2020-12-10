"""
A Watchdog that can sync an external repository containing DAGs and Plugins 
with the Airflow instance of airflow-dev-env
"""
import json
import subprocess
import sys
import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

banner = """
(\,-----------------------'()'--o
 (_    _airflow-watchdog_    /~" 
  (_)_)                 (_)_)
"""


class AirflowWatchdog:

    AIRFLOW_OBJECT_TYPE_DAGS = "dags"
    AIRFLOW_OBJECT_TYPE_HOOKS = "hooks"
    AIRFLOW_OBJECT_TYPE_OPERATORS = "operators"
    AIRFLOW_OBJECT_TYPE_SENSORS = "sensors"

    eventhandlers = []
    observers = []

    def __init__(self):
        self.config = self.Config()
        self.utils: self.Utils = self.Utils()

    def start(self):
        if self.config.dags_source:
            name = "DAGs-Watchdog"
            event_handler = RepoSyncHandler(name, watch_dir=self.config.dags_source,
                                            sync_destination=self.Utils.path_to(self.AIRFLOW_OBJECT_TYPE_DAGS))
            self.eventhandlers.append(event_handler)
            observer = Observer()
            observer.setName(name)
            observer.schedule(
                event_handler, self.config.dags_source, recursive=True)
            self.observers.append(observer)
            observer.start()
        if self.config.hooks_source:
            name = "Hooks-Watchdog"
            event_handler = RepoSyncHandler(name, watch_dir=self.config.hooks_source,
                                            sync_destination=self.Utils.path_to(self.AIRFLOW_OBJECT_TYPE_HOOKS))
            self.eventhandlers.append(event_handler)
            observer = Observer()
            observer.setName(name)
            observer.schedule(
                event_handler, self.config.hooks_source, recursive=True)
            self.observers.append(observer)
            observer.start()
        if self.config.operators_source:
            name = "Operators-Watchdog"
            event_handler = RepoSyncHandler(name, watch_dir=self.config.operators_source,
                                            sync_destination=self.Utils.path_to(self.AIRFLOW_OBJECT_TYPE_OPERATORS))
            self.eventhandlers.append(event_handler)
            observer = Observer()
            observer.setName(name)
            observer.schedule(
                event_handler, self.config.operators_source, recursive=True)
            self.observers.append(observer)
            observer.start()
        if self.config.sensors_source:
            name = "Sensors-Watchdog"
            event_handler = RepoSyncHandler(name, watch_dir=self.config.sensors_source,
                                            sync_destination=self.Utils.path_to(self.AIRFLOW_OBJECT_TYPE_SENSORS))
            self.eventhandlers.append(event_handler)
            observer = Observer()
            observer.setName(name)
            observer.schedule(
                event_handler, self.config.sensors_source, recursive=True)
            self.observers.append(observer)
            observer.start()

    def status(self):
        if len(self.observers) > 0:
            print(
                f"There are currently {len(self.observers)} Watchdogs active")
            for i in range(len(self.observers)):
                watch_dir = self.eventhandlers[i].watch_dir
                sync_dir = self.eventhandlers[i].sync_destination
                print(
                    f"[{i}] {self.observers[i].getName()} (isAlive = {self.observers[i].is_alive()}): Watching '{watch_dir}' ===syncing===> '{sync_dir}'")
        else:
            print("No Watchdogs active")

    def stop(self):
        for observer in self.observers:
            observer.stop()
            observer.join()
        self.eventhandlers.clear()
        self.observers.clear()

    def sync(self):
        if self.config.dags_source:
            self.__sync_by_airflow_object_type(self.AIRFLOW_OBJECT_TYPE_DAGS)
        if self.config.hooks_source:
            self.__sync_by_airflow_object_type(self.AIRFLOW_OBJECT_TYPE_HOOKS)
        if self.config.operators_source:
            self.__sync_by_airflow_object_type(self.AIRFLOW_OBJECT_TYPE_OPERATORS)
        if self.config.sensors_source:
            self.__sync_by_airflow_object_type(self.AIRFLOW_OBJECT_TYPE_SENSORS)
    
    def __sync_by_airflow_object_type(self, airflow_object_type):

        source = None

        if airflow_object_type ==  self.AIRFLOW_OBJECT_TYPE_DAGS:
            source = self.config.dags_source
        if airflow_object_type ==  self.AIRFLOW_OBJECT_TYPE_HOOKS:
            source = self.config.hooks_source
        if airflow_object_type ==  self.AIRFLOW_OBJECT_TYPE_OPERATORS:
            source = self.config.operators_source
        if airflow_object_type ==  self.AIRFLOW_OBJECT_TYPE_SENSORS:
            source = self.config.sensors_source

        print(f"Synchronizing {source}")
        all_files_and_folders = sorted(source.glob("**/*"))
        all_files = [x for x in all_files_and_folders if x.is_file()]
        # Create all folders
        all_folders = [x for x in all_files_and_folders if x.is_dir()]
        for dir in all_folders:
            src_from_sub_path_parts = Path(str(dir).split(str(source))[1]).parts[1:]
            dst_path = self.Utils.add_parts_to_path(self.Utils.path_to(airflow_object_type), src_from_sub_path_parts)
            print(f"Creating folders: {dst_path}")
            self.utils.create_dir(dst=dst_path)

        for f in all_files:
            print(f"Creating file: {f}")
            src_from_sub_path_parts = Path(str(f).split(str(source))[1]).parts[1:]
            dst_path = self.Utils.add_parts_to_path(self.Utils.path_to(airflow_object_type), src_from_sub_path_parts).parent

            self.utils.copy(src=f,
                        dst=dst_path)

    class Utils:

        @staticmethod
        def win_powershell_prefix():
            """Checks if the system runs on Windows and returns a powershell as prefix if so
            """
            if sys.platform == "win32":
                return "powershell "
            else:
                return ""

        @staticmethod
        def path_to(airflow_object_type):
            """Returns the path to the airflow_object_type (DAGs, Plugins)
            """
            if airflow_object_type == AirflowWatchdog.AIRFLOW_OBJECT_TYPE_DAGS:
                return (Path.cwd() / "../../airflow/dags").resolve()
            elif airflow_object_type == AirflowWatchdog.AIRFLOW_OBJECT_TYPE_HOOKS:
                return (Path.cwd() / "../../airflow/plugins/hooks").resolve()
            elif airflow_object_type == AirflowWatchdog.AIRFLOW_OBJECT_TYPE_OPERATORS:
                return (Path.cwd() / "../../airflow/plugins/operators").resolve()
            elif airflow_object_type == AirflowWatchdog.AIRFLOW_OBJECT_TYPE_SENSORS:
                return (Path.cwd() / "../../airflow/plugins/sensors").resolve()
            else:
                return None

        @staticmethod
        def add_parts_to_path(path, parts):
            p = Path(path)
            for part in parts:
                p = p / part
            return p

        def create_dir(self, dst):
            subprocess.call(f"{self.win_powershell_prefix()}mkdir {dst}",
                            shell=True)

        def copy(self, src, dst):
            subprocess.call(f"{self.win_powershell_prefix()}cp {src}",
                            cwd=dst, shell=True)

        def remove(self, src, dst):
            subprocess.call(f"{self.win_powershell_prefix()}rm -r .{src}",
                            cwd=dst, shell=True)

        def move(self, src_dir, src_sub_path_from_parts, src_sub_path_to_parts, dst):
            dst_previous_path = self.add_parts_to_path(dst, src_sub_path_from_parts)
            dst_new_path = self.add_parts_to_path(dst, src_sub_path_to_parts)
            src_new_path = self.add_parts_to_path(src_dir, src_sub_path_to_parts)
            # If it does not yet exist in dst, copy instead of move
            if dst_previous_path.exists():
                subprocess.call(f"{self.win_powershell_prefix()}mv {dst_previous_path} {dst_new_path}",
                                cwd=dst, shell=True)
            else:
                self.copy(src=src_new_path, dst=dst_new_path.parent)

    class Config:
        dags_source: Path = None
        hooks_source: Path = None
        operators_source: Path = None
        sensors_source: Path = None

        def __init__(self):
            self.__load()

        def __load(self):
            with open("watchdog_config.json") as f:
                config = json.load(f)
                if config["dags_source"]:
                    self.dags_source = Path(config["dags_source"])
                if config["hooks_source"]:
                    self.hooks_source = Path(config["hooks_source"])
                if config["operators_source"]:
                    self.operators_source = Path(config["operators_source"])
                if config["sensors_source"]:
                    self.sensors_source = Path(config["sensors_source"])


class RepoSyncHandler(FileSystemEventHandler):

    def __init__(self, name, watch_dir:Path, sync_destination:Path):
        self.name = name
        self.watch_dir = watch_dir
        self.sync_destination = sync_destination
        self.utils: AirflowWatchdog.Utils = AirflowWatchdog.Utils()
        super().__init__()

    def on_created(self, event):
        print(
            f"[{self.name}] Created '{event.src_path}', syncing after Modification ...")

    def on_modified(self, event):
        # If it's a folder, just skip as we sync just the files located unter that folder
        src_from_path = Path(event.src_path)
        src_from_sub_path_parts = Path(str(src_from_path).split(str(self.watch_dir))[1]).parts[1:]
        dst_path = AirflowWatchdog.Utils.add_parts_to_path(self.sync_destination, src_from_sub_path_parts).parent

        if not os.path.isdir(event.src_path):
            print(
                f"[{self.name}] Modified '{event.src_path}', ===syncing===> '{self.sync_destination}' ...")
            self.utils.copy(src=event.src_path, dst=dst_path)

    def on_deleted(self, event):
        src_sub_path = Path(str(event.src_path).split(str(self.watch_dir))[1])
        print(
            f"[{self.name}] Deleted '{event.src_path}', ===syncing===> '{self.sync_destination}' ...")
        self.utils.remove(src=src_sub_path, dst=self.sync_destination)

    def on_moved(self, event):
        src_from_path = Path(event.src_path)
        src_to_path = Path(event.dest_path)
        # Path Parts without root dir as this is just sub paths!
        src_from_sub_path_parts = Path(str(src_from_path).split(str(self.watch_dir))[1]).parts[1:]
        src_to_sub_path_parts = Path(str(event.dest_path).split(str(self.watch_dir))[1]).parts[1:]
        print(
            f"[{self.name}] Moved or Renamed '{event.src_path}' to '{event.dest_path}', ===syncing===> {self.sync_destination} ...")
        self.utils.move(src_dir=self.watch_dir, src_sub_path_from_parts=src_from_sub_path_parts,
                        src_sub_path_to_parts=src_to_sub_path_parts, dst=self.sync_destination)


if __name__ == "__main__":
    print(banner)
    w = AirflowWatchdog()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--sync":
            w.sync()
    else:
        w.start()
        w.status()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            w.stop()