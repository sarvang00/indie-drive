from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/users/login/')
def index(request):
    return render(request, template_name='pages/index.html')

def about(request):
    return render(request, 'pages/about.html')