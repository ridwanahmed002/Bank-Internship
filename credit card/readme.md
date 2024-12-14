---

# Personal Data Processing Script

Automate the processing of customer data efficiently with this Python script. It manages both personal and financial information, ensuring that output files contain only unique customer entries. This prevents data duplication and maintains data integrity across multiple runs.

## **Features**

- **Duplicate Prevention**: Ensures each `FI_SUBJECT_CODE` is processed only once to avoid duplication.
- **Automated Data Processing**: Handles all necessary computations and transformations for personal and financial data.
- **Clear Output Management**: Generates two well-structured files, `personal.csv` and `financial.csv`, based on the latest input data.
- **Processed IDs Tracking**: Records processed `FI_SUBJECT_CODE`s in `processed_ids.csv` to facilitate accurate data filtering in future runs.

## **How It Works**

1. **Load Input Data**
    - The script reads customer data from `input.csv`.
    - It verifies the existence of the input file before proceeding.

2. **Personal Data Processing**
    - **Column Mapping**: Renames columns according to established standards for consistency.
    - **Default Fields Addition**: Adds necessary default fields with predefined values.
    - **Unique Identifier Generation**: Uses the `CLIENT ID` to create a unique `FI_SUBJECT_CODE` for each client.
    - **Filtering New Entries**: Compares `FI_SUBJECT_CODE`s against those in `processed_ids.csv` to identify new, unprocessed entries.
    - **Output Management**:
        - **`personal.csv`**: Overwrites with only the new unique entries from the current run.
        - **`processed_ids.csv`**: Updates with the newly processed `FI_SUBJECT_CODE`s to prevent future duplication.

3. **Financial Data Processing**
    - Transforms and extracts financial information from the input data.
    - Performs calculations such as `CREDIT_LIMIT`, `OD_NOT_PAID_AMOUNT`, `TOTAL_OUTSTANDING`, and determines the `DEFAULTER_FLAG` based on delinquency classification.
    - Exports the processed financial data to `financial.csv`.

## **Files**

- **`input.csv`**: The source file containing raw customer data.
- **`personal.csv`**: Outputs the latest unique customer entries after each run.
- **`processed_ids.csv`**: Logs all processed `FI_SUBJECT_CODE`s to ensure each is handled only once.
- **`financial.csv`**: Contains processed financial data derived from the input.

## **Requirements**

- **Python 3.x**
- **Pandas Library**

## **Installation**

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ridwanahmed002/Bank-Internship/tree/b63c05dfc99cbaa7402fd4ce9d9f1702f9a8c500/credit%20card
    ```

2. **Navigate to the Directory**:
    ```bash
    cd personal-data-processing
    ```

3. **Install Dependencies**:
    ```bash
    pip install pandas
    ```

## **Usage**

1. **Prepare the `input.csv` File**:
    - Ensure your `input.csv` includes necessary columns such as `CLIENT ID`, `CONTRACT NO`, `CLASSIFICATION DATE`, and other relevant personal and financial fields.

2. **Run the Script**:
    ```bash
    python data_processing.py
    ```
    - Replace `data_processing.py` with the actual name of your script file.

3. **Script Execution Flow**:
    - **First Run**:
        - Processes all entries from `input.csv`.
        - Creates `personal.csv` with these entries.
        - Logs the corresponding `FI_SUBJECT_CODE`s in `processed_ids.csv`.
    - **Subsequent Runs**:
        - Only new entries with unique `FI_SUBJECT_CODE`s are added to `personal.csv`.
        - Updates `processed_ids.csv` with the new `FI_SUBJECT_CODE`s.
        - If no new entries are found, `personal.csv` is cleared.

## **Example Outputs**

### **personal.csv**
```csv
ROWID,RECORD_TP,FI_CODE,BRANCH_CODE,FI_SUBJECT_CODE,CUST_TITLE,CUST_NAME,FATHER_TITLE,FATHER_NAME,MOTHER_TITLE,MOTHER_NAME,SPOUSE_TITLE,SPOUSE_NAME,SECTOR_TP,COUNTRY_BIRTH_CODE,NATIONAL_ID_FLAG,ADDRESS_COUNTRY_CODE,ADD_ADDRESS_COUNTRY_CODE,BUS_ADDRESS_POSTAL_CODE,BUS_ADDRESS_DISTRICT,BUS_ADDRESS_COUNTRY_CODE,ACC_DATE,DOC_TP,DOC_NO,DOC_ISSUE_DATE,DOC_ISSUE_COUNTRY_CODE,PHONE_NO,MAKE_BY,MAKE_DT,AUTH_BY,AUTH_DT,STATUS,CUST_ID,ADDRESS_POSTAL_CODE,ADD_ADDRESS_POSTAL_CODE
1,TP,FI120,1101,C00000001,Mr.,John Doe,,,,,,9,BD,1,BD,BD,BD,1101,2024-12-31,,,,,,,,A,,12345,12345
2,TP,FI120,1101,C00000002,Ms.,Jane Smith,,,,,,9,BD,1,BD,BD,BD,1101,2024-12-31,,,,,,,,A,,67890,67890
```

### **processed_ids.csv**
```csv
FI_SUBJECT_CODE
C00000001
C00000002
```

### **financial.csv**
```csv
CLIENT ID,F_I_SUBJECT_CODE,F_I_CONTRACT_CODE,DATE_OF_CLASSIFICATION,RECORD_TYPE,F_I_CODE,BRANCH_CODE,CONTRACT_TYPE,CONTRACT_PHASE,CONTRACT_STATUS,CURRENCY_CODE,PERIODICITY_PAYMENT,ECONOMIC_PURPOSE_CODE,CREDIT_LIMIT,OD_NOT_PAID_AMOUNT,TOTAL_OUTSTANDING,DEFAULTER_FLAG
123,C00000001,0001,2024-01-15,D,085,1000,CR,LV,B,BDT,M,9830,125000,120000,245000,Y
456,C00000002,0002,2024-02-20,D,085,1000,CR,LV,B,BDT,M,9830,250000,240000,490000,N
```

## **License**

This project is licensed under the [MIT License](LICENSE).

---
