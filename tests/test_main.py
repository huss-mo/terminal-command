import sys
import unittest

from main import main
from unittest.mock import patch, MagicMock


class TestMain(unittest.TestCase):
    @patch('main.subprocess.run')
    @patch('main.get_command_from_llm')
    @patch('main.detect_suspicious_command')
    def test_main_execution(self, mock_detect_suspicious, mock_get_command, mock_subprocess):
        # Mock the functions to simulate the expected behavior
        mock_get_command.return_value = '{"command": "echo Hello", "explanation": "Prints Hello"}'
        mock_detect_suspicious.return_value = False
        mock_subprocess.return_value = MagicMock()

        # Simulate command-line arguments
        with patch('sys.argv', ['tc', 'print hello', '--execute']):
            main()

        # Verify that the functions were called with the expected arguments
        mock_get_command.assert_called_once_with("print hello")
        mock_detect_suspicious.assert_called_once_with("echo Hello")
        mock_subprocess.assert_called_once_with("echo Hello", shell=True, check=True)

    @patch('main.print')
    @patch('main.get_command_from_llm')
    @patch('main.detect_suspicious_command')
    def test_main_no_execution(self, mock_detect_suspicious, mock_get_command, mock_print):
        # Mock the functions to simulate the expected behavior
        mock_get_command.return_value = '{"command": "echo Hello", "explanation": "Prints Hello"}'
        mock_detect_suspicious.return_value = True

        # Simulate command-line arguments
        with patch('sys.argv', ['tc', 'print hello']):
            main()

        # Verify that the functions were called with the expected arguments
        mock_get_command.assert_called_once_with("print hello")
        mock_detect_suspicious.assert_called_once_with("echo Hello")
        mock_print.assert_any_call("WARNING: The command is detected as potentially dangerous.", file=sys.stderr)

if __name__ == '__main__':
    unittest.main()
