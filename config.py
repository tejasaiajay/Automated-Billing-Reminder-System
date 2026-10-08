EXCEL_FILE = "PersonsBillingDetails.xlsx"

CREDENTIALS_FILE = "credentials.json"

TOKEN_FILE = "gmail_token.json"

EMAIL_SUBJECT = "Urgent Reminder: Invoice Payment Due in 2 Days"

CUSTOMER_NAME_COLUMN = "Customer Name"

CUSTOMER_EMAIL_COLUMN = "Customer Email"

DUE_DATE_COLUMN = "Due Date"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]

DUE_DAYS_BEFORE = 2