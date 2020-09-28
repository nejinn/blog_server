# from utils.response_data.response import ResponseDate
# from rest_framework.views import APIView
# import collections
#
#
# class ValidRequestArgs(APIView):
#     args_dict = None
#     checked_args = None
#     request = None
#
#     @staticmethod
#     def default_required_help_text(name):
#         return '{} 不能为空'.format(name)
#
#     @classmethod
#     def add_args(cls, name, required=False, help_text=None):
#         cls.args_dict[name] = {
#             'required': required,
#             'help_text': help_text
#         }
#
#     @classmethod
#     def init_args(cls, request):
#         cls.args_dict = collections.OrderedDict()
#         cls.checked_args = collections.OrderedDict()
#         cls.request = request
#
#     @classmethod
#     def check_required(cls, key):
#         if cls.args_dict.get(key).get('required') and cls.request.data.get(key) is None :
#             data = {
#                 'error': cls.default_required_help_text(
#                     cls.args_dict.get(key).get('help_text')
#                 )
#             }
#             return ResponseDate.json_data(data=data)
#
#         cls.checked_args[key] = cls.request.data.get(key)
#
#     @classmethod
#     def check_args(cls):
#         args_keys = list(cls.args_dict.keys())
#         list(map(cls.check_required, args_keys))
#         return cls.check_args

