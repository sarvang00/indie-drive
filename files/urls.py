from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='myfiles'),
    path('sharedfiles', views.shared, name='sharedfiles'),
    path('<int:file_id>', views.file, name='file')
]