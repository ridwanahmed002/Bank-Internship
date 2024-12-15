from django.shortcuts import render, redirect
from .forms import FileUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import pandas as pd
import subprocess
import os
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO


# Home View
def home(request):
    return render(request, "core/home.html")

# Upload File View


def upload_file(request):
    fs = FileSystemStorage()

    # Handle file deletion
    if request.GET.get("action") == "delete":
        file_url = request.session.get("uploaded_file_url")
        if file_url:
            file_path = "." + file_url  # Relative file path to the uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)  # Delete the file
            # Clear session data
            request.session.pop("uploaded_file_name", None)
            request.session.pop("uploaded_file_url", None)
        return redirect("upload_file")

    # Handle file upload
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Save file details in the session
        request.session["uploaded_file_name"] = uploaded_file.name
        request.session["uploaded_file_url"] = file_url

        return redirect("upload_file")

    # Load file details from session
    file_url = request.session.get("uploaded_file_url")
    file_name = request.session.get("uploaded_file_name")

    return render(request, "core/upload.html", {
        "file_url": file_url,
        "file_name": file_name,
    })


def check_header(request):
    # Get the file path from session
    uploaded_file_url = request.session.get("uploaded_file_url", None)
    file_path = None

    if uploaded_file_url:
        # Convert the relative file path
        file_path = "." + uploaded_file_url  # Media files are stored with '/media/'

    context = {}

    if file_path:
        try:
            # Read the uploaded CSV file
            df = pd.read_csv(file_path)
            
            # Get the first 10 rows
            head_data = df.head(10).to_html(classes="table table-bordered", index=False)

            # Get dataset description
            describe_data = df.describe(include="all").to_html(classes="table table-bordered", index=True)

            # Pass data to the template
            context["head_data"] = head_data
            context["describe_data"] = describe_data
        except Exception as e:
            context["error"] = f"Error reading the file: {str(e)}"
    else:
        context["error"] = "No file uploaded. Please upload a file first."

    return render(request, "core/check_header.html", context)

def visualize_data(request):
    file_url = request.session.get("uploaded_file_url")
    file_path = None
    context = {}

    # Check if file exists in the session
    if file_url:
        file_path = "." + file_url  # Relative file path to the uploaded file

    if file_path and os.path.exists(file_path):
        # Load the uploaded CSV
        df = pd.read_csv(file_path)

        # Separate numeric and categorical columns
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

        context["numeric_columns"] = numeric_columns
        context["categorical_columns"] = categorical_columns

        # Handle form submission
        if request.method == "POST":
            col_x = request.POST.get("col_x")
            col_y = request.POST.get("col_y")
            chart_type = request.POST.get("chart_type")
            extra_columns = request.POST.getlist("extra_columns[]")

            # Generate chart based on selection
            plt.figure(figsize=(10, 6))
            try:
                if chart_type == "bar" and col_x in categorical_columns:
                    # Bar chart based on counts or grouping
                    df[col_x].value_counts().plot(kind="bar")
                    plt.title(f"Bar Chart of {col_x}")
                elif chart_type == "pie" and col_x in categorical_columns:
                    # Pie chart
                    df[col_x].value_counts().plot(kind="pie", autopct='%1.1f%%')
                    plt.title(f"Pie Chart of {col_x}")
                elif chart_type == "scatter" and col_x in numeric_columns and col_y in numeric_columns:
                    # Scatter plot
                    plt.scatter(df[col_x], df[col_y])
                    plt.title(f"Scatter Plot: {col_x} vs {col_y}")
                    plt.xlabel(col_x)
                    plt.ylabel(col_y)
                elif chart_type == "box" and col_x in numeric_columns and col_y in numeric_columns:
                    # Box plot
                    df[[col_x, col_y]].boxplot()
                    plt.title(f"Box Plot of {col_x} and {col_y}")
                elif extra_columns:
                    # Additional columns logic (e.g., group by)
                    selected_columns = [col_x] + extra_columns
                    df[selected_columns].plot(kind="line")
                    plt.title(f"Line Chart for {', '.join(selected_columns)}")
                else:
                    return HttpResponse("Invalid column selection for the chosen chart type.")

                # Save the chart to a BytesIO buffer
                buffer = BytesIO()
                plt.tight_layout()
                plt.savefig(buffer, format="png")
                plt.close()
                buffer.seek(0)

                # Return the chart as an image response
                return HttpResponse(buffer.getvalue(), content_type="image/png")

            except Exception as e:
                return HttpResponse(f"Error generating chart: {str(e)}")
    else:
        context["error"] = "No file uploaded or file does not exist."

    return render(request, "core/visualize_data.html", context)

def extract_csv(request):
    context = {}
    script_path = os.path.join(settings.BASE_DIR, "script.py")
    uploaded_file_url = request.session.get("uploaded_file_url")

    if not uploaded_file_url:
        context["error"] = "No file uploaded. Please upload a file first."
        return render(request, "core/extract_csv.html", context)

    input_file = os.path.join(settings.BASE_DIR, uploaded_file_url.strip("/"))
    output_dir = os.path.join(settings.MEDIA_ROOT, "extracted_csvs")
    os.makedirs(output_dir, exist_ok=True)

    personal_output_file = os.path.join(output_dir, "personal.csv")
    processed_ids_file = os.path.join(output_dir, "processed_ids.csv")
    financial_output_file = os.path.join(output_dir, "financial.csv")

    try:
        print(f"Running script.py with arguments:")
        print(f"Input File: {input_file}")
        print(f"Personal Output: {personal_output_file}")
        print(f"Processed IDs: {processed_ids_file}")
        print(f"Financial Output: {financial_output_file}")

        subprocess.run([
            "python", script_path,
            input_file, personal_output_file, processed_ids_file, financial_output_file
        ], check=True)

        context["success"] = "CSV files successfully extracted!"
        context["personal_file_url"] = os.path.join(settings.MEDIA_URL, "extracted_csvs/personal.csv")
        context["processed_ids_file_url"] = os.path.join(settings.MEDIA_URL, "extracted_csvs/processed_ids.csv")
        context["financial_file_url"] = os.path.join(settings.MEDIA_URL, "extracted_csvs/financial.csv")
    except subprocess.CalledProcessError as e:
        print(f"Error: {str(e)}")
        context["error"] = f"Error running script: {str(e)}"

    return render(request, "core/extract_csv.html", context)

def view_csv(request, file_type):
    """
    View to display the content of personal.csv or financial.csv
    based on the file_type passed in the URL.
    """
    output_dir = os.path.join(settings.MEDIA_ROOT, "extracted_csvs")
    file_path = None

    # Determine which file to display
    if file_type == "personal":
        file_path = os.path.join(output_dir, "personal.csv")
    elif file_type == "financial":
        file_path = os.path.join(output_dir, "financial.csv")
    else:
        return render(request, "core/view_csv.html", {"error": "Invalid file type."})

    # Check if file exists
    if not os.path.exists(file_path):
        return render(request, "core/view_csv.html", {"error": f"File '{file_type}.csv' not found."})

    # Read the CSV content using pandas
    try:
        df = pd.read_csv(file_path)
        data_html = df.to_html(classes="table table-bordered table-striped", index=False)
        return render(request, "core/view_csv.html", {"data": data_html, "file_type": file_type})
    except Exception as e:
        return render(request, "core/view_csv.html", {"error": f"Error reading file: {str(e)}"})
