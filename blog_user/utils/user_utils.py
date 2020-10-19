from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from blog_server import settings
from io import BytesIO
from django.core.files import File
from blog_user.models import BlogUser


class CreateUser(object):

    @staticmethod
    def set_default_user_pic(username):
        """
        给没有头像的新建用户生成一个以 username 第一个字符串为文本的 默认头像
        :param username:
        :return:
        """
        pic_size = (80, 80)
        pic = Image.new("RGB", pic_size, (255, 255, 255))
        draw = ImageDraw.Draw(pic)
        text = username[0]
        font = ImageFont.truetype(os.path.join(settings.STATICFILES_DIRS[0], 'fonts', 'wqwmh.ttf'), 60,
                                  encoding="uft-8")
        text_width = font.getsize(text)
        text_coordinate = int((pic_size[0] - text_width[0]) / 2), int((pic_size[1] - text_width[1]) / 2)
        draw.text(text_coordinate, text, 'black', font)
        pic_blob = BytesIO()
        pic.save(pic_blob, 'png')
        return File(pic_blob)

    @staticmethod
    def set_default_user_pic_name(userid, is_default=True):
        """
        给用户头像重命名
        :param is_default: 是否默认头像
        :param userid: 用户id
        :return:
        """
        if is_default:
            return 'user-pic/user-id-{}/default.png'.format(userid)
        return 'user-pic/user-id-{}/avator.png'.format(userid)

    @classmethod
    def save_user_pic(cls, username, userid, request):
        """
        为 给用户保存 头像
        :param request:
        :param username: 用户名
        :param userid: 用户id
        :return:
        """
        user_pic = cls.set_default_user_pic(username)
        blog_user = BlogUser()
        blog_user.base_user_id = userid

        blog_user.create_id = request.user.id
        blog_user.update_id = request.user.id
        blog_user.user_type = request.data['user_type']
        blog_user.user_phone = request.data.get('user_phone')
        blog_user.user_email = request.data['user_email']
        blog_user.user_birthday = request.data.get('user_birthday')
        blog_user.user_gender = request.data['user_gender']

        instance_default_pic = os.path.join(settings.MEDIA_ROOT, cls.set_default_user_pic_name(userid))
        if os.path.exists(instance_default_pic):
            os.remove(instance_default_pic)

        blog_user.user_pic.save(cls.set_default_user_pic_name(userid), user_pic, save=False)
        blog_user.save()

    @staticmethod
    def create_base_user(username, password):
        """
        创建 base_user
        :param username: 用户名
        :param password: 用户密码
        :return:
        """
        password = make_password(password, salt=None, hasher='default')
        user = User(username=username, password=password, is_active=False, is_staff=False, is_superuser=False)
        user.save()
        return user


class DeleteUser(object):

    @staticmethod
    def delete_user(user, base_user):
        """
        删除用户
        :param user:  BlogUser 对象
        :param base_user:  User 对象
        :return:
        """
        user.is_delete = True
        user.save()

        base_user.is_active = False
        base_user.is_staff = False
        # base_user.is_superuser = False
        base_user.save()


class LaunchUser(object):

    @staticmethod
    def launch_user(user, base_user):
        """
        启用
        :param user:  BlogUser 对象
        :param base_user:  User 对象
        :return:
        """
        user.is_delete = False
        user.save()

        base_user.is_active = True
        if base_user.is_superuser:
            base_user.is_staff = True
        base_user.save()
