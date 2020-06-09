import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from user.models import UserProfile
from django.core.paginator import Paginator


# Create your views here.
# 查看所有攻略
def get_all_list(request):
    topics = IntroductionInfo.objects.filter(is_show=True).order_by('-create_time')
    users = UserProfile.objects.all()
    username = request.session.get('username')
    paginator = Paginator(topics, 5)
    cur_page = int(request.GET.get('page', 1))
    page = paginator.page(cur_page)
    return render(request, 'topics.html', locals())


def get_user_list(request, username=None):
    # 查看用户个人发布的攻略
    if request.method == 'GET':
        # TODO检验用户是否已登录,待合并项目后利用token进行校验
        _username = request.session.get('username')
        if _username == username:
            try:
                user = UserProfile.objects.get(username=username)
            except:
                return HttpResponse('用户不存在')
            topics = IntroductionInfo.objects.filter(userid_id=user.id, is_show=True).order_by('-create_time')
            paginator = Paginator(topics, 5)
            cur_page = int(request.GET.get('page', 1))
            page = paginator.page(cur_page)
            return render(request, 'user_topics.html', locals())
        else:
            return HttpResponse('对不起!您还没有登录')


def add_topic(request, username=None):
    # 发布攻略界面
    if request.method == 'GET':
        _username = request.session.get('username')
        if _username == username:
            return render(request, 'addtopic.html')
        else:
            return HttpResponse('对不起!您还没有登录')
    # 用户提交攻略
    elif request.method == 'POST':
        try:
            user = UserProfile.objects.get(username=username)
        except:
            result = {'code': 601, 'error': '没有该用户'}
            return JsonResponse(result)
        # TODO将路由提交的用户名和token的用户名作校验
        title = request.POST.get('title')
        if not title:
            result = {'code': 602, 'error': '没有标题'}
            return JsonResponse(result)
        keywords = request.POST.get('keywords')
        if not keywords:
            result = {'code': 603, 'error': '没有关键词'}
            return JsonResponse(result)
        info = request.POST.get('info')
        if not info:
            result = {'code': 604, 'error': '没有文章内容'}
            return JsonResponse(result)
        shortinfo = info[0:29]
        location = request.POST.get('location')
        if not location:
            result = {'code': 605, 'error': '没有地理位置'}
            return JsonResponse(result)
        image = request.FILES.get('image')
        if not image:
            result = {'code': 606, 'error': '没上传游记图片'}
            return JsonResponse(result)
        topic = IntroductionInfo.objects.create(userid_id=user.id, title=title, info=info, shortinfo=shortinfo,
                                                location=location,
                                                image=image,
                                                create_time=time.time()
                                                )
        IntroductionKeyWord.objects.create(titleid_id=topic.id, keywords=keywords)
        result = {'code': 200, 'error': '发布成功'}
        return JsonResponse(result)


def mod_topic(request, username=None, t_id=None):
    if request.method == 'GET':
        _username = request.session.get('username')
        if _username == username:
            topic = IntroductionInfo.objects.get(id=t_id, is_show=True)
            t_kw = IntroductionKeyWord.objects.get(titleid_id=topic.id)
            return render(request, 'modtopic.html', locals())
        else:
            return HttpResponse('对不起!您还没有登录')

    elif request.method == 'POST':
        try:
            user = UserProfile.objects.get(username=username)
        except:
            result = {'code': 601, 'error': '没有该用户'}
            return JsonResponse(result)
        # TODO将路由提交的用户名和token的用户名作校验
        title = request.POST.get('title')
        if not title:
            result = {'code': 602, 'error': '没有标题'}
            return JsonResponse(result)
        keywords = request.POST.get('keywords')
        if not keywords:
            result = {'code': 603, 'error': '没有关键词'}
            return JsonResponse(result)
        info = request.POST.get('info')
        if not info:
            result = {'code': 604, 'error': '没有文章内容'}
            return JsonResponse(result)
        shortinfo = info[0:29]
        location = request.POST.get('location')
        if not location:
            result = {'code': 605, 'error': '没有地理位置'}
            return JsonResponse(result)
        image = request.FILES.get('image')
        if not image:
            result = {'code': 606, 'error': '没上传游记图片'}
            return JsonResponse(result)
        topic = IntroductionInfo.objects.get(id=t_id, is_show=True)
        t_kw = IntroductionKeyWord.objects.get(titleid_id=topic.id)
        topic.title = title
        topic.info = info
        topic.shortinfo = shortinfo
        topic.location = location
        topic.image = image
        topic.mod_time = time.time()
        t_kw.keywords = keywords
        topic.save()
        t_kw.save()
        result = {'code': 200, 'error': '修改成功'}
        return JsonResponse(result)


def del_topic(request, username=None, t_id=None):
    if request.method == 'GET':
        _username = request.session.get('username')
        if _username == username:
            topic = IntroductionInfo.objects.get(id=t_id, is_show=True)
            t_kw = IntroductionKeyWord.objects.get(titleid_id=topic.id)
            t_kw.is_show = False
            topic.is_show = False
            topic.save()
            result = {'code': 200, 'error': '删除成功'}
            return JsonResponse(result)
        else:
            return HttpResponse('对不起!您还没有登录')


def detail_topic(request, t_id=None):
    if request.method == 'GET':
        topic = IntroductionInfo.objects.get(id=t_id, is_show=True)
        user = UserProfile.objects.get(id=topic.userid_id)
        topic.see_count += 1
        topic.save()

        _username = request.GET.get('username')
        is_login = False
        # 路人进入查看
        if _username != request.session.get('username'):
            previous_topic = IntroductionInfo.objects.filter(id__gt=t_id, is_show=True).first()
            next_topic = IntroductionInfo.objects.filter(id__lt=t_id, is_show=True).last()
        # 发布人进入查看
        else:
            is_login = True
            previous_topic = IntroductionInfo.objects.filter(id__gt=t_id, userid_id=user.id, is_show=True).first()
            next_topic = IntroductionInfo.objects.filter(id__lt=t_id, userid_id=user.id, is_show=True).last()
        if previous_topic:
            previous_title = previous_topic.title
            previous_id = previous_topic.id
        else:
            previous_title = None
            previous_id = None

        if next_topic:
            next_title = next_topic.title
            next_id = next_topic.id
        else:
            next_title = None
            next_id = None
        return render(request, 'detailtopic.html', locals())

# def check_login(request, username=None):
#     # 检查用户是否登录,暂用cookies,合并项目后改为token检验
#     _username = request.COOKIES.get('username')
#     if _username == username:
#         return True
#     else:
#         return False
