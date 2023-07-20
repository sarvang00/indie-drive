from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='files'),
    path('<int:file_id>', views.file, name='file')
]