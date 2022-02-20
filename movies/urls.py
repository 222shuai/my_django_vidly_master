from django.urls import path
from . import views

app_name = 'movies'  # 设置app名称方便被引用
# /movies/1
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>', views.detail, name='detail')
]
