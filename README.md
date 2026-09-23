# Automated Billing Reminder System

A simple Python project that reads customer billing information from an Excel file and sends an email reminder when a customer's bill is due in two days.

## Technologies Used

- Python
- Pandas
- Excel
- Gmail API
- Google OAuth

## Features

- Reads billing information from Excel
- Checks the current date
- Finds bills due in exactly two days
- Sends an automatic email reminder
- Uses Gmail API for sending emails
- Uses Google OAuth instead of storing a Gmail password

## Excel Columns

The Excel file contains:

- Customer Name
- Customer Email
- Amount Due
- Due Date

## How It Works

1. Python reads the Excel file.
2. The program gets today's date.
3. It calculates the date after two days.
4. It checks each customer's due date.
5. If the due date matches, an email reminder is created.
6. The reminder is sent through the Gmail API.

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt