"""Forward GitHub issue events to the class Slack channel."""
import json
import os
import urllib.request


def lambda_handler(event, context):
    # API Gateway REST integration passes the original JSON, without a proxy wrapper.
    issue_url = (event.get("issue") or {}).get("html_url")
    if not issue_url:
        return "ignored"
    slack_url = os.environ.get("SLACK_URL")
    if not slack_url:
        raise RuntimeError("SLACK_URL environment variable is missing")
    request = urllib.request.Request(
        slack_url,
        data=json.dumps({"text": f"issue created: {issue_url}"}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    # Stay inside GitHub's delivery timeout; never log the secret webhook URL.
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            result = response.read().decode("utf-8")
        if result != "ok":
            raise RuntimeError("Slack did not acknowledge the notification")
    except Exception:
        raise RuntimeError("Slack notification failed; check Lambda configuration") from None
    return result
