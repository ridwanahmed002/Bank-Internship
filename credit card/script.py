import os
import pandas as pd
from datetime import datetime
from calendar import monthrange

# ========================== File Paths ==========================
INPUT_FILE = "input.csv"
PERSONAL_OUTPUT_FILE = "personal.csv"
PROCESSED_IDS_FILE = "processed_ids.csv"
FINANCIAL_OUTPUT_FILE = "financial.csv"

# ========================== Helper Functions ==========================

def load_input_data(input_file):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")
    return pd.read_csv(input_file)

def load_processed_ids(processed_ids_file):
    if os.path.exists(processed_ids_file):
        try:
            processed_ids = pd.read_csv(processed_ids_file)
            return set(processed_ids['FI_SUBJECT_CODE'].unique())
        except pd.errors.EmptyDataError:
            return set()
    return set()

def add_default_fields(input_data):
    today = datetime.today()
    last_day = monthrange(today.year, today.month)[1]
    
    default_fields = {
        'BUS_ADDRESS_POSTAL_CODE': input_data['ZIP CODE'],
        'BUS_ADDRESS_DISTRICT': input_data['REGION'],
        'RECORD_TP': 'TP',
        'FI_CODE': 'FI120',
        'BRANCH_CODE': '1101',
        'FATHER_TITLE': None,
        'MOTHER_TITLE': None,
        'SPOUSE_TITLE': None,
        'SECTOR_TP': 9,
        'COUNTRY_BIRTH_CODE': 'BD',
        'NATIONAL_ID_FLAG': 1,
        'ADD_ADDRESS_COUNTRY_CODE': 'BD',
        'ADDRESS_COUNTRY_CODE': 'BD',
        'DOC_TP': None,
        'DOC_NO': None,
        'DOC_ISSUE_DATE': None,
        'DOC_ISSUE_COUNTRY_CODE': None,
        'PHONE_NO': None,
        'MAKE_BY': None,
        'MAKE_DT': None,
        'AUTH_BY': None,
        'AUTH_DT': None,
        'CUST_ID': None,
        'BUS_ADDRESS_COUNTRY_CODE': 'BD',
        'STATUS': 'A',
        'ACC_DATE': datetime(today.year, today.month, last_day).strftime('%Y-%m-%d')
    }
    
    for key, value in default_fields.items():
        input_data[key] = value

    input_data['FI_SUBJECT_CODE'] = 'C0000000' + input_data['CLIENT ID'].astype(str)
    input_data['ROWID'] = range(1, len(input_data) + 1)
    input_data['ADDRESS_DISTRICT'] = input_data['REGION']
    
    return input_data

def rename_columns(input_data):
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
        'REGION': 'ADD_ADDRESS_DISTRICT'
    }
    return input_data.rename(columns=columns_mapping)

def select_required_columns(df):
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
    return df[required_columns]

def save_to_personal(new_data, personal_output_file):
    if not new_data.empty:
        new_data.to_csv(personal_output_file, mode='w', index=False)
        print(f"Added {len(new_data)} new row(s) to {personal_output_file}.")
    else:
        if os.path.exists(personal_output_file):
            open(personal_output_file, 'w').close()
            print(f"No new rows to add. {personal_output_file} has been cleared.")
        else:
            print("No new rows to add and personal.csv does not exist.")

def update_processed_ids(new_fi_codes, processed_ids_file):
    if os.path.exists(processed_ids_file):
        new_fi_codes.to_csv(processed_ids_file, mode='a', header=False, index=False)
    else:
        new_fi_codes.to_csv(processed_ids_file, mode='w', index=False)
    print(f"Updated {processed_ids_file} with {len(new_fi_codes)} new FI_SUBJECT_CODE.")

def process_financial_data(input_data, financial_output_file):
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

    df_financial['CREDIT_LIMIT'] = df_financial['CREDIT LIMIT [BDT]'] + (df_financial['CREDIT LIMIT [USD]'] * 125)
    df_financial['OD_NOT_PAID_AMOUNT'] = df_financial['OVERDUE AMT [BDT]'] + (df_financial['OVERDUE AMT [USD]'] * 120)
    df_financial['TOTAL_OUTSTANDING'] = (
        df_financial['OUTSTANDING [BDT]'] +
        (df_financial['OUTSTANDING [USD]'] * 120) +
        df_financial['UNPAID EMI [BDT]']
    )
    df_financial['DEFAULTER_FLAG'] = df_financial['DELIQ CLASS'].apply(lambda x: 'Y' if x == 'classified' else 'N')

    df_financial.to_csv(financial_output_file, index=False)
    print(f"Financial data exported to '{financial_output_file}'.")

# ========================== Main Script ==========================

def main():
    input_data = load_input_data(INPUT_FILE)
    input_data = add_default_fields(input_data)
    df_renamed = rename_columns(input_data)
    df_renamed['ADDRESS_POSTAL_CODE'] = input_data['ZIP CODE']
    df_renamed['ADD_ADDRESS_POSTAL_CODE'] = input_data['ZIP CODE']
    df_selected = select_required_columns(df_renamed)

    existing_fi_codes = load_processed_ids(PROCESSED_IDS_FILE)
    new_data = df_selected[~df_selected['FI_SUBJECT_CODE'].isin(existing_fi_codes)]

    save_to_personal(new_data, PERSONAL_OUTPUT_FILE)

    if not new_data.empty:
        new_fi_codes = new_data[['FI_SUBJECT_CODE']]
        update_processed_ids(new_fi_codes, PROCESSED_IDS_FILE)

    process_financial_data(input_data, FINANCIAL_OUTPUT_FILE)

if __name__ == "__main__":
    main()
