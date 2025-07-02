from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://Isha_ngrok:FGNdKDi2K0D91biA@cluster0.pef31ur.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['webhook_db']
collection = db['github_events']

@app.route("/", methods=["GET"])
def home():
    return "Webhook Server Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    if not payload:
        return jsonify({"error": "Invalid payload"}), 400

    try:
        # Common values
        timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
        author = payload['sender']['login']
        request_id = payload['after'] if event_type == 'push' else payload.get('pull_request', {}).get('id', 'NA')

        # Initialize fields
        from_branch = to_branch = None
        action_type = None

        if event_type == 'push':
            from_branch = payload['ref'].split('/')[-1]
            to_branch = from_branch
            action_type = 'PUSH'

        elif event_type == 'pull_request' and payload.get('action') == 'closed' and payload['pull_request'].get('merged'):
            # This is a merged pull request
            from_branch = payload['pull_request']['head']['ref']
            to_branch = payload['pull_request']['base']['ref']
            action_type = 'MERGE'

        elif event_type == 'pull_request':
            from_branch = payload['pull_request']['head']['ref']
            to_branch = payload['pull_request']['base']['ref']
            action_type = 'PULL_REQUEST'

        else:
            return jsonify({"message": f"Ignored event: {event_type}"}), 200

        doc = {
            "request_id": request_id,
            "author": author,
            "action": action_type,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

        collection.insert_one(doc)
        return jsonify({"message": f"{action_type} event processed successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
