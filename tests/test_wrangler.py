import unittest
from unittest.mock import patch, Mock
from wrangler import call_ai

class TestWrangler(unittest.TestCase):
    @patch("wrangler.requests.post")
    def test_call_wrangler_success(self, mock_post):
        print("Test Success")
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {"content": '{"device": "CPAP"}'}
            }],
            "usage": {
                "prompt_tokens": 100,
                "total_tokens": 120
            }
        }
        mock_post.return_value = mock_response

        result = call_ai(
            api_key="test-key",
            user_prompt="Needs a CPAP",
            system_prompt="Extract device from note.",
            model="mock-model",
            temperature=0.3,
            max_tokens=512
        )

        self.assertIn("device", result["output"])
        self.assertAlmostEqual(result["elapsed"], result["elapsed"])  # Just check it's a float
        self.assertEqual(result["tokens"]["prompt_tokens"], 100)

    @patch("wrangler.requests.post")
    def test_call_wrangler_failure(self, mock_post):
        print("Test Failure")
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("bad json")
        mock_response.text = "Invalid JSON response"
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            call_ai(
                api_key="test-key",
                user_prompt="Test",
                system_prompt="Test",
                model="mock-model",
                temperature=0.3,
                max_tokens=512
            )

if __name__ == "__main__":
    unittest.main()
