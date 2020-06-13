from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import UserProfile


# Create your views here.
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usertype = request.POST.get('usertype')
        UserProfile.objects.create(username=username, password=password, usertype=usertype)
        # token = make_token(username)
        # result = {'code': 200, 'token': token.decode(), 'username': username}
        html = """注册成功!<a href='login'>登录</a>"""
        resp = HttpResponse(html)
        # resp.set_cookie('username', username)
        request.session['username'] = username
        # return render(request, 'login.html', result)
        return resp


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = UserProfile.objects.get(username=username)
        except:
            return HttpResponse('用户不存在')
        if user.password == password:
            html = """登录成功!<div><a href='/v1/topics/{}'>我的游记</a></div>""".format(username)
            html += """<div><a href='/v1/topics'>全部游记</a></div>"""
            html += """<div><a href='/v1/topics/{}/add'>发布游记</a></div>""".format(username)
            resp = HttpResponse(html)
            # resp.set_cookie('username', username)
            request.session['username'] = username
            # token = make_token(username)
            # result = {'code': 200, 'token': token.decode(), 'username': username}
            return resp
        else:
            return HttpResponse('密码错误')


def logout(request):
    del request.session['username']
    return render(request, 'index.html', locals())


def make_token(username, expire=3600 * 24):
    import jwt, time
    key = '123456'
    now = time.time()
    payload = {'username': username, 'exp': int(now + expire)}
    return jwt.encode(payload, key, algorithm='HS256')
