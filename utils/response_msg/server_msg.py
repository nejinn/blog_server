# 200 为业务正常逻辑
OK = {'code': 200, 'msg': 'ok!'}

# 1 开头  系统问题 code
# 11开头 自定义response错误 code

STATUS_CODE_ERROR = {'code': 110001, 'msg': 'response 状态码错误, 请联系后端工程师'}

# 2 开头  blog_user 错误 code
# 21开头 用户创建错误 code
BLOG_ADMIN_CREATE_USER_ERROR = {'code': 210001, 'msg': '管理员创建用户出错'}

# 22开头 用户登录错误 code
BLOG_ADMIN_LOGIN_ERROR = {'code': 220001, 'msg': '账号或者密码错误'}

# 23开头 用户信息错误 code
BLOG_ADMIN_USER_INFO_ERROR = {'code': 23000, 'msg': '用户资料出错'}

# 9 开头 权限错误 code

USER_PERMISSION_LOGIN_ADMIN_REFUSED = {'code': 900001, 'msg': '用户无权限登录 admin 站点'}
