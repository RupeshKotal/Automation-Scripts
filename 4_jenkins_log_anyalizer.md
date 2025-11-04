Perfect 👍 Here’s your **Automation #4: Jenkins Log Analyzer & Failure Report Generator (Python)** — fully formatted as a clean, professional `README.md` entry (consistent with your previous automations):

---

````markdown
# 🧩 Automation #4: Jenkins Log Analyzer & Failure Report Generator (Python)

## 🧾 Problem

In CI/CD pipelines, builds often fail for **repetitive and predictable reasons**, such as:

- Dependency installation failures  
- Network or timeout errors  
- Docker build issues  

Manually reviewing each Jenkins job log is **time-consuming** and **inefficient**.  
To solve this, I built a Python automation that **analyzes Jenkins logs** and **generates a daily failure summary report**.

---

## ⚙️ Short Python Code Example: `jenkins_log_analyzer.py`

```python
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
````

---

## 💡 How It Works

1. **Fetches the last 10 Jenkins builds** via the REST API (`/api/json`)
2. **Retrieves console logs** for failed builds (`/consoleText`)
3. **Analyzes logs** using regex-based pattern matching for known error types
4. **Generates a summary report** — e.g.:

   ```
   Jenkins Failure Summary for 2025-11-05
   Timeout Issue: 2 builds failed
   Dependency Issue: 3 builds failed
   Docker Build Error: 1 build failed
   ```
5. The output can optionally be **emailed** or **posted to Slack** for daily visibility

---

## 💬 Interview-Ready Explanation

> “We had frequent Jenkins build failures, and manually checking each log was very time-consuming.
> So I wrote a Python script using the Jenkins REST API that fetches the latest build logs, scans them for patterns like timeout, dependency, or Docker build errors, and then generates a daily failure summary.
> We scheduled it as a daily cron job, sending the results automatically to our DevOps Slack channel.
> This helped us quickly identify recurring issues and focus on fixing root causes rather than manually investigating every job.”

---

## 🎯 Common Interview Follow-Ups

### 🧩 Q1: Why use the Jenkins API instead of scraping the UI?

> Jenkins exposes structured JSON endpoints like `/api/json` and `/consoleText`,
> which are **lightweight**, **reliable**, and **ideal for automation** — unlike web scraping, which is brittle and slow.

---

### 🧩 Q2: How did you categorize failure reasons?

> I used **regex-based keyword matching** for known patterns such as:
>
> * `"timeout"`
> * `"connection refused"`
> * `"dependency"`
> * `"docker build"`
>   Over time, we refined this list based on new error patterns in our environment.

---

### 🧩 Q3: Did you integrate it with Slack or Email?

> Yes. I extended it to post summaries to **Slack** via an **incoming webhook** every morning.
> This ensured the entire DevOps team got quick insights into build health trends.

---

### 🧩 Q4: What’s the benefit of this automation?

> It reduced manual log analysis time by **over 70%**.
> Instead of checking 20–30 Jenkins builds manually, we got a concise automated summary showing top failure causes.

---

## ✅ Impact

> “This script helped us identify that most failures were caused by dependency timeouts.
> After implementing dependency caching in Jenkins agents, the overall failure rate dropped by **40%**, and builds became more stable.”

---

## 📂 Example Folder Structure

```
/opt/
 ├── scripts/
 │    └── jenkins_log_analyzer.py
 ├── reports/
 │    └── jenkins_failure_summary_2025-11-05.txt
 ├── logs/
 │    └── analyzer.log
```

---

## 🧠 Key Benefits

* Automates daily Jenkins log analysis
* Detects recurring CI/CD pipeline issues instantly
* Reduces manual investigation time drastically
* Supports Slack/email integration
* Helps track and fix root causes faster

---

**Author:** *Rupesh Kotal*
**Category:** *DevOps Automation Scripts (Jenkins / Python)*

```

---

Would you like me to make **Automation #3** next (so we have #1–#4 as a complete “DevOps Automation Scripts” collection)?  
I can also merge them into a **single repository-level README.md** with an index (like `Automation #1 – Log Rotation`, `#2 – EC2 Snapshot Backup`, etc.) for your GitHub portfolio.
```
