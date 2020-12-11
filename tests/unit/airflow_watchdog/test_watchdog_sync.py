import unittest
from . import test_watchdog_utils
# from scripts.watchdog.airflow_watchdog import AirflowWatchdog
from scripts.airflow_watchdog.airflow_watchdog import AirflowWatchdog
import subprocess

class TestWatchdogSync(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set up test environment (once for all tests)
        """
        super(TestWatchdogSync, cls).setUpClass()

        test_watchdog_utils.TestWatchdogUtils.update_watchdog_config_for_unittests()
        test_watchdog_utils.TestWatchdogUtils.create_test_file_and_folder_structure()
        # Exceute syncing once here and just test the result afterwards
        w = AirflowWatchdog(test_watchdog_utils.TestWatchdogUtils.WATCHDOG_CONFIG_FILEPATH)
        w.sync()

    @classmethod
    def tearDownClass(cls):
        """ Clean the test environment (once after all tests)
        """
        super(TestWatchdogSync, cls).tearDownClass()
        test_watchdog_utils.TestWatchdogUtils.remove_test_files_and_folders_structure()

    def test_files_and_contents_were_synced(self):
        """Tests that all files were synced and contain the expected content
        """
        for (filename, expected_content) in test_watchdog_utils.TestWatchdogUtils.test_files_and_contents:
            dst_file:Path = test_watchdog_utils.TestWatchdogUtils.get_sync_destination_path(filename) / filename.name
            # Check that the destination file exists
            assert(dst_file.exists())
            # Check that the content is correct
            with open(dst_file, "r") as f:
                actual_content = f.read() 
                self.assertEqual(actual_content, expected_content)

if __name__ == '__main__':
    unittest.main()