import unittest

from src.config import load_config
from unittest.mock import patch, mock_open


class TestConfig(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"default_provider": "openai"}')
    def test_load_config(self, mock_file):
        # Mock the file system to simulate a configuration file
        with patch("os.path.isfile", return_value=True):
            config = load_config()
            self.assertEqual(config, {"default_provider": "openai"})

    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    def test_load_config_empty(self, mock_file):
        # Mock the file system to simulate an empty configuration file
        with patch("os.path.isfile", return_value=True):
            config = load_config()
            self.assertEqual(config, {})

    def test_load_config_no_file(self):
        # Mock the file system to simulate a missing configuration file
        with patch("os.path.isfile", return_value=False):
            config = load_config()
            self.assertEqual(config, {})

if __name__ == '__main__':
    unittest.main()
