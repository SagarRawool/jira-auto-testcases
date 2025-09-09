import os
from jira import JIRA
from openai import OpenAI
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Connect to Jira
jira = JIRA(
    server=JIRA_URL,
    basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
)

# Connect to OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_test_cases(requirement: str) -> str:
    """Generate test cases from requirement using AI"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert QA engineer. Generate test cases in clear numbered format."},
            {"role": "user", "content": f"Requirement:\n{requirement}\n\nGenerate test cases."}
        ]
    )
    return response.choices[0].message.content

def process_jira_tickets():
    """Find Jira issues in QA Needed status and add test cases"""
    # Adjust JQL as per your workflow/status
    issues = jira.search_issues('status="QA Needed"')

    for issue in issues:
        print(f"🔎 Processing issue {issue.key}: {issue.fields.summary}")

        description = issue.fields.description or "No description provided."
        test_cases = generate_test_cases(description)

        # Add test cases as a comment in Jira
        jira.add_comment(issue, f"🤖 AI-Generated Test Cases:\n\n{test_cases}")
        print(f"✅ Added test cases to {issue.key}")

if __name__ == "__main__":
    process_jira_tickets()
