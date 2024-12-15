from django.shortcuts import render, redirect
from .forms import FileUploadForm
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os

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
    # Placeholder for visualization logic
    return render(request, "core/visualize_data.html")

def extract_csv(request):
    # Placeholder for CSV extraction logic
    return render(request, "core/extract_csv.html")
