from django.shortcuts import render

def index(request):
    return render(request, 'files/files.html')

def file(request):
    return render(request, 'files/file.html')