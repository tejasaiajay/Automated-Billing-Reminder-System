import os
import base64
import pandas as pd

from datetime import date, timedelta
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from customer_checker import check_customer_due
from config import (
    EXCEL_FILE,
    CREDENTIALS_FILE,
    TOKEN_FILE,
    EMAIL_SUBJECT,
    CUSTOMER_NAME_COLUMN,
    CUSTOMER_EMAIL_COLUMN,
    DUE_DATE_COLUMN,
    SCOPES,
    DUE_DAYS_BEFORE
)


def get_gmail_service():

    credentials = None

    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials or not credentials.valid:

        if not os.path.exists(CREDENTIALS_FILE):
            print("ERROR: credentials.json was not found.")
            return None

        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE,
            SCOPES
        )

        credentials = flow.run_local_server(
            port=0,
            access_type="offline",
            prompt="consent"
        )

        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    return build(
        "gmail",
        "v1",
        credentials=credentials
    )


def send_email(
    service,
    customer_name,
    customer_email,
    current_bill,
    wifi_bill,
    water_bill,
    mobile_bill,
    gas_bill,
    due_date
):

    email = EmailMessage()

    email["To"] = customer_email
    email["Subject"] = EMAIL_SUBJECT

    email_body = f"""
Hello {customer_name},

This is a friendly reminder that your upcoming bills are due on {due_date}.

Bill Details:

Current Bill: ${current_bill:.2f}
WiFi Bill: ${wifi_bill:.2f}
Water Bill: ${water_bill:.2f}
Mobile Bill: ${mobile_bill:.2f}
Gas Bill: ${gas_bill:.2f}

Please ensure payment is submitted on time.

Best regards,
Finance Department
"""

    email.set_content(email_body)

    encoded_email = base64.urlsafe_b64encode(
        email.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": encoded_email}
    ).execute()

    print("Email sent successfully to:", customer_email)


# Check Excel file

if not os.path.exists(EXCEL_FILE):

    print("ERROR: Excel file was not found.")
    print("Expected file:", EXCEL_FILE)

    raise SystemExit


# Read Excel

data = pd.read_excel(EXCEL_FILE)

print("Excel file read successfully.")


# Check required columns

required_columns = [
    CUSTOMER_NAME_COLUMN,
    CUSTOMER_EMAIL_COLUMN,
    DUE_DATE_COLUMN,
    "Current Bill",
    "Wifi Bill",
    "Water Bill",
    "Mobile Bill",
    "Gas Bill"
]

missing_columns = [
    column
    for column in required_columns
    if column not in data.columns
]

if missing_columns:

    print("ERROR: Missing Excel columns:")
    print(", ".join(missing_columns))

    raise SystemExit


# Convert Due Date

data[DUE_DATE_COLUMN] = pd.to_datetime(
    data[DUE_DATE_COLUMN]
).dt.date


# Calculate target date

today = date.today()

target_date = today + timedelta(days=2)

print("Today's date:", today)
print("Checking bills due on:", target_date)


# Connect to Gmail

print("Connecting to Gmail...")

gmail_service = get_gmail_service()

if gmail_service is None:
    raise SystemExit

print("Gmail connected successfully.")


# Check every customer

email_sent = False

for index, row in data.iterrows():

    customer_name = row[CUSTOMER_NAME_COLUMN]
    customer_email = row[CUSTOMER_EMAIL_COLUMN]

    current_bill = float(row["Current Bill"])
    wifi_bill = float(row["Wifi Bill"])
    water_bill = float(row["Water Bill"])
    mobile_bill = float(row["Mobile Bill"])
    gas_bill = float(row["Gas Bill"])

    due_date = row[DUE_DATE_COLUMN]

    if check_customer_due(row, target_date):

        print("Bill found for:", customer_name)

        send_email(
            gmail_service,
            str(customer_name),
            str(customer_email),
            current_bill,
            wifi_bill,
            water_bill,
            mobile_bill,
            gas_bill,
            due_date
        )

        email_sent = True


if not email_sent:

    print(
        "No bills are due exactly 2 days from today."
    )


print("Program finished.")