# ESEP Webhooks

Sends a Slack message when an issue is opened or updated in this repository.

GitHub → API Gateway → AWS Lambda → Slack

The Python function in `lambda_function.py` sends `issue created: <issue URL>`. The Slack webhook URL is stored in Lambda’s `SLACK_URL` environment variable.

Run tests with `python3 -m unittest -v`.
