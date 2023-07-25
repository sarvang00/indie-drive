from django.contrib import admin

from .models import File

class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_public', 'upload_date')
    list_display_links = ('id', 'name')
    # list_filter = ('upload_date') change to user
    search_fields = ('name', ) # also add user
    list_editable = ('is_public', )
    list_per_page = 25

admin.site.register(File, FileAdmin)
