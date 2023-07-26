from datetime import datetime
import os
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from files.models import File
from files.awssdk import S3ClientObject
from indiedrive.settings import MEDIA_ROOT
from pages.models import FileServer

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/users/login/')
def index(request):
    return render(request, template_name='pages/index.html')

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/users/login/')
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file_obj = request.FILES['file']

        # Save to file system
        tmp_fs = FileServer(file=file_obj)
        tmp_fs.save()

        # Store to s3
        status = S3ClientObject().upload_file_to_s3(tmp_fs.file.path, file_obj.name)

        if status:
            # On successful upload, store to database
            new_file = File.objects.create(owner=request.user, name=file_obj.name, s3Uri=status, is_public=True, upload_date=datetime.now())
            # Remove the temporary file system entries and clear temp storage
            FileServer.objects.all().delete()
            # Loop through the files in the MEDIA_ROOT directory
            for root, dirs, files in os.walk(MEDIA_ROOT):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
            messages.success(request, 'File uploaded successfully')
        else:
            # Raise the error message
            messages.error(request, 'File upload failed')
        return redirect('index')

def about(request):
    return render(request, 'pages/about.html')