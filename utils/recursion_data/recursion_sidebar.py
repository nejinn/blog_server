class RecursionSidebar(object):

    # 转换 导航数据为无限极树形
    @staticmethod
    def x_tree(sidebar):
        """
        导航数据为无限极树形
        :param sidebar: 字典数据
        :return:
        """
        tree_list = []
        tree = {}
        for i in sidebar:
            item = i
            tree[item.get('id')] = item
        for i in sidebar:
            obj = i
            if not obj.get('parent'):
                root = tree[obj['id']]
                tree_list.append(root)
            else:
                parent_id = obj.get('parent')
                if 'children' not in tree[parent_id]:
                    tree[parent_id]['children'] = []
                    tree[parent_id]['children'].append(tree[obj['id']])
                else:
                    tree[parent_id]['children'].append(tree[obj['id']])
        return tree_list
