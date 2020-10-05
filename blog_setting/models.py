from django.db import models
from blog_user.models import BaseModel
from blog_user.models import BaseModel


class Sidebar(BaseModel):
    name = models.CharField(verbose_name='导航名称', max_length=225, default="", blank=True, null=True)
    level = models.IntegerField(verbose_name='导航级别', blank=True, null=True, default=10)
    icon = models.CharField(verbose_name='导航icon', max_length=225, default="nav-icon fas nlyfont nly-icon-dashboard",
                            blank=True, null=True)
    order = models.IntegerField(verbose_name='导航顺序', blank=True, null=True, default=10)
    parent = models.IntegerField(verbose_name='父级导航', blank=True, null=True, default=0)
    router = models.CharField(verbose_name='router name', max_length=225, default=None, blank=True, null=True, help_text='有子菜单时不需要设置')
    active = models.CharField(verbose_name='router active', max_length=225, default=None, blank=True, null=True, help_text='无子菜单时，必须设置')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id', 'level')
        verbose_name_plural = '导航表'
        verbose_name = '导航表'
