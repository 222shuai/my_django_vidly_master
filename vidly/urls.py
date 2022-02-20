"""vidly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.models import MovieResource
from . import views

movie_resource = MovieResource()  # 实例化电影资源类

urlpatterns = [
    path('', views.home),  # 项目主页
    path('admin/', admin.site.urls),  # 管理员模块
    path('movies/', include('movies.urls')),  # app movies
    path('api/', include(movie_resource.urls))  # api movie_resource
]
