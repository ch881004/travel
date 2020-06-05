from django.conf.urls import url
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/v1/topics/
    # 旅游攻略主页
    # url(r'^$', views.get_all_list),
    # http://127.0.0.1:8000/v1/topics/<username>
    # 用户查看自己发布的游记
    # url(r'^/(?P<username>[\w]+)$', views.get_list),
    # http://127.0.0.1:8000/v1/topics/<username>/submit
    # 用户发布游记
    url(r'^/(?P<username>[\w]+/submit)$', views.submit_topic),
]
