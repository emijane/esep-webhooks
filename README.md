# ESEP Webhooks

GitHub Issues → API Gateway REST API → AWS Lambda → Slack.

This assignment uses Python (an alternative language permitted by the handout) and only the standard library.

## AWS configuration

- Region: `us-east-2`
- Function: `EsepWebhook`
- Handler: `lambda_function.lambda_handler`
- Environment variable: `SLACK_URL`, configured only in Lambda
- REST API: `Esep-Webhook-Api`, root `POST`, Lambda proxy integration disabled
- Stage: `default`
- GitHub webhook: JSON, Issues events only, SSL verification enabled

Run local tests with `python3 -m unittest -v`.

Opening or updating an issue sends `issue created: <issue URL>` to Slack. GitHub ping events are ignored. Slack delivery failures raise an error without logging the webhook URL.

Never commit the Slack webhook URL or AWS credentials.

## Current deployment

The deployed handler is `lambda_function.py`. The `EsepWebhook/` directory preserves the earlier C# implementation.

API endpoint: `https://webqr49o6b.execute-api.us-east-2.amazonaws.com/default`

AWS CLI profile: `emma-uf`.
