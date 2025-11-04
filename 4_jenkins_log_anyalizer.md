🧩 Automation #4: Jenkins Log Analyzer & Failure Report Generator (Python)
🧾 Problem:

In CI/CD pipelines, builds fail often for repetitive reasons — like:

Dependency install failures

Timeout/network issues

Docker build errors

Manually checking each Jenkins job log wastes time.
So I wrote a Python automation that analyzes logs and generates a daily failure summary report.

⚙️ Short Python Code Example
#!/usr/bin/env python3
import requests
import re
from datetime import datetime

JENKINS_URL = "https://jenkins.example.com"
JOB_NAME = "my-app-deploy"
USERNAME = "jenkins_user"
API_TOKEN = "your_api_token"

# Jenkins API endpoint for last 10 builds
url = f"{JENKINS_URL}/job/{JOB_NAME}/api/json?tree=builds[number,result,url]"

response = requests.get(url, auth=(USERNAME, API_TOKEN))
builds = response.json()['builds']

def analyze_log(log_text):
    if "timeout" in log_text.lower():
        return "Timeout Issue"
    elif "connection refused" in log_text.lower():
        return "Network Issue"
    elif re.search(r'Failed to download|dependency', log_text, re.I):
        return "Dependency Issue"
    elif "docker build" in log_text.lower():
        return "Docker Build Error"
    else:
        return "Other Failure"

failure_summary = {}

for build in builds[:10]:
    if build['result'] != "SUCCESS":
        log_url = f"{build['url']}consoleText"
        log_text = requests.get(log_url, auth=(USERNAME, API_TOKEN)).text
        reason = analyze_log(log_text)
        failure_summary[reason] = failure_summary.get(reason, 0) + 1

# Generate summary report
date = datetime.now().strftime("%Y-%m-%d")
print(f"Jenkins Failure Summary for {date}\n")
for issue, count in failure_summary.items():
    print(f"{issue}: {count} builds failed")

💡 How It Works:

Fetches the last 10 Jenkins builds using the REST API

Reads each build’s console log

Uses simple pattern matching to categorize failures

Summarizes results (e.g., “3 Docker errors”, “2 Network issues”)

Output can be emailed or posted to Slack (optional next step)

💬 Interview-Ready Explanation:

“We had frequent Jenkins build failures, and manually checking each log was time-consuming.
So I wrote a Python script using the Jenkins REST API that fetches the last few build logs, scans them for common error patterns like timeout, dependency, or Docker build issues, and generates a summary report.
We scheduled it as a daily cron job and sent the report to the DevOps Slack channel.
It helped the team quickly identify recurring failure trends and fix root causes faster.”

🎯 Common Follow-Up Q&A

🧩 Q1: Why use the Jenkins API instead of scraping UI?

Because Jenkins provides a clean REST API (/api/json and /consoleText), which is more reliable and script-friendly than HTML parsing.

🧩 Q2: How did you categorize failure reasons?

I used regex-based keyword matching for known patterns like "timeout", "dependency", "docker build", etc. Later, we refined it based on new patterns we found in logs.

🧩 Q3: Did you consider integrating with Slack or Email?

Yes — I extended it to send Slack messages using an incoming webhook for automated daily updates.

🧩 Q4: What’s the benefit of this automation?

It reduced log analysis time by over 70%. Instead of manually checking 20–30 builds daily, we got an automated summary showing the top failure causes.

✅ Impact you can mention:

“This script helped us spot that most failures were due to dependency timeouts. After caching dependencies in Jenkins agents, the failure rate dropped by 40%.”