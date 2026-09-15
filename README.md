# Gmail Email Management System

A Python-based email management system that securely connects to Gmail using the Gmail API and OAuth 2.0.

## Features

- Secure Gmail authentication using OAuth 2.0
- Fetches incoming emails using Gmail API
- Extracts sender name and sender email
- Extracts subject and date/time
- Extracts and cleans email body
- Identifies read/unread status
- Stores email information in SQLite database
- Provides a basic Flask dashboard
- Provides an API endpoint to view stored emails

## Technologies Used

- Python
- Flask
- Gmail API
- Google OAuth 2.0
- SQLite
- Git and GitHub

## Security

Sensitive files such as `credentials.json`, `token.json`, and the local database are excluded from GitHub using `.gitignore`.

## Run the Project

Install the required Python packages and run:

python app.py

Then open:

http://127.0.0.1:5000

API endpoint:

http://127.0.0.1:5000/api/emails
