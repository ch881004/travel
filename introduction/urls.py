from django.conf.urls import url
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/v1/topics/
    # 旅游攻略主页
    url(r'^$', views.get_all_list, name='get_all_list'),
    # http://127.0.0.1:8000/v1/topics/<username>
    # 用户查看自己发布的游记
    url(r'^/(?P<username>[\w]+)$', views.get_user_list, name='get_user_list'),
    # http://127.0.0.1:8000/v1/topics/<username>/submit
    # 用户发布游记
    url(r'^/(?P<username>[\w]+)/add$', views.add_topic, name='add_topic'),
    # 用户修改游记
    url(r'^/(?P<username>[\w]+)/mod/(?P<t_id>[\d]+)$', views.mod_topic, name='mod_topic'),
    # 用户修改游记
    url(r'^/(?P<username>[\w]+)/del/(?P<t_id>[\d]+)$', views.del_topic, name='del_topic'),
    # 攻略详情页
    url(r'^/detail/(?P<t_id>[\d]+)$', views.detail_topic, name='detail_topic'),
]
