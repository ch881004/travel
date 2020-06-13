from django.shortcuts import render


def index(request):
    username = request.session.get('username')
    return render(request, 'index.html', locals())
