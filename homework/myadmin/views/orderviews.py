from django.shortcuts import render
from django.http import HttpResponse
from .. models import Orders
# Create your views here.

def index(request):
    
    orderlist = Orders.objects.all()
    # 获取搜索条件
    types = request.GET.get('type',None)
    keywords = request.GET.get('keywords',None)
    # 判断是否具有搜索条件
    # print(types,keywords)
    if types:
        if types == 'all':
            from django.db.models import Q
            orderlist = Orders.objects.filter(
                Q(title__contains=keywords)|
                Q(descr__contains=keywords)|
                Q(price__contains=keywords)|
                Q(store__contains=keywords)|
                Q(info__contains=keywords)   
            )
        elif types == "status":
            orderlist = Orders.objects.filter(status__contains=keywords)
        
    else:
        # 获取所有用户数据
        orderlist = Orders.objects.all()
    # 导入分页类
    from django.core.paginator import Paginator
    # 实例化分类页　参数１　数据集合　参数２　每页显示条数
    paginator = Paginator(orderlist,10)
    # 获取当前页码数
    p = request.GET.get('p',1)
    # 获取当前页的数据
    orderlist = paginator.page(p)
    # 分配数据
    context = {'orderlist':orderlist}
    # 加载模板
    return render(request,'myadmin/order/list.html',context)