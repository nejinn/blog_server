import sys
import os
import django

# 这两行很重要，用来寻找项目根目录，os.path.dirname要写多少个根据要运行的python文件到根目录的层数决定
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_server.settings')
django.setup()

from blog_setting.models import Sidebar

data = list(Sidebar.objects.filter(is_delete=False).values('order', 'name', 'level', 'parent','id','icon'))


def xTree(data):
    tree_list = []
    tree = {}
    parent_id = ''
    for i in data:
        item = i
        tree[item.get('id')] = item
    root = None
    for i in data:
        obj = i
        if not obj.get('parent'):
            root = tree[obj['id']]
            tree_list.append(root)
        else:
            parent_id = obj.get('parent')
            if 'children' not in tree[parent_id]:
                tree[parent_id]['children'] = []
                tree[parent_id]['children'].append(tree[obj['id']])
    return tree_list

s = xTree(data)

print(s)