import os
import pandas as pd
from datetime import date, timedelta
from email.message import EmailMessage
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# Gmail permission
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
# File names
excel_file = "billing_data.xlsx"
credentials_file = "credentials.json"
token_file = "gmail_token.json"
# STEP 1: Check Excel file
if not os.path.exists(excel_file):
    print("billing_data.xlsx file not found.")
    exit()
# Read Excel file
data = pd.read_excel(excel_file)
print("Excel file read successfully.")
# STEP 2: Get today's date
today = date.today()
target_date = today + timedelta(days=2)
print("Today's date:", today)
print("Checking bills due on:", target_date)
# STEP 3: Convert Excel date
data["Due Date"] = pd.to_datetime(data["Due Date"]).dt.date
# STEP 4: Connect to Gmail
print("Connecting to Gmail...")
credentials = None
# Check if login token already exists
if os.path.exists(token_file):
    credentials = Credentials.from_authorized_user_file(token_file,SCOPES)
# If no login, ask Google for permission
if not credentials or not credentials.valid:
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file,SCOPES)
    credentials = flow.run_local_server(port=0)
    # Save login permission
    with open(token_file, "w") as file:
        file.write(credentials.to_json())
# Create Gmail connection
gmail = build("gmail","v1",credentials=credentials)
print("Gmail connected successfully.")
# STEP 5: Check every customer
for index, row in data.iterrows():
    customer_name = row["Customer Name"]
    customer_email = row["Customer Email"]
    amount = row["Amount Due"]
    due_date = row["Due Date"]
    # Send only if due date is exactly 2 days away
    if due_date == target_date:
        print("Bill found for:", customer_name)
        # Create email
        email = EmailMessage()
        email["To"] = customer_email
        email["Subject"] = ("Urgent Reminder: Invoice Payment Due in 2 Days")
        email_body = f"""Hello {customer_name},
This is a friendly reminder that your upcoming bill of ${amount:.2f} is due on {due_date}. Please ensure payment is submitted on time.
Best regards,
Finance Department"""
        email.set_content(email_body)
        # Convert email into Gmail format
        encoded_email = base64.urlsafe_b64encode(email.as_bytes()).decode()
        # Send email
        gmail.users().messages().send(
            userId="me",
            body={
                "raw": encoded_email
            }
        ).execute()
        print("Email sent successfully to:",customer_email)
print("Program finished.")