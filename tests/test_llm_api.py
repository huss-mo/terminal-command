import unittest

from src.llm_api import _build_user_prompt, get_command_from_llm, detect_suspicious_command, call_llm_api
from unittest.mock import patch

class TestLLMApi(unittest.TestCase):
    def test_build_user_prompt(self):
        user_query = "list running docker containers"
        operating_system = "Windows"
        
        # Call the function to build the user prompt
        prompt = _build_user_prompt(user_query)
        
        # Assert that the prompt contains the user query and operating system
        self.assertIn(user_query, prompt)
        self.assertIn(operating_system, prompt)

    @patch('src.llm_api.call_llm_api')
    def test_get_command_from_llm(self, mock_call_llm_api):
        # Mock the API call to return a specific response
        mock_call_llm_api.return_value = '{"command": "ls", "explanation": "List files"}'
        user_query = "list files"
        
        # Mock the configuration to return specific provider details
        with patch('src.llm_api.load_config', return_value={"default_provider": "openai", "providers": {"openai": {"api_key": "test_key", "model": "gpt-4o-mini", "api_url": "https://api.openai.com/v1/chat/completions"}}}):
            response = get_command_from_llm(user_query)
            self.assertEqual(response, '{"command": "ls", "explanation": "List files"}')

    def test_detect_suspicious_command_local(self):
        command = "rm -rf /"
        
        # Mock the configuration to disable provider-based detection
        with patch('src.llm_api.load_config', return_value={"suspicious_command_detection": {"suspicious_substrings": ["rm -rf /"], "provider_detection": {"enabled": False}}}):
            result = detect_suspicious_command(command)
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
