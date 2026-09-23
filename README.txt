BILLING REMINDER - GMAIL LOGIN (NO GMAIL PASSWORD IN PYTHON)
===============================================================

This version does NOT ask you to put your Gmail password in the Python code.

It uses Google's official Gmail API login.
The first time you run it, a Google sign-in page will open in your browser.
You sign in normally to Gmail and give the program permission to SEND email.

FILES
-----
billing_reminder.py
billing_data.xlsx
requirements.txt
README.txt

IMPORTANT
---------
You still need ONE file from Google:
    credentials.json

Put credentials.json in this same folder.

SIMPLE SETUP
------------

1. Install the Python packages:

   py -m pip install -r requirements.txt


2. Create Google OAuth credentials:

   Open Google Cloud Console:
   https://console.cloud.google.com/

   Create/select a project.

   Enable:
   Gmail API

   Then go to:
   APIs & Services -> Credentials

   Create Credentials -> OAuth client ID

   If Google asks for the OAuth consent screen, complete it.

   Choose application type:
   Desktop app

   Download the JSON file.

   Rename it to:
   credentials.json

   Put it beside billing_reminder.py.


3. OPEN billing_data.xlsx

   Replace YOUR_GMAIL@gmail.com with YOUR OWN Gmail address.

   For the first test, use your own Gmail address for every row.
   Do not use real customers yet.


4. Run:

   py billing_reminder.py


5. A Google sign-in page should open.

   Sign in to the Gmail account that should send the reminders.

   Approve the Gmail permission.

   IMPORTANT:
   Your Gmail password is entered ONLY on Google's website.
   It is NOT written in billing_reminder.py.


6. After successful login, token.json will be created automatically.

   Do NOT share credentials.json or token.json with anyone.


DATE LOGIC
----------
The program checks:

    target date = today's date + 2 days

Only rows whose Due Date is exactly that date receive an email.

For example, if today is 2026-09-21:
    2026-09-21       -> ignored
    2026-09-22 -> ignored
    2026-09-23 -> EMAIL SENT
    2026-09-28 -> ignored


EMAIL
-----
Subject:
Urgent Reminder: Invoice Payment Due in 2 Days

The Excel Customer Name, Customer Email, Amount Due and Due Date
are used in the email.

NO PASSWORD
-----------
There is no SENDER_PASSWORD in the Python code.

Google OAuth is used instead.
