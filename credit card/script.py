import os
import pandas as pd
import numpy as np
from datetime import datetime
from calendar import monthrange

# ========================== File Paths ==========================
input_file = "input.csv"
personal_output_file = "personal.csv"
temp_personal_file = "temp_personal.csv"
financial_output_file = "financial.csv"

# ========================== Load Input Data ==========================
# Check if input file exists
if not os.path.exists(input_file):
    raise FileNotFoundError(f"Input file '{input_file}' does not exist.")

# Load input CSV
input_data = pd.read_csv(input_file)

# ========================== Personal Data Processing ==========================
# Column mapping from input to output
columns_mapping = {
    'TITLE': 'CUST_TITLE',
    'CUSTOMER NAME': 'CUST_NAME',
    "FATHER'S NAME": 'FATHER_NAME',
    "MOTHER'S NAME": 'MOTHER_NAME',
    'SPOUSE NAME': 'SPOUSE_NAME',
    'SECTOR CODE': 'SECTOR_CODE',
    'SEX': 'GENDER',
    'DATE OF BIRTH': 'DATE_OF_BIRTH',
    'PLACE OF BIRTH': 'PLACE_BIRTH_DIST',
    'NATIONAL ID': 'NATIONAL_ID_NUMBER',
    'TIN': 'TIN',
    'REG ADDRESS': 'ADDRESS_STREET_NO',
    'ZIP CODE': 'ADDRESS_POSTAL_CODE',
    'REGION': 'ADDRESS_DISTRICT',
    'RES ADDRESS': 'ADD_ADDRESS_STREET_NO',
    'CONTRACT ADDRESS': 'BUS_ADDRESS_STREET_NO',
    'ZIP CODE': 'ADD_ADDRESS_POSTAL_CODE',
    'REGION': 'ADD_ADDRESS_DISTRICT',
}

# Add additional fields and default values
input_data['BUS_ADDRESS_POSTAL_CODE'] = input_data['ZIP CODE']
input_data['BUS_ADDRESS_DISTRICT'] = input_data['REGION']
input_data['RECORD_TP'] = 'TP'
input_data['FI_CODE'] = 'FI120'
input_data['BRANCH_CODE'] = '1101'
input_data['FATHER_TITLE'] = None
input_data['MOTHER_TITLE'] = None
input_data['SPOUSE_TITLE'] = None
input_data['SECTOR_TP'] = 9
input_data['COUNTRY_BIRTH_CODE'] = 'BD'
input_data['NATIONAL_ID_FLAG'] = 1
input_data['ADD_ADDRESS_COUNTRY_CODE'] = 'BD'
input_data['ADDRESS_COUNTRY_CODE'] = 'BD'
input_data['DOC_TP'] = None
input_data['DOC_NO'] = None
input_data['DOC_ISSUE_DATE'] = None
input_data['DOC_ISSUE_COUNTRY_CODE'] = None
input_data['PHONE_NO'] = None
input_data['MAKE_BY'] = None
input_data['MAKE_DT'] = None
input_data['AUTH_BY'] = None
input_data['AUTH_DT'] = None
input_data['CUST_ID'] = None
input_data['BUS_ADDRESS_COUNTRY_CODE'] = 'BD'
input_data['STATUS'] = 'A'

# Calculate last day of the current month
today = datetime.today()
last_day = monthrange(today.year, today.month)[1]
input_data['ACC_DATE'] = datetime(today.year, today.month, last_day).strftime('%Y-%m-%d')

# Generate FI_SUBJECT_CODE
input_data['FI_SUBJECT_CODE'] = 'C0000000' + input_data['CLIENT ID'].astype(str)
input_data['ROWID'] = range(1, len(input_data) + 1)
input_data['ADDRESS_DISTRICT'] = input_data['REGION']

# Rename columns based on mapping
df_renamed = input_data.rename(columns=columns_mapping)

# Ensure postal codes are present
df_renamed['ADDRESS_POSTAL_CODE'] = input_data['ZIP CODE']
df_renamed['ADD_ADDRESS_POSTAL_CODE'] = input_data['ZIP CODE']

# Select required columns
required_columns = [
    'ROWID', 'RECORD_TP', 'FI_CODE', 'BRANCH_CODE', 'FI_SUBJECT_CODE',
    'CUST_TITLE', 'CUST_NAME',
    'FATHER_TITLE', 'FATHER_NAME',
    'MOTHER_TITLE', 'MOTHER_NAME',
    'SPOUSE_TITLE', 'SPOUSE_NAME',
    'SECTOR_TP', 'COUNTRY_BIRTH_CODE', 'NATIONAL_ID_FLAG', 'ADDRESS_COUNTRY_CODE',
    'ADD_ADDRESS_COUNTRY_CODE', 'BUS_ADDRESS_POSTAL_CODE', 'BUS_ADDRESS_DISTRICT',
    'BUS_ADDRESS_COUNTRY_CODE', 'ACC_DATE', 'DOC_TP', 'DOC_NO', 'DOC_ISSUE_DATE',
    'DOC_ISSUE_COUNTRY_CODE', 'PHONE_NO', 'MAKE_BY', 'MAKE_DT', 'AUTH_BY', 'AUTH_DT',
    'STATUS', 'CUST_ID', 'ADDRESS_POSTAL_CODE', 'ADD_ADDRESS_POSTAL_CODE'
]

df_renamed = df_renamed[required_columns]

# ========================== Handle Existing Data in personal.csv ==========================

# Check if the personal_output_file exists and load it
if os.path.exists(personal_output_file):
    # Load existing personal data
    existing_personal_data = pd.read_csv(personal_output_file)
    # Extract existing FI_SUBJECT_CODE values from the previous file
    existing_fi_codes = existing_personal_data['FI_SUBJECT_CODE'].unique()
    
    # Filter the input data to only include new rows (those not already in personal.csv)
    new_data = df_renamed[~df_renamed['FI_SUBJECT_CODE'].isin(existing_fi_codes)]
else:
    # If personal.csv doesn't exist, treat all rows as new
    new_data = df_renamed

# ========================== Save New Data to personal.csv ==========================
# If there are new rows, overwrite personal.csv with only those
if not new_data.empty:
    new_data.to_csv(personal_output_file, mode='w', index=False)
else:
    print("No new rows to add to personal.csv.")

# ========================== Financial Data Processing ==========================

# Add financial data fields
df_financial = input_data.copy()
df_financial['F_I_SUBJECT_CODE'] = 'C0000000' + df_financial['CLIENT ID'].astype(str)
df_financial['F_I_CONTRACT_CODE'] = df_financial['CONTRACT NO'].str[4:]
df_financial['DATE_OF_CLASSIFICATION'] = df_financial['CLASSIFICATION DATE']
df_financial['RECORD_TYPE'] = 'D'
df_financial['F_I_CODE'] = '085'
df_financial['BRANCH_CODE'] = '1000'
df_financial['CONTRACT_TYPE'] = 'CR'
df_financial['CONTRACT_PHASE'] = 'LV'
df_financial['CONTRACT_STATUS'] = 'B'
df_financial['CURRENCY_CODE'] = 'BDT'
df_financial['PERIODICITY_PAYMENT'] = 'M'
df_financial['ECONOMIC_PURPOSE_CODE'] = 9830

# Financial calculations
df_financial['CREDIT_LIMIT'] = df_financial['CREDIT LIMIT [BDT]'] + (df_financial['CREDIT LIMIT [USD]'] * 125)
df_financial['OD_NOT_PAID_AMOUNT'] = df_financial['OVERDUE AMT [BDT]'] + (df_financial['OVERDUE AMT [USD]'] * 120)
df_financial['TOTAL_OUTSTANDING'] = (
    df_financial['OUTSTANDING [BDT]'] +
    (df_financial['OUTSTANDING [USD]'] * 120) +
    df_financial['UNPAID EMI [BDT]']
)
df_financial['DEFAULTER_FLAG'] = df_financial['DELIQ CLASS'].apply(lambda x: 'Y' if x == 'classified' else 'N')

# Export financial data
df_financial.to_csv(financial_output_file, index=False)
print(f"Financial data exported to '{financial_output_file}'.")
