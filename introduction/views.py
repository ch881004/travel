from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.
# 查看所有攻略
# def get_all_list(request):
#     # return render(request, 'topics.html')
#     return render(request, 'submittopic.html')
#
# def get_list(request, username):
#     # 查看用户个人发布的攻略
#     if request.method == 'GET':
#         # return render(request, 'user_topics.html')
#         return render(request, 'submittopic.html')

def submit_topic(request, username):
    print('我进来了')
    # if request.method == 'GET':
    return render(request, 'submittopic.html')
    # 用户提交攻略
    # elif request.method == 'POST':
    #     title = request.body['title']
    #     keyword = request.body['keyword']
    #     info = request.body['info']
    #     return render(request, {'title': title, 'keyword': keyword, 'info': info})
