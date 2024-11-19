import os
import shutil
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def compress_file(file, zip_name):
    """Compress a single file and return the zip path."""
    # Create a temporary directory to store the file
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_files')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Save the file to the temporary directory
    file_path = os.path.join(temp_dir, file.name)
    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

    # Create the zip file for the single file
    zip_path = os.path.join(settings.MEDIA_ROOT, f"{zip_name}.zip")
    shutil.make_archive(zip_path.replace(".zip", ""), 'zip', temp_dir)

    # Clean up temporary files after zipping
    shutil.rmtree(temp_dir)

    return zip_path

def convert(request):
    template = 'index.html'
    zip_files = []  # List to store paths of the generated zip files

    if request.method == "POST":
        uploaded_files = request.FILES.getlist('files')  # Get the uploaded files
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                zip_name = uploaded_file.name.split('.')[0]  # Use the original file name (without extension) for the zip name
                zip_path = compress_file(uploaded_file, zip_name)  # Compress each file separately
                zip_file_url = os.path.join(settings.MEDIA_URL, f"{zip_name}.zip")  # URL for the zip file
                zip_files.append(zip_file_url)  # Add the zip file URL to the list
            
            # Pass the zip files URLs to the template
            return render(request, template, {'zip_files': zip_files})

    return render(request, template, {'zip_files': zip_files})
