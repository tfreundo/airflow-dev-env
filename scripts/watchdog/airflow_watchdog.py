"""
A Watchdog that can sync an external repository containing DAGs and Plugins 
with the Airflow instance of airflow-dev-env
"""
import json
import subprocess
import sys
import time
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
        self.utils:self.Utils = self.Utils() 

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
            print(f"Synchronizing {self.config.dags_source}")
            self.utils.copy(src=f"{self.config.dags_source}/*", dst=self.Utils.path_to(self.AIRFLOW_OBJECT_TYPE_DAGS))
        if self.config.hooks_source:
            print(f"Synchronizing {self.config.hooks_source}")
            self.utils.copy(src=f"{self.config.hooks_source}/*", dst=self.Utils.path_to(self.AIRFLOW_OBJECT_TYPE_HOOKS))
        if self.config.operators_source:
            print(f"Synchronizing {self.config.operators_source}")
            self.utils.copy(src=f"{self.config.operators_source}/*", dst=self.Utils.path_to(self.AIRFLOW_OBJECT_TYPE_OPERATORS))
        if self.config.sensors_source:
            print(f"Synchronizing {self.config.sensors_source}")
            self.utils.copy(src=f"{self.config.sensors_source}/*", dst=self.Utils.path_to(self.AIRFLOW_OBJECT_TYPE_SENSORS))

    class Utils:

        # TODO Move all the subprocess calls into Utils
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
                return "../../airflow/dags"
            elif airflow_object_type == AirflowWatchdog.AIRFLOW_OBJECT_TYPE_HOOKS:
                return "../../airflow/plugins/hooks"
            elif airflow_object_type == AirflowWatchdog.AIRFLOW_OBJECT_TYPE_OPERATORS:
                return "../../airflow/plugins/operators"
            elif airflow_object_type == AirflowWatchdog.AIRFLOW_OBJECT_TYPE_SENSORS:
                return "../../airflow/plugins/sensors"
            else:
                return None

        def copy(self, src, dst):
            subprocess.call(f"{self.win_powershell_prefix()}cp -r {src}",
                            cwd=dst, shell=True)

        def remove(self, src, dst):
            subprocess.call(f"{self.win_powershell_prefix()}rm -r .{src}",
                            cwd=dst, shell=True)

    class Config:
        dags_source: str = ""
        hooks_source: str = ""
        operators_source: str = ""
        sensors_source: str = ""

        def __init__(self):
            self.__load()

        def __load(self):
            with open("watchdog_config.json") as f:
                config = json.load(f)
                self.dags_source = config["dags_source"]
                self.hooks_source = config["hooks_source"]
                self.operators_source = config["operators_source"]
                self.sensors_source = config["sensors_source"]


class RepoSyncHandler(FileSystemEventHandler):

    def __init__(self, name, watch_dir, sync_destination):
        self.name = name
        self.watch_dir = watch_dir
        self.sync_destination = sync_destination
        self.utils:AirflowWatchdog.Utils = AirflowWatchdog.Utils()
        super().__init__()

    def on_created(self, event):
        print(
            f"[{self.name}] Created '{event.src_path}', I will sync on modification!")

    def on_modified(self, event):
        print(
            f"[{self.name}] Modified '{event.src_path}', syncing to '{self.sync_destination}' ...")
        self.utils.copy(src=event.src_path, dst=self.sync_destination)

    def on_deleted(self, event):
        src_sub_path = event.src_path.split(self.watch_dir)[1]
        print(
            f"[{self.name}] Deleted '{event.src_path}', syncing to '{self.sync_destination}' ...")
        self.utils.remove(src=src_sub_path, dst=self.sync_destination)

    def on_moved(self, event):
        # TODO Implement copy + delete
        print(
            f"[{self.name}] Moved or Renamed'{event.src_path}' to '{event.dest_path}', syncing to {self.sync_destination} ...")


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
