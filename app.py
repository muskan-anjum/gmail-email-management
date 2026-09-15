from flask import Flask, jsonify
import sqlite3


app = Flask(__name__)

DATABASE_NAME = "emails.db"


def get_emails_from_database():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            sender_name,
            sender_email,
            subject,
            date_time,
            email_body,
            status
        FROM emails
        ORDER BY id DESC
    """)

    emails = cursor.fetchall()
    connection.close()

    return [dict(email) for email in emails]


@app.route("/")
def home():
    emails = get_emails_from_database()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gmail Email Management System</title>
    </head>

    <body>
        <h1>Gmail Email Management System</h1>
        <h2>Fetched Emails</h2>
    """

    for email in emails:
        html += f"""
        <hr>
        <p><b>Sender Name:</b> {email['sender_name']}</p>
        <p><b>Sender Email:</b> {email['sender_email']}</p>
        <p><b>Subject:</b> {email['subject']}</p>
        <p><b>Date/Time:</b> {email['date_time']}</p>
        <p><b>Status:</b> {email['status']}</p>
        <p><b>Email Body:</b> {email['email_body'][:500]}</p>
        """

    html += """
    </body>
    </html>
    """

    return html


@app.route("/api/emails")
def api_emails():
    emails = get_emails_from_database()
    return jsonify(emails)


if __name__ == "__main__":
    app.run(debug=True)