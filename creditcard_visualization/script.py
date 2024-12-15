import os
import sys
import pandas as pd
from datetime import datetime
from calendar import monthrange

# ========================== Helper Functions ==========================

def load_input_data(input_file):
    """Load the input file and validate its existence."""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")
    print(f"Loading input file: {input_file}")
    return pd.read_csv(input_file)

def validate_columns(df, required_columns):
    """Check if required columns are present in the input file."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

def add_default_fields(input_data):
    """Add default fields to the input data."""
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
        'STATUS': 'A',
        'ACC_DATE': datetime(today.year, today.month, last_day).strftime('%Y-%m-%d')
    }
    
    for key, value in default_fields.items():
        input_data[key] = value

    input_data['FI_SUBJECT_CODE'] = 'C0000000' + input_data['CLIENT ID'].astype(str)
    input_data['ROWID'] = range(1, len(input_data) + 1)
    input_data['ADDRESS_DISTRICT'] = input_data['REGION']
    
    return input_data

def save_to_personal(new_data, personal_output_file):
    """Save personal data to a CSV file."""
    if not new_data.empty:
        new_data.to_csv(personal_output_file, mode='w', index=False)
        print(f"Added {len(new_data)} rows to {personal_output_file}.")
    else:
        print(f"No data to save to {personal_output_file}.")

def process_financial_data(input_data, financial_output_file):
    """Process and save financial data."""
    df_financial = input_data.copy()
    df_financial['F_I_SUBJECT_CODE'] = 'C0000000' + df_financial['CLIENT ID'].astype(str)
    df_financial['CREDIT_LIMIT'] = df_financial['CREDIT LIMIT [BDT]'] + (df_financial['CREDIT LIMIT [USD]'] * 125)
    df_financial['TOTAL_OUTSTANDING'] = df_financial['OUTSTANDING [BDT]'] + (df_financial['OUTSTANDING [USD]'] * 120)
    df_financial.to_csv(financial_output_file, index=False)
    print(f"Financial data saved to {financial_output_file}.")

# ========================== Main Script ==========================

def main(input_file, personal_output_file, processed_ids_file, financial_output_file):
    try:
        print("Starting script...")

        # Load input file
        input_data = load_input_data(input_file)

        # Validate required columns
        required_columns = ['CLIENT ID', 'ZIP CODE', 'REGION']
        validate_columns(input_data, required_columns)

        # Add default fields and process data
        input_data = add_default_fields(input_data)

        # Save personal data
        save_to_personal(input_data, personal_output_file)

        # Save processed IDs (mock logic for now)
        processed_ids = input_data[['FI_SUBJECT_CODE']].drop_duplicates()
        processed_ids.to_csv(processed_ids_file, index=False)
        print(f"Processed IDs saved to {processed_ids_file}.")

        # Save financial data
        process_financial_data(input_data, financial_output_file)

        print("Script completed successfully.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <input_file> <personal_output_file> <processed_ids_file> <financial_output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    personal_output_file = sys.argv[2]
    processed_ids_file = sys.argv[3]
    financial_output_file = sys.argv[4]

    main(input_file, personal_output_file, processed_ids_file, financial_output_file)
