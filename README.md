---

# Program for Handling Individual Records



By automating the processing of customer data, this Python script efficiently manages personal and financial information. The system ensures that the output files contain only unique customer entries, which prevents data duplication and maintains data integrity across runs.

## **When I am Available**

This function ensures that each 'FI_SUBJECT_CODE' is processed just once in order to prevent duplicates.
**Automated Data Processing** handles all the necessary computations and transformations for both personal and financial data.
The most current data is used to generate two well-structured files, "personal.csv" and "financial.csv," as part of the **Clear Output Management** process.
- **Recording Processed IDs**: Memorises processed 'FI_SUBJECT CODES' for usage in future runs' accurate data filtering.

## **How It Works**

1. Customer data is read from 'input.csv' by the script.
    The existence of the input file is verified before proceeding.

2. In **Personal Data Processing**, - **Column Mapping**: Renames columns according to established standards.
    Include mandatory default fields with predefined values by adding them as defaults.
    - **Unique Identifier Generation** uses the 'CLIENT ID,' to create a unique 'FI_SUBJECT_CODE' for each client.
    **Filtering New items** compares the 'FI_SUBJECT_CODE' with those in the 'processed_ids.csv' file to locate new, unprocessed items.
    All but the most recent unique items from this run are written into the **personal.csv** file.
        - **'processed_ids.csv'**: This file stores the freshly processed 'FI_SUBJECT_CODE's so they don't have to be processed again.

Financial data processing, the third step, entails transforming and extracting financial information from the input data.
    - Calculates 'CREDIT_LIMIT,' 'OD_NOT_PAID_AMOUNT,' and 'TOTAL_OUTSTANDING,' and decides the 'DEFAULTER_FLAG' based on the classification of delinquency.
    Data related to finances will be saved in the file "financial.csv" after optimisation.

Assembled materials

The **'input.csv'** file is the initial source file that holds the raw client data.
The most current unique customer records are written to **'personal.csv'** after every run.
By recording all of the 'FI_SUBJECT_CODE' values in the **'processed_ids.csv'** file, we can ensure that each value is processed only once.
The file named **'finance.csv'** contains processed financial data.

## **Required Items**

Python 3.x and the Pandas Library

**Setup** Section

First, **Clone the Repository**: "'''bash'git clone https://github.com/yourusername/personal-data-processing.git '''2. Navigate to the Directory: '''bash'cd personal-data-processing '''3. ***Install Dependencies**:  

One uses it.

*Prepare the 'input.csv' file:** 8.
    You need to include columns like "CLIENT ID," "CONTRACT NO.," and "CLASSIFICATION DATE" in your "input.csv" file, along with any other relevant fields for personal and financial information.

Step 2: **Go to Work** - Type in **bash python data processing.py** to launch the script. You must change the name of your script file from "data processing.py" to its actual name.

3. The **Script Execution** Process: - **The First Run**: - The full 'input.csv' file is processed.
        - To build the "personal.csv" file, these entries are utilised.
        Processing IDs ('processed_ids.csv') records the corresponding 'FI_SUBJECT_CODE's.
    **Runs That Follow**: - The 'personal.csv' file is only updated when new entries with unique 'FI_SUBJECT_CODE' variables are added.
        There are now "processed_ids.csv" files that contain the new "FI_SUBJECT_CODE" names.
        If the 'personal.csv' file does not contain any new entries, it is cleared.

**Pick a Few Outcomes**

The file is named **personal.csv** and is in the "csv" format.
This includes the following fields: ROWID, RECORD_TP, FI_CODE, BRANCH_CODE, FI_SUBJECT_CODE, CUST_TITLE, CUST_NAME, FATHER_TITLE, MOTHER_TITLE, MOTHER_NAME, SPOUSE_TITLE, SPOUSE_NAME, SECTOR_TP, COUNTRY_BIRTH_CODE, NATIONAL_ID_FLAG, ADDRESS_COUNTRY CODE, ADD_ADDRESS_COUNTRY_CODE, BUS_ADDRESS_POSTAL_CODE, BUS_ADDRESS_DISTRICT, BUS_ADDRESS_COUNTRY_CODE, ACC_DATE, DOC_TP, DOC_NO, DOC_ISS_ISSUE_COUNTRY_CODE,PHONE_NO,MAKE_BY,MAKE_DT,AUTH_BY,AUTH_DT,STATUS,CUST_ID,ADDRESS_POSTAL_CODE,ADD_ADDRESS_POSTAL_CODE 1,TP,FI120,1101,C00000001,Mr. John Doe[9,BD,1,BD,BD,BD,1101,2024-12-31]; Ms. Jane Smith[9,BD,1,BD,BD,BD,1101,2024-12-31]; A[12345,12345]; TP[FI120,1101,C00000002]; and

**saved_ids.csv** ""'csv FI_SUBJECT_CODE C00000001 C00000002""

The financial.csv file is this.
Details such as client ID, F_I_subject_code, F_I_contract_code, date of classification, record type, branch code, contract type, contract phase, contract status, currency code, periodicity payment, economic purpose code, credit limit, OD not paid amount, total outstanding, default flag, and more are recorded. The following information is provided: 123,F_I_SUBJECT_CODE_value,F_I_CONTRACT_CODE_value,2024-01-15,D,085,1000,CR,LV,B,BDT,M,9830,125000,120000,245000, Y 456,The values of the variables F_I_SUBJECT_CODE_value and F_I_CONTRACT_CODE_value are 025,1000, CR, LV, B, BDT, M, 9830, 250000, 240000, 490000, U.

## **Authorisation**

To license this project, you must comply with the [MIT License](LICENSE).

---

Learn everything about the Personal Data Processing Script—its features, capabilities, and installation—in this comprehensive README file. Make any changes you think are necessary to make it work for your project.
