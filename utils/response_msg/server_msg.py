# 200 为业务正常逻辑
OK = {'code': 200, 'msg': 'ok!'}

# 1 开头  系统问题 code
# 11开头 自定义response错误 code

STATUS_CODE_ERROR = {'code': 110001, 'msg': 'response 状态码错误'}

# 12开头 校验数据类型错误 code
DATA_TYPE_LIST_ERROR = {'code': 120001, 'msg': '数据类型应该是 list'}
DATA_TYPE_DICT_ERROR = {'code': 120002, 'msg': '数据类型应该是 dict'}

# 13开头 删除参数错误 code
DELETE_USER_ID_ERROR = {'code': 130001, 'msg': '用户资料 id 不存在'}
DELETE_BASE_USER_ID_ERROR = {'code': 130002, 'msg': '用户 id 不存在'}
DELETE_USER_ID_COMPARE_ERROR = {'code': 130003, 'msg': '用户 id 和用户资料 id 不匹配'}
DELETE_USER_ERROR = {'code': 130004, 'msg': '删除用户错误'}
DELETE_USER_SELF_ERROR = {'code': 130005, 'msg': '用户不能删除自己'}

# 14开头 删除参数错误 code
LAUNCH_USER_ID_ERROR = {'code': 140001, 'msg': '用户资料 id 不存在'}
LAUNCH_BASE_USER_ID_ERROR = {'code': 140002, 'msg': '用户 id 不存在'}
LAUNCH_USER_ID_COMPARE_ERROR = {'code': 140003, 'msg': '用户 id 和用户资料 id 不匹配'}
LAUNCH_USER_ERROR = {'code': 140004, 'msg': '启用用户错误'}
# DELETE_USER_SELF_ERROR = {'code': 130005, 'msg': '用户不能删除自己'}

# 15开头， 编辑用户参数错误 code
EDITOR_USER_ERROR = {'code': 150001, 'msg': '编辑用户错误'}

# 2 开头  blog_user 错误 code
# 21开头 用户创建/修改错误 code
BLOG_ADMIN_CREATE_USER_ERROR = {'code': 210001, 'msg': '管理员创建用户出错'}
BLOG_ADMIN_CREATE_USER_TYPE_ERROR = {'code': 210002, 'msg': "用户类型错误"}
BLOG_ADMIN_CREATE_USER_GENDER_ERROR = {'code': 210003, 'msg': "用户性别错误"}
# BLOG_ADMIN_UPDATE_USER_ERROR = {'code': 210004, 'msg': "用户名"}

# 22开头 用户登录错误 code
BLOG_ADMIN_LOGIN_ERROR = {'code': 220001, 'msg': '账号或者密码错误'}

# 23开头 用户信息错误 code
BLOG_ADMIN_USER_INFO_ERROR = {'code': 230001, 'msg': '用户资料出错'}

# 9 开头 权限错误 code

USER_PERMISSION_LOGIN_ADMIN_REFUSED = {'code': 900001, 'msg': '用户无权限登录 admin 站点'}
