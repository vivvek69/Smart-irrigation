import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Define the scope for Google Sheets and Drive API
SCOPES = ['https://docs.google.com/spreadsheets/d/1c1g8smnbeW4z6eOuDknD1wJqHHRCOCbkc3UBtg3KAxU/edit?gid=0#gid=0', 'https://www.googleapis.com/auth/drive']

# Load the service account credentials
credentials = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)

# Authenticate with Google Sheets
gc = gspread.authorize(credentials)

# Define the name of the Google Sheet
spreadsheet_name = "Irrigation Dataset"

# Check if the spreadsheet already exists, otherwise create it
try:
    sh = gc.open(spreadsheet_name)
    print(f"Spreadsheet '{spreadsheet_name}' already exists.")
except gspread.exceptions.SpreadsheetNotFound:
    # Create a new Google Sheet
    sh = gc.create(spreadsheet_name)
    print(f"Spreadsheet '{spreadsheet_name}' created.")

# Share the sheet with your email (optional)
# Replace 'your-email@gmail.com' with your Google account email
sh.share('your-email@gmail.com', perm_type='user', role='writer')

# Select the first sheet
worksheet = sh.sheet1

# Load the dataset
df = pd.read_csv('data/irrigation_dataset.csv')

# Clear the existing sheet content (if any)
worksheet.clear()

# Write the dataset to Google Sheets
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print(f"Dataset uploaded to Google Sheet: {spreadsheet_name}")
