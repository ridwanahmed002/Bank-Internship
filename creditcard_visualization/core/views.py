from django.shortcuts import render
from .forms import FileUploadForm
from django.core.files.storage import FileSystemStorage

# Home View
def home(request):
    return render(request, "core/home.html")

# Upload File View
def upload_file(request):
    if request.method == "POST" and request.FILES.get('file'):
        uploaded_file = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        return render(request, "core/upload.html", {
            "file_url": file_url,
            "file_name": uploaded_file.name,
            "form": FileUploadForm(),
        })
    else:
        form = FileUploadForm()
    return render(request, "core/upload.html", {"form": form})
