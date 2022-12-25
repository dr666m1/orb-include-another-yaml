import os
import pathlib
import unittest
import yaml

import main

TESTCASE_PATH = pathlib.Path("../../testcase")
VALID_INPUT_PATH = TESTCASE_PATH / "input" / "valid"
INVALID_INPUT_PATH = TESTCASE_PATH / "input" / "invalid"


class TestMain(unittest.TestCase):
    def test_valid_input(self):
        inputs = os.listdir(VALID_INPUT_PATH)
        inputs = filter(lambda x: os.path.isfile(VALID_INPUT_PATH / x), inputs)

        for input_ in inputs:
            with self.subTest(msg=input_):  # msg is displayed when a subtest fails
                actual = main.main(VALID_INPUT_PATH / input_, False)
                with open(TESTCASE_PATH / "expected" / input_, "r") as f:
                    expected = yaml.full_load(f)
                self.assertEqual(actual, expected)

    def test_invalid_input(self):
        inputs = os.listdir(INVALID_INPUT_PATH)
        inputs = filter(
            lambda x: os.path.isfile(INVALID_INPUT_PATH / x),
            inputs,
        )

        for input_ in inputs:
            with self.subTest(msg=input_):  # msg is displayed when a subtest fails
                with self.assertRaises(main.Error):
                    main.main(INVALID_INPUT_PATH / input_, False)


if __name__ == "__main__":
    unittest.main()
