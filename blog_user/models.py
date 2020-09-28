from django.db import models
from django.contrib.auth.models import User
from enum import Enum


# Create your models here.

class BaseModel(models.Model):
    create_data = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_data = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name='删除', default=False)

    class Meta:
        abstract = True


class BlogUser(BaseModel):
    class UserType(Enum):
        super_user = 1
        base_user = 2

    USER_TYPE_TEXT = {
        UserType.super_user: "超级用户",
        UserType.base_user: "普通用户"
    }

    base_user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_pic = models.ImageField(verbose_name='用户头像', help_text='用户头像')
    user_type = models.IntegerField(verbose_name='用户类型', default=UserType.base_user.value,
                                    help_text='用户类型，base_user 无法登陆 admin端', blank=True, null=True)
    user_phone = models.CharField(verbose_name='用户手机号', default=None, max_length=11, help_text='用户手机号码', blank=True,
                                  null=True)
    user_email = models.EmailField(verbose_name='用户邮箱', default=None, blank=True, help_text='用户邮箱', null=True)
    user_exp = models.IntegerField(verbose_name='用户经验', default=0, blank=True, null=True, help_text='用户经验值')
    user_level = models.IntegerField(verbose_name='用户等级', default=0, blank=True, null=True, help_text='用户等级')
    user_birthday = models.DateField(verbose_name='用户出生年月日', help_text='用户出生年月日', default=None, null=True)
    user_gender = models.BooleanField(verbose_name='用户性别', default=False, help_text='性别')

    def __str__(self):
        return self.base_user.username

    class Meta:
        verbose_name_plural = '用户表'
        verbose_name = '用户表'
