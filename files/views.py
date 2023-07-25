from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from files.models import File

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/users/login/')
def index(request):
    # TODO: Filter files for the owner
    files = File.objects.all().filter(owner=request.user.id).order_by('-upload_date')

    shared_files_list = File.shared.through.objects.all().filter(user_id=request.user.id)
    shared_files = list()

    for file_info in shared_files_list:
        shared_files.append(File.objects.get(pk=file_info.id))

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
        return redirect('myfiles')