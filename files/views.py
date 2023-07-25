from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from files.models import File

def index(request):
    # TODO: Filter files for the owner
    files = File.objects.order_by('-upload_date')
    paginator = Paginator(files, 6)
    page = request.GET.get('page')
    paged_files = paginator.get_page(page)

    context = {
        'files': paged_files
    }
    return render(request, 'files/myfiles.html', context)

def shared(request):
    return render(request, 'files/sharedfiles.html')

def myfile(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    context = {
        'file': file
    }
    return render(request, 'files/myfile.html', context)