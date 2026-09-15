import sqlite3


DATABASE_NAME = "emails.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gmail_message_id TEXT UNIQUE,
            sender_name TEXT,
            sender_email TEXT,
            subject TEXT,
            date_time TEXT,
            email_body TEXT,
            status TEXT
        )
    """)

    connection.commit()
    connection.close()

    print("Database and emails table created successfully!")
def save_email(
    gmail_message_id,
    sender_name,
    sender_email,
    subject,
    date_time,
    email_body,
    status
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO emails (
            gmail_message_id,
            sender_name,
            sender_email,
            subject,
            date_time,
            email_body,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        gmail_message_id,
        sender_name,
        sender_email,
        subject,
        date_time,
        email_body,
        status
    ))

    connection.commit()
    connection.close()
if __name__ == "__main__":
    create_database()
