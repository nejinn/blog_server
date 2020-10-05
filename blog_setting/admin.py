from django.contrib import admin
from .models import Sidebar


# Register your models here.
class SidebarAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'level',
        'icon',
        'order',
        'parent',
        'router',
        'active',
        'create_id',
        'update_id',
        'create_date',
        'update_date',
        'is_delete'
    )


admin.site.register(Sidebar, SidebarAdmin)
