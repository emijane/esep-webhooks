import json
import unittest
from unittest.mock import MagicMock, patch
from lambda_function import lambda_handler


class HandlerTests(unittest.TestCase):
    def test_ping_is_ignored(self):
        with patch("lambda_function.urllib.request.urlopen") as send:
            self.assertEqual(lambda_handler({"zen": "hello"}, None), "ignored")
            send.assert_not_called()

    @patch.dict("os.environ", {"SLACK_URL": "https://example.invalid/webhook"})
    def test_issue_posts_correct_message(self):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b"ok"
        with patch("lambda_function.urllib.request.urlopen", return_value=response) as send:
            url = "https://github.com/emijane/esep-webhooks/issues/1"
            self.assertEqual(lambda_handler({"issue": {"html_url": url}}, None), "ok")
            request = send.call_args.args[0]
            self.assertEqual(json.loads(request.data), {"text": f"issue created: {url}"})
            self.assertEqual(request.get_method(), "POST")

    @patch.dict("os.environ", {"SLACK_URL": "https://example.invalid/webhook"})
    def test_failure_does_not_expose_url(self):
        with patch("lambda_function.urllib.request.urlopen", side_effect=Exception("secret URL")):
            with self.assertRaisesRegex(RuntimeError, "Slack notification failed") as error:
                lambda_handler({"issue": {"html_url": "https://example.com/issue"}}, None)
            self.assertNotIn("secret URL", str(error.exception))


if __name__ == "__main__":
    unittest.main()
