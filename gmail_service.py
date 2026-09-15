import os
import base64
import re
import html
from email.utils import parseaddr
from database import create_database, save_email

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service
def clean_html(html_text):
    from html import unescape
    import re

    if not html_text:
        return ""

    text = re.sub(
        r"<script.*?</script>",
        "",
        html_text,
        flags=re.DOTALL | re.IGNORECASE
    )

    text = re.sub(
        r"<style.*?</style>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p\s*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)

    text = unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)

    return text.strip()
def get_email_body(payload):
    def decode_data(data):
        if not data:
            return ""

        try:
            return base64.urlsafe_b64decode(data).decode(
                "utf-8",
                errors="ignore"
            )
        except Exception:
            return ""

    def find_mime_type(part, wanted_type):
        # Check this part
        if part.get("mimeType") == wanted_type:
            data = part.get("body", {}).get("data")

            if data:
                decoded = decode_data(data)

                if decoded:
                    return decoded

        # Check all child/nested parts
        for child in part.get("parts", []):
            result = find_mime_type(child, wanted_type)

            if result:
                return result

        return ""

    # FIRST: Search the entire email for HTML
    html_body = find_mime_type(payload, "text/html")

    if html_body:
        return clean_html(html_body)

    # SECOND: If no HTML exists, use plain text
    plain_body = find_mime_type(payload, "text/plain")

    if plain_body:
        return plain_body

    # LAST: Check direct body
    direct_data = payload.get("body", {}).get("data")

    if direct_data:
        return decode_data(direct_data)

    return ""
def fetch_emails(service):
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        print("No emails found.")
        return

    print("\nLatest Inbox Emails:\n")

    for message in messages:
        msg = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full",
        ).execute()

        headers = msg["payload"]["headers"]
        body = get_email_body(msg["payload"])

        sender = ""
        subject = ""
        date = ""
        sender_name = ""
        sender_email = ""

        for header in headers:
            if header["name"] == "From":
                sender = header["value"]
                sender_name, sender_email = parseaddr(sender)
            elif header["name"] == "Subject":
                subject = header["value"]
            elif header["name"] == "Date":
                date = header["value"]

        if "UNREAD" in msg.get("labelIds", []):
            status = "Unread"
        else:
            status = "Read"

        print("Sender Name:", sender_name)
        print("Sender Email:", sender_email)
        print("Subject:", subject)
        print("Date:", date)
        print("Email Body:", body[:500])
        print("Status:", status)
        save_email(
    message["id"],
    sender_name,
    sender_email,
    subject,
    date,
    body,
    status
)
        print("-" * 50)


if __name__ == "__main__":
    create_database()
    service = get_gmail_service()

    profile = service.users().getProfile(
        userId="me"
    ).execute()

    print("Gmail connected successfully!")
    print("Email:", profile["emailAddress"])
    print("Total messages:", profile["messagesTotal"])

    fetch_emails(service)