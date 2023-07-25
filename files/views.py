from django.shortcuts import render

def index(request):
    return render(request, 'files/myfiles.html')

def shared(request):
    return render(request, 'files/sharedfiles.html')

def file(request):
    return render(request, 'files/file.html')