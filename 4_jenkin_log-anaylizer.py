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
