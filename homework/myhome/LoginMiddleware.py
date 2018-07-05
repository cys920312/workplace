from django.shortcuts import render
from django.http import HttpResponse
import re
class LoginMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,request):
        # 定义当前用户请求的url路径
        u = request.path
        # 后台中间键验证
        if re.match('/myadmin/',u) and u not in ['/myadmin/user/login/']:
            # 判断是否登录
            if not request.session.get('AdminUser',None):
                # 没有登录
                return HttpResponse('<script>alert("请先登录");location.href="/myadmin/user/login/?next='+u+'"</script>')



        # 定义需要登录的url请求
        ulist=['/ordercheck/','/addressedit/','/addressadd/','/ordercreate/','/buy/','/mycenter/','/myorders/',]
        # 判断当前的请求是否需要登录
        if u in ulist:
            # 验证是否登录
            if not request.session.get('VipUser',None):
                return HttpResponse('<script>alert("请先登录");location.href="/login/?next='+u+'"</script>')
        response = self.get_response(request)
        return response