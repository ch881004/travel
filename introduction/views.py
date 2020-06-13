import time
from itertools import chain

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from user.models import UserProfile
from django.core.paginator import Paginator


# Create your views here.
# 查看所有攻略
def get_all_list(request):
    topics = IntroductionInfo.objects.filter(is_show=True).order_by('-create_time')
    if not topics:
        result = {'code': 601, 'error': '没找到文章'}
        return JsonResponse(result)
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
                result = {'code': 602, 'error': '用户不存在'}
                return JsonResponse(result)
            topics = IntroductionInfo.objects.filter(userid_id=user.id, is_show=True).order_by('-create_time')
            if not topics:
                result = {'code': 603, 'error': '没找到文章'}
                return JsonResponse(result)
            paginator = Paginator(topics, 5)
            cur_page = int(request.GET.get('page', 1))
            page = paginator.page(cur_page)
            return render(request, 'user_topics.html', locals())
        else:
            result = {'code': 603, 'error': '对不起!您还没有登录'}
            return JsonResponse(result)


def add_topic(request, username=None):
    # 发布攻略界面
    if request.method == 'GET':
        # TODO将路由提交的用户名和token的用户名作校验
        _username = request.session.get('username')
        if _username == username:
            return render(request, 'addtopic.html')
        else:
            result = {'code': 604, 'error': '对不起!您还没有登录'}
            return JsonResponse(result)
    # 用户提交攻略
    elif request.method == 'POST':
        try:
            user = UserProfile.objects.get(username=username)
        except:
            result = {'code': 605, 'error': '没有该用户'}
            return JsonResponse(result)
        title = request.POST.get('title')
        if not title:
            result = {'code': 606, 'error': '没有标题'}
            return JsonResponse(result)
        keywords = request.POST.get('keywords')
        if not keywords:
            result = {'code': 607, 'error': '没有关键词'}
            return JsonResponse(result)
        info = request.POST.get('info')
        if not info:
            result = {'code': 608, 'error': '没有文章内容'}
            return JsonResponse(result)
        shortinfo = info[0:29]
        location = request.POST.get('location')
        if not location:
            result = {'code': 609, 'error': '没有地理位置'}
            return JsonResponse(result)
        image = request.FILES.get('image')
        if not image:
            result = {'code': 610, 'error': '没上传游记图片'}
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
            try:
                topic = IntroductionInfo.objects.get(id=t_id, is_show=True)
            except:
                result = {'code': 611, 'error': '没找到该文章'}
                return JsonResponse(result)
            try:
                t_kw = IntroductionKeyWord.objects.get(titleid_id=topic.id)
            except:
                result = {'code': 612, 'error': '关键字缺失'}
                return JsonResponse(result)
            return render(request, 'modtopic.html', locals())
        else:
            result = {'code': 613, 'error': '对不起!您还没有登录'}
            return JsonResponse(result)

    elif request.method == 'POST':
        try:
            user = UserProfile.objects.get(username=username)
        except:
            result = {'code': 614, 'error': '没有该用户'}
            return JsonResponse(result)
        # TODO将路由提交的用户名和token的用户名作校验
        title = request.POST.get('title')
        if not title:
            result = {'code': 615, 'error': '没有标题'}
            return JsonResponse(result)
        keywords = request.POST.get('keywords')
        if not keywords:
            result = {'code': 616, 'error': '没有关键词'}
            return JsonResponse(result)
        info = request.POST.get('info')
        if not info:
            result = {'code': 617, 'error': '没有文章内容'}
            return JsonResponse(result)
        shortinfo = info[0:29]
        location = request.POST.get('location')
        if not location:
            result = {'code': 618, 'error': '没有地理位置'}
            return JsonResponse(result)
        image = request.FILES.get('image')
        if not image:
            result = {'code': 619, 'error': '没上传游记图片'}
            return JsonResponse(result)
        try:
            topic = IntroductionInfo.objects.get(id=t_id, is_show=True)
        except:
            result = {'code': 620, 'error': '没找到该文章'}
            return JsonResponse(result)
        try:
            t_kw = IntroductionKeyWord.objects.get(titleid_id=topic.id)
        except:
            result = {'code': 621, 'error': '关键字缺失'}
            return JsonResponse(result)
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
            try:
                topic = IntroductionInfo.objects.get(id=t_id, is_show=True)
            except:
                result = {'code': 622, 'error': '没找到该文章'}
                return JsonResponse(result)
            try:
                t_kw = IntroductionKeyWord.objects.get(titleid_id=topic.id)
            except:
                result = {'code': 623, 'error': '关键字缺失'}
                return JsonResponse(result)
            t_kw.is_show = False
            topic.is_show = False
            topic.save()
            result = {'code': 200, 'error': '删除成功'}
            return JsonResponse(result)
        else:
            result = {'code': 624, 'error': '对不起!您还没有登录'}
            return JsonResponse(result)


def detail_topic(request, t_id=None):
    if request.method == 'GET':
        try:
            topic = IntroductionInfo.objects.get(id=t_id, is_show=True)
        except:
            result = {'code': 625, 'error': '没找到该文章'}
            return JsonResponse(result)
        try:
            user = UserProfile.objects.get(id=topic.userid_id)
        except:
            result = {'code': 626, 'error': '没有该用户'}
            return JsonResponse(result)
        topic.see_count += 1
        topic.save()
        if not request.session.get('username'):
            is_login = False
        else:
            _username = request.GET.get('username')
            if _username == request.session.get('username'):
                is_login = True
            else:
                is_login = False
        # 路人进入查看
        if not is_login:
            try:
                previous_topic = IntroductionInfo.objects.filter(id__gt=t_id, is_show=True).first()
            except:
                result = {'code': 627, 'error': '没找到上一篇文章'}
                return JsonResponse(result)
            try:
                next_topic = IntroductionInfo.objects.filter(id__lt=t_id, is_show=True).last()
            except:
                result = {'code': 628, 'error': '没找到下一篇文章'}
                return JsonResponse(result)
        # 发布人进入查看
        else:
            try:
                previous_topic = IntroductionInfo.objects.filter(id__gt=t_id, userid_id=user.id, is_show=True).first()
            except:
                result = {'code': 629, 'error': '没找到上一篇文章'}
                return JsonResponse(result)
            try:
                next_topic = IntroductionInfo.objects.filter(id__lt=t_id, userid_id=user.id, is_show=True).last()
            except:
                result = {'code': 630, 'error': '没找到下一篇文章'}
                return JsonResponse(result)
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

        messages = IntroductionMessage.objects.filter(topicid_id=topic.id, parent_id=0).order_by('create_time')
        reply_messages = IntroductionMessage.objects.filter(topicid_id=topic.id, parent_id__gt=0).order_by('create_time')
        return render(request, 'detailtopic.html', locals())


def search_topic(request):
    if request.method == 'GET':
        search_word = request.GET.get('search_word')
        if not search_word:
            result = {'code': 631, 'error': "请提交查询内容"}
            return JsonResponse(result)
        username = request.session['username']
        users = UserProfile.objects.all()
        keywords = IntroductionKeyWord.objects.filter(is_show=True, keywords__contains=search_word)
        if not keywords:
            result = {'code': 632, 'error': "未找到相关内容"}
            return JsonResponse(result)
        topics = IntroductionInfo.objects.none()
        for keyword in keywords:
            try:
                _topics = IntroductionInfo.objects.filter(is_show=True, id=keyword.titleid_id)
            except:
                result = {'code': 633, 'error': "没找到文章"}
                return JsonResponse(result)
            topics = topics | _topics

        paginator = Paginator(topics, 2)
        cur_page = int(request.GET.get('page', 1))
        page = paginator.page(cur_page)
        return render(request, 'index.html', locals())


def message_topic(request, t_id=None):
    if request.method != 'POST':
        result = {'code': 634, 'error': "不是POST请求"}
        return JsonResponse(result)
    username = request.session['username']
    if not username:
        result = {'code': 635, 'error': "对不起！您还没有登录"}
        return JsonResponse(result)
    try:
        user = UserProfile.objects.get(username=username)
    except:
        result = {'code': 636, 'error': "没有该用户"}
        return JsonResponse(result)
    try:
        topic = IntroductionInfo.objects.get(id=t_id)
    except:
        result = {'code': 637, 'error': "没有该文章"}
        return JsonResponse(result)
    reply = request.POST.get('reply')
    if reply is None:
        result = {'code': 638, 'error': '发表（回复）异常'}
        return JsonResponse(result)
    if reply == '0':
        message = request.POST.get('message')
        if not message:
            result = {'code': 639, 'error': "没有填写评论"}
            return JsonResponse(result)
        msg = IntroductionMessage.objects.create(message=message, topicid_id=topic.id, userid_id=user.id)
        msg.save()
        result = {'code': 200, 'error': '发表成功'}
        return JsonResponse(result)
    else:
        reply_message = request.POST.get('reply_message')
        if not reply_message:
            result = {'code': 640, 'error': '没有填写回复'}
            return JsonResponse(result)
        msg = IntroductionMessage.objects.create(message=reply_message, topicid_id=topic.id, userid_id=user.id,
                                                 parent_id=reply)
        msg.save()
        result = {'code': 200, 'error': '回复成功'}
        return JsonResponse(result)

# def check_login(request, username=None):
#     # 检查用户是否登录,暂用cookies,合并项目后改为token检验
#     _username = request.COOKIES.get('username')
#     if _username == username:
#         return True
#     else:
#         return False
