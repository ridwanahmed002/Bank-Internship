---

# Credit Card Dataset Visualization and Processing

## Overview

This project is a Django-based application designed to upload, process, and visualize credit card datasets. The application includes features for:
- Uploading CSV files.
- Extracting and processing personal and financial data.
- Visualizing dataset columns through various charts.
- Downloading processed outputs.

---

## Features

1. **File Upload**:
   - Upload credit card datasets in CSV format.
   - Automatically store the uploaded file for further processing.

2. **Extract CSV**:
   - Process the uploaded file to generate:
     - `personal.csv`: Contains personal details extracted from the dataset.
     - `financial.csv`: Contains financial details.
     - `processed_ids.csv`: Tracks processed IDs to avoid duplication.

3. **Visualize Data**:
   - Select relevant columns for visualization.
   - Generate the following chart types:
     - Bar Chart
     - Pie Chart
     - Scatter Plot
     - Box Plot
   - Dynamically add more columns for enhanced analysis.

4. **View Processed Files**:
   - Directly view the contents of `personal.csv` and `financial.csv` within the browser.
   - Download the processed files.

---

## Project Structure

```
creditcard_visualization/
├── core/                          # Main application
│   ├── templates/core/            # HTML templates
│   ├── views.py                   # Django views for processing
│   ├── urls.py                    # URL routing for the application
├── media/                         # Directory for uploaded and processed files
│   ├── extracted_csvs/            # Output files (personal.csv, financial.csv, etc.)
├── script.py                      # Python script for processing input files
├── manage.py                      # Django management script
```

---

## Installation

### Prerequisites
- Python 3.x
- Django 5.x
- Pandas

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ridwanahmed002/creditcard-visualization.git
   cd creditcard-visualization
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## Usage

### 1. Upload a Dataset
- On the home page, click **Upload Dataset**.
- Choose a CSV file and upload it.

### 2. Extract CSV Files
- Navigate to the **Extract CSV** page.
- Process the uploaded file to generate `personal.csv`, `financial.csv`, and `processed_ids.csv`.

### 3. Visualize Data
- Navigate to the **Visualize Data** page.
- Select relevant columns and a chart type.
- Generate dynamic charts to analyze the dataset.

### 4. View and Download Processed Files
- Navigate to the **View CSV** links to see the contents of processed files.
- Download files directly from the links provided.

---

## Outputs

- **personal.csv**:
  - Contains key personal details extracted from the dataset.

- **financial.csv**:
  - Contains calculated financial metrics like credit limits and outstanding amounts.

- **processed_ids.csv**:
  - Tracks processed `FI_SUBJECT_CODE` values to avoid duplication.

---

## Sample Dataset

Ensure the input CSV file contains the following required columns:
- `CLIENT ID`
- `ZIP CODE`
- `REGION`
- `CONTRACT NO`
- `CLASSIFICATION DATE`
- `CREDIT LIMIT [BDT]`
- `CREDIT LIMIT [USD]`
- `OUTSTANDING [BDT]`
- `OUTSTANDING [USD]`
- `UNPAID EMI [BDT]`

---

## Scripts

### `script.py`
- Processes the uploaded file to generate:
  - Personal data (`personal.csv`).
  - Financial data (`financial.csv`).
  - Processed IDs (`processed_ids.csv`).

Usage:
```bash
python script.py <input_file> <personal_output_file> <processed_ids_file> <financial_output_file>
```

---

## Technologies Used

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, Bootstrap
- **Data Processing**: Pandas
- **Database**: SQLite (default Django DB)

---

## Future Enhancements

- Add more advanced visualization options (e.g., heatmaps).
- Support for larger datasets with background processing.
- User authentication for dataset uploads and processing.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

---
