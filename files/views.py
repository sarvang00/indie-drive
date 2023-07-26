from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from files.models import File

from files.awssdk import S3ClientObject

import requests, json

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/users/login/')
def index(request):
    files = File.objects.all().filter(owner=request.user.id).order_by('-upload_date')

    shared_files_list = File.shared.through.objects.all().filter(user_id=request.user.id)
    shared_files = list()

    for file_info in shared_files_list:
        shared_files.append(File.objects.get(pk=file_info.file_id))

    context = {
        'files': files,
        'shared_files': shared_files
    }
    return render(request, 'files/myfiles.html', context)

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/users/login/')
def myfile(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    shared = file.shared.all()
    context = {
        'file': file,
        'shared': shared
    }
    return render(request, 'files/myfile.html', context)

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/users/login/')
def stop_sharing(request):
    if request.method == 'POST':
        file_id = request.POST['file_id']
        file = File.objects.get(pk=file_id)
        file.shared.clear()
        return redirect('myfiles')
    
@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/users/login/')
def share_with_user(request):
    if request.method == 'POST':
        file_id = request.POST['file_id']
        receiver_email = request.POST['receiver_email']
        receiver_message = request.POST['receiver_message']

        file = File.objects.get(pk=file_id)
        file.shared.add(User.objects.get(email=receiver_email))

        # Prepare the data to be sent as JSON
        data = {
            'receiver_email': receiver_email,
            'receiver_message': receiver_message
        }

        # Replace the URL with your API endpoint
        api_url = 'https://mgv62yuw8f.execute-api.us-east-1.amazonaws.com/staging/'

        try:
            # Send the POST request with JSON data
            response = requests.post(api_url, json=data)

            # Check the response status code (optional)
            if response.status_code == 200:
                print("Email sent successfully!")
            else:
                print(f"Failed to send email. Status code: {response.status_code}")

            return redirect('myfiles')

        except requests.exceptions.RequestException as e:
            print("Error sending the request:", e)

            # Handle the error as required
            return HttpResponseServerError("Failed to send the email.")

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/users/login/')
def make_file_private(request):
    if request.method == 'POST':
        file_id = request.POST['file_id']
        file = File.objects.get(pk=file_id)

        status = S3ClientObject().set_public_access_to_false(file.name)
        if status:
            file.is_public = False
            file.save()
            messages.success(request, 'File access changed to private')
        else:
            messages.error(request, 'File access change failed')
            
        return redirect('myfiles')
    
@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/users/login/')
def make_file_public(request):
    if request.method == 'POST':
        file_id = request.POST['file_id']
        file = File.objects.get(pk=file_id)

        status = S3ClientObject().set_public_access_to_true(file.name)
        if status:
            file.is_public = True
            file.save()
            messages.success(request, 'File access changed to public')
        else:
            messages.error(request, 'File access change failed')
            
        return redirect('myfiles')
    
@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/users/login/')
def delete_file(request):
    if request.method == 'POST':
        file_id = request.POST['file_id']
        file = File.objects.get(pk=file_id)

        status = S3ClientObject().delete_file_from_s3(file.name)
        if status:
            file.delete()
            messages.success(request, 'File deleted')
        else:
            messages.error(request, 'File deletion failed')
            
        return redirect('myfiles')