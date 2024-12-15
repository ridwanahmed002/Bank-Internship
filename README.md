# Bank Internship Projects

This repository contains two projects completed during my bank internship. Each project has its dedicated folder with a detailed `README.md` file for comprehensive documentation.

---

## 1. **Credit Card Dataset Visualization and Processing**

This Django-based web application facilitates the management, processing, and visualization of credit card datasets.

### Key Features:
- **Upload and Process**: Users can upload CSV files, extract data, and process them into `personal.csv`, `financial.csv`, and `processed_ids.csv`.
- **Dynamic Visualization**: Select columns to generate charts like bar plots, pie charts, scatter plots, and box plots.
- **File Viewing**: View and download processed CSV files directly from the browser.

### Technologies Used:
- **Backend**: Django
- **Frontend**: HTML, CSS, Bootstrap
- **Data Processing**: Python, Pandas

---

## 2. **Personal Data Processing Script**

A Python script automating the processing of customer data into structured outputs for personal and financial information.

### Key Features:
- **Duplicate Prevention**: Ensures each `FI_SUBJECT_CODE` is processed only once by logging entries in `processed_ids.csv`.
- **Automated Data Transformation**: Handles column mapping, default field addition, and financial calculations (`CREDIT_LIMIT`, `TOTAL_OUTSTANDING`, etc.).
- **Output Management**:
  - `personal.csv`: Contains unique personal data.
  - `processed_ids.csv`: Tracks processed `FI_SUBJECT_CODE`s.
  - `financial.csv`: Processes financial details with calculated metrics.

### Technologies Used:
- **Programming Language**: Python
- **Libraries**: Pandas

---

## How to Use

1. **Credit Card Visualization**:
   - Navigate to the `creditcard-visualization` folder.
   - Follow the instructions in the included `README.md` to set up and run the Django application.

2. **Personal Data Processing Script**:
   - Navigate to the `personal-data-processing` folder.
   - Follow the instructions in the included `README.md` to run the Python script for data processing.

---

## License

These projects are licensed under the [MIT License]

