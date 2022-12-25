import os
import pathlib
import unittest
import yaml

import main

TESTCASE_PATH = pathlib.Path("../../testcase")


class TestMain(unittest.TestCase):
    def test_all(self):
        input_paths = os.listdir(TESTCASE_PATH / "input")
        input_paths = filter(
            lambda x: os.path.isfile(TESTCASE_PATH / "input" / x), input_paths
        )

        for input_path in input_paths:
            with self.subTest(msg=input_path):  # msg is displayed when a subtest fails
                actual = main.main(TESTCASE_PATH / "input" / input_path, False)
                with open(
                    TESTCASE_PATH / "expected" / input_path, "r"
                ) as expected_file:
                    expected = yaml.full_load(expected_file)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
