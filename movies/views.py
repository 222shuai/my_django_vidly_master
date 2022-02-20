from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Movie


# Create your views here.
def index(request):
    movies = Movie.objects.all()  # 获取所有电影，作为上下文数据返回给页面进行渲染
    return render(request, 'movies/index.html', {'movies': movies})  # 返回页面及上下文数据


def detail(request, movie_id):
    # get_object_or_404方法获取指定数据表对象，不存在自动为404页面
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})
