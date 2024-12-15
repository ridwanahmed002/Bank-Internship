from django.shortcuts import render
from .forms import FileUploadForm
from django.core.files.storage import FileSystemStorage

# Home View
def home(request):
    return render(request, "core/home.html")

# Upload File View
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Store the file name and path in the session
        request.session["uploaded_file_name"] = uploaded_file.name
        request.session["uploaded_file_url"] = file_url

        return render(request, "core/upload.html", {
            "file_url": file_url,
            "file_name": uploaded_file.name,
            "form": FileUploadForm(),
        })

    # Load file details from the session if they exist
    file_url = request.session.get("uploaded_file_url", None)
    file_name = request.session.get("uploaded_file_name", None)

    return render(request, "core/upload.html", {
        "file_url": file_url,
        "file_name": file_name,
        "form": FileUploadForm(),
    })

def check_header(request):
    # Placeholder for checking header logic
    return render(request, "core/check_header.html")

def visualize_data(request):
    # Placeholder for visualization logic
    return render(request, "core/visualize_data.html")

def extract_csv(request):
    # Placeholder for CSV extraction logic
    return render(request, "core/extract_csv.html")
