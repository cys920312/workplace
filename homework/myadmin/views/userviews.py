from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import Users
import os
# Create your views here.
# 会员登录
def login(request):
    if request.method == "GET":
        return render(request,"myadmin/login.html")

    elif request.method == "POST":
        from django.contrib.auth.hashers import make_password, check_password
        #                                                                                                                              = request.POST.get('username',None)
        # password = request.POST.get('password',None)
        # 执行登录
        # 根据用户名先获取用户对象.在检测密码是否正确
        try:
            ob = Users.objects.get(username = request.POST['username'])
            # 检测密码是否正确
            res = check_password(request.POST['password'],ob.password)
            if res:
                # 密码正确
                request.session['AdminUser'] = {'uid':ob.id,'username':ob.username}
                return HttpResponse('<script>alert("登录成功");location.href="/myadmin/"</script>')

        except:
            # 用户名错误
            pass
        
        return HttpResponse('<script>alert("用户名或密码错误");location.href="/myadmin/user/login"</script>')

# 会员退出
def logout(request):
    data  = {}
    if  request.session.get('AdminUser',None):
        request.session['AdminUser'] = data
        return HttpResponse('<script>alert("退出成功");location.href="/myadmin/user/login"</script>')
    else:
        return HttpResponse('<script>alert("未登录无法退出");location.href="/myadmin/user/login"</script>')
# 会员列表
def index(request):
     # 获取搜索条件
    types = request.GET.get('type',None)
    keywords = request.GET.get('keywords',None)
    # 判断是否具有搜索条件
    # print(types,keywords)
    if types:
        if types == 'all':
            # 有搜索条件
            from django.db.models import Q
            userlist = Users.objects.filter(
                Q(username__contains=keywords)|
                Q(age__contains=keywords)|
                Q(email__contains=keywords)|
                Q(phone__contains=keywords)|
                Q(sex__contains=keywords)         
            )
        elif types == 'username':
            # 按照用户名搜索
            userlist = Users.objects.filter(username__contains=keywords)
        elif types == 'age':
            # 按照年龄搜索
            userlist = Users.objects.filter(age__contains=keywords)
        elif types == 'email':
            # 按照邮箱搜索
            userlist = Users.objects.filter(email__contains=keywords)
        elif types == 'phone':
            # 按照手机号搜索
            userlist = Users.objects.filter(phone__contains=keywords)
        elif types == 'sex':
            # 按照性别搜索
            userlist = Users.objects.filter(sex__contains=keywords)
    else:
        # 获取所有用户数据
        userlist = Users.objects.filter()
    # 导入分页类
    from django.core.paginator import Paginator
    # 实例化分类页　参数１　数据集合　参数２　每页显示条数
    paginator = Paginator(userlist,10)
    # 获取当前页码数
    p = request.GET.get('p',1)
    # 获取当前页的数据
    ulist = paginator.page(p)
    # 分配数据
    context = {'userlist':ulist}
    # 加载模板
    return render(request,'myadmin/user/list.html',context)
# 显示添加页面
def add(request):
    if request.method =='GET':
        return render(request,'myadmin/user/add.html')   
    elif request.method == 'POST':
        try:
            # 接受表单提交的数据
            data = request.POST.copy().dict()
            # 删除csrf字段的数据
            del data['csrfmiddlewaretoken']
            if request.FILES.get('pic',None):
                data['pic'] = uploads(request)
                if data['pic'] == 1:
                    return HttpResponse('<script>alert("上传的文件类型不符合要求");location.href="'+reverse('myadmin_user_add')+'"</script>')
            else:
                del data['pic'] 
             # 执行用户的创建
            ob = Users.objects.create(**data)

            return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_user_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("添加失败");location.href="'+reverse('myadmin_user_add')+'"</script>')
def delete(request):
    try:
        uid = request.GET.get('uid',None)
        ob =Users.objects.get(id=uid) 
        if ob.pic:
            os.remove('.'+ob.pic)
        ob.delete()
        data = {'msg':'删除成功','code':0}
    except:
        data = {'msg':'删除失败','code':1}

    return JsonResponse(data)     
def edit(request):
    # 接受参数
    uid = request.GET.get('uid',None)
    # 获取对象
    ob = Users.objects.get(id=uid)

    if request.method == 'GET':
       
        # 分配数据
        context = {'uinfo':ob}
        # 显示编辑页面
        return render(request,'myadmin/user/edit.html',context)

    elif request.method == 'POST':

        try:
            # 判断是否上传了新的图片
            if request.FILES.get('pic',None):
                # 判断是否使用的默认图
                if ob.pic:
                    # 如果使用的不是默认图,则删除之前上传的头像
                    os.remove('.'+ob.pic)

                # 执行上传
                ob.pic = uploads(request)
                

            ob.username = request.POST['username']
            ob.email = request.POST['email']
            ob.age = request.POST['age']
            ob.sex = request.POST['sex']
            ob.phone = request.POST['phone']
            ob.save()

            return HttpResponse('<script>alert("更新成功");location.href="'+reverse('myadmin_user_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("更新失败");location.href="'+reverse('myadmin_user_edit')+'?uid='+str(ob.id)+'"</script>')
# 执行文件的上传
def uploads(request):
    
    # 获取请求中的 文件 File 
    myfile = request.FILES.get('pic',None)

    # 获取上传的文件后缀名 myfile.name.split('.').pop()
    p = myfile.name.split('.').pop()
    arr = ['jpg','png','jpeg','gif']
    if p not in arr:
        return 1

    import time,random
    # 生成新的文件名
    filename = str(time.time())+str(random.randint(1,99999))+'.'+p
    
    # 打开文件
    destination = open("./static/pics/"+filename,"wb+")

    # 分块写入文件  
    for chunk in myfile.chunks():      
       destination.write(chunk)  

    # # destination.write(myfile.read()) #不推荐

    # 关闭文件
    destination.close()
    
    # return HttpResponse(filename)

    return '/static/pics/'+filename
