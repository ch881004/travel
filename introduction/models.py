from django.db import models

# Create your models here.

#
from user.models import UserProfile


# 文章、攻略表
class IntroductionInfo(models.Model):
    # 外键,用户表id
    userid = models.ForeignKey(UserProfile)
    title = models.CharField('文章标题', max_length=30)
    shortinfo = models.CharField('文章简介', max_length=30)
    info = models.TextField('文章内容')
    location = models.CharField('地理位置', max_length=10)
    image = models.ImageField('游记图片', upload_to='introduction/')

    create_time = models.DateTimeField('发布时间', auto_now_add=True)
    mod_time = models.DateTimeField('修改时间', auto_now=True)
    see_count = models.IntegerField('浏览次数', default=0)
    # 设置伪删除False
    is_show = models.BooleanField('显示', default=True)


# 文章关键字表,与上表是一对一关系
class IntroductionKeyWord(models.Model):
    # 外键,关联文章、攻略表
    titleid = models.ForeignKey(IntroductionInfo)
    keywords = models.CharField('文章关键字列表', max_length=50)
    is_show = models.BooleanField('显示', default=True)
