from django.contrib import admin
from .models import *


# Register your models here.

class BlogUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_pic',
        'user_type',
        'user_phone',
        'user_email',
        'user_exp',
        'user_level',
        'user_birthday',
        'user_gender',
        'user_ip',
        'user_last_login_ip',
        'user_last_login_time',
        'create_date',
        'update_date',
        'is_delete',
    )


admin.site.register(BlogUser, BlogUserAdmin)
