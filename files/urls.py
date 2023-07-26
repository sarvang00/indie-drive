from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='myfiles'),
    path('<int:file_id>', views.myfile, name='myfile'),
    path('stop_sharing', views.stop_sharing, name='stop_sharing'),
    path('share_with_user', views.share_with_user, name='share_with_user'),
    path('make_file_private', views.make_file_private, name='make_file_private'),
    path('make_file_public', views.make_file_public, name='make_file_public'),
    path('delete_file', views.delete_file, name='delete_file'),
]