from django.db import models
from tastypie.resources import ModelResource
from movies.models import Movie


# Create your models here.
class MovieResource(ModelResource):  # 电影资源类
    class Meta:  # 定义元类属性，用以定义该api资源类的各元属性
        queryset = Movie.objects.all()  # 电影资源列表，返回给前端页面的数据资源
        resource_name = 'movies'  # 资源名称，标记该api资源名称，方便请求
        excludes = ['date_created']  # 资源排除列表,从queryset排除掉的属性键值对列表
