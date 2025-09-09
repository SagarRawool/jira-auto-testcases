from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

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

@app.route("/webhook", methods=["POST"])
def jira_webhook():
    """Receive Jira webhook payload"""
    data = request.json
    issue_key = data["client_payload"]["issueKey"]

    # Fetch issue details from Jira
    issue = jira.issue(issue_key)
    description = issue.fields.description or "No description provided."

    # Generate test cases
    test_cases = generate_test_cases(description)

    # Add test cases as comment in Jira
    jira.add_comment(issue, f"🤖 AI-Generated Test Cases:\n\n{test_cases}")

    print(f"✅ Added test cases to {issue.key}")
    return jsonify({"status": "success", "issue": issue_key}), 200

if __name__ == "__main__":
    # Run Flask app on port 5000
    app.run(host="0.0.0.0", port=5000)
