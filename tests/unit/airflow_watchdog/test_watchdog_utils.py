import os
from pathlib import Path
import shutil
import json
from scripts.airflow_watchdog.airflow_watchdog import AirflowWatchdog

class TestWatchdogUtils:

    # Test folders
    test_folder_root = Path().cwd() / "tests/unit/airflow_watchdog/tmp_test"
    test_folder_dags = test_folder_root / "dags/nested"
    test_folder_hooks = test_folder_root / "plugins/hooks/nested"
    test_folder_operators = test_folder_root / "plugins/operators/nested"
    test_folder_sensors = test_folder_root / "plugins/sensors/nested"

    # Test files
    test_file_dag_1 = test_folder_dags / "../my_test_dag.py"
    test_file_dag_1_initial_content = "print('I am a DAG!')"
    test_file_dag_2 = test_folder_dags / "nested_dag.py"
    test_file_dag_2_initial_content = "print('I am a nested DAG!')"

    test_file_hook_1 = test_folder_hooks / "../my_test_hook.py"
    test_file_hook_1_initial_content = "print('I am a Hook!')"
    test_file_hook_2 = test_folder_hooks / "nested_hook.py"
    test_file_hook_2_initial_content = "print('I am a nested Hook!')"

    test_file_operator_1 = test_folder_operators / "../my_test_operator.py"
    test_file_operator_1_initial_content = "print('I am a Operator!')"
    test_file_operator_2 = test_folder_operators / "nested_operator.py"
    test_file_operator_2_initial_content = "print('I am a nested Operator!')"

    test_file_sensor_1 = test_folder_sensors / "../my_test_sensor.py"
    test_file_sensor_1_initial_content = "print('I am a sensor!')"
    test_file_sensor_2 = test_folder_sensors / "nested_sensor.py"
    test_file_sensor_2_initial_content = "print('I am a nested sensor!')"

    test_files_and_contents = [
        (test_file_dag_1, test_file_dag_1_initial_content),
        (test_file_dag_2, test_file_dag_2_initial_content),
        (test_file_hook_1, test_file_hook_1_initial_content),
        (test_file_hook_2, test_file_hook_2_initial_content),
        (test_file_operator_1, test_file_operator_1_initial_content),
        (test_file_operator_2, test_file_operator_2_initial_content),
        (test_file_sensor_1, test_file_sensor_1_initial_content),
        (test_file_sensor_2, test_file_sensor_2_initial_content)
    ]

    WATCHDOG_CONFIG_FILEPATH = Path().cwd() / "tests/unit/airflow_watchdog/watchdog_config_unittests.json"

    @staticmethod
    def __create_dir(dirname):
        Path(dirname).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def __create_file(filename, content=""):
        with open(filename, "w") as f:
            f.write(content)

    @staticmethod
    def __remove(src: Path):
        try:
            if src.is_dir():
                shutil.rmtree(src)
            else:
                src.unlink()
        except FileNotFoundError as ex:
            print(f"Unable to remove file. {ex}")

    @staticmethod
    def create_test_file_and_folder_structure():
        # Create folders
        [TestWatchdogUtils.__create_dir(x) for x in [TestWatchdogUtils.test_folder_dags,
                                                     TestWatchdogUtils.test_folder_hooks,
                                                     TestWatchdogUtils.test_folder_operators,
                                                     TestWatchdogUtils.test_folder_sensors]]
        # DAGs
        TestWatchdogUtils.__create_file(
            TestWatchdogUtils.test_file_dag_1, TestWatchdogUtils.test_file_dag_1_initial_content)
        TestWatchdogUtils.__create_file(
            TestWatchdogUtils.test_file_dag_2, TestWatchdogUtils.test_file_dag_2_initial_content)
        # Hooks
        TestWatchdogUtils.__create_file(
            TestWatchdogUtils.test_file_hook_1, TestWatchdogUtils.test_file_hook_1_initial_content)
        TestWatchdogUtils.__create_file(
            TestWatchdogUtils.test_file_hook_2, TestWatchdogUtils.test_file_hook_2_initial_content)
        # Operatos
        TestWatchdogUtils.__create_file(
            TestWatchdogUtils.test_file_operator_1, TestWatchdogUtils.test_file_operator_1_initial_content)
        TestWatchdogUtils.__create_file(
            TestWatchdogUtils.test_file_operator_2, TestWatchdogUtils.test_file_operator_2_initial_content)
        # Sensors
        TestWatchdogUtils.__create_file(
            TestWatchdogUtils.test_file_sensor_1, TestWatchdogUtils.test_file_sensor_1_initial_content)
        TestWatchdogUtils.__create_file(
            TestWatchdogUtils.test_file_sensor_2, TestWatchdogUtils.test_file_sensor_2_initial_content)

    @staticmethod
    def remove_test_file_and_folder_structure():
        TestWatchdogUtils.__remove(TestWatchdogUtils.test_folder_root)

    @staticmethod
    def update_watchdog_config_for_unittests():
        with open(TestWatchdogUtils.WATCHDOG_CONFIG_FILEPATH, "w") as f:
            # TODO Update config
            config_data = {
                "dags_source": str(TestWatchdogUtils.test_folder_root / "dags"),
                "hooks_source": str(TestWatchdogUtils.test_folder_root / "plugins/hooks"),
                "operators_source": str(TestWatchdogUtils.test_folder_root / "plugins/operators"),
                "sensors_source": str(TestWatchdogUtils.test_folder_root / "plugins/sensors")
            }

            f.write(json.dumps(config_data))
    
    @staticmethod
    def get_sync_destination_path(source_path):
        """Returns the desination path where the airflow_watchdog should sync the source files to
        """
        # Points to root of the airflow-dev-env project
        sync_destination = Path().cwd() / "airflow"
        src_from_sub_path_parts = Path(str(source_path).split(str(TestWatchdogUtils.test_folder_root))[1]).parts[1:]
        dst_path = AirflowWatchdog.Utils.add_parts_to_path(sync_destination, src_from_sub_path_parts).parent
        return dst_path