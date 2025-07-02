# 📬 GitHub Webhook Receiver – `webhook-repo`

This repository contains the backend webhook listener for GitHub events triggered from [`action-repo`](https://github.com/IshaGupta2010/action-repo).

It receives GitHub Webhook POST requests and logs the activity (pushes, pull requests, merges) into a MongoDB collection.

## 🛠 Tech Stack

- **Flask (Python)** – REST API to handle webhook
- **MongoDB** – Stores structured event data
- **Ngrok** – Exposes local Flask server for GitHub to access
- **Webhook Events** – Handles: `push`, `pull_request`, `merge` (via PR closed with merged status)

---

## 📦 Endpoints

| Method | Endpoint     | Description                   |
|--------|--------------|-------------------------------|
| POST   | `/webhook`   | Receives GitHub Webhook       |
| GET    | `/`          | Simple health check endpoint  |

---

## 💡 Example Entry in MongoDB

```json
{
  "request_id": "abc123def456",
  "author": "IshaGupta2010",
  "action": "MERGE",
  "from_branch": "feature-xyz",
  "to_branch": "main",
  "timestamp": "02 July 2025 - 09:34 AM UTC"
}

🚀 How to Use
Clone this repo

Install dependencies:

bash
Copy
Edit
pip install flask pymongo
Run the server:

bash
Copy
Edit
python app.py
Expose it with ngrok:

bash
Copy
Edit
ngrok http 5000
Set GitHub Webhook URL as:

arduino
Copy
Edit
https://<your-ngrok-subdomain>.ngrok-free.app/webhook
🔗 Related Repositories
Frontend UI – webhook-ui

Trigger Events – action-repo
