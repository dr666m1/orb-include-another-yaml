import unittest

import main


class TestMain(unittest.TestCase):
    def test_upper(self):
        self.assertEqual(main.temp().upper(), "DUMMY")


if __name__ == "__main__":
    unittest.main()
