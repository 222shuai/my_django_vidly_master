# my_django_vidly

#### 介绍
django实例练习之vidly

"""本次实践基于mosh的python+django web快速入门教程"""
1.路由功能(urls)
    1.为了在模板或其他组件能勾引用url模块，url的列表应当具有一定规范：
        app_name = 'movies'  # 设置app名称方便被引用
        # /movies/1
        urlpatterns = [
            path('', views.index, name='index'),
            path('<int:movie_id>', views.detail, name='detail')
        ]
2.admin(管理员)
3.models(模型)
4.views(视图)
    1.访问的数据库对象不存在的处理实例：
        from django.shortcuts import render, get_object_or_404
        def detail(request, movie_id):
            # get_object_or_404方法获取指定数据表对象，不存在自动为404页面
            movie = get_object_or_404(Movie, pk=movie_id)
            return render(request, 'movies/detail.html', {'movie': movie})
    2.为页面列表增加超链接：
        1.<a href="/movies/{{ movie.id }}">{{ movie.title }}</a>
        2.但这并不是一个较好的方法，如果页面的系统url结构发生更改,因此可以采用以下方式：
            <a href="{% url 'movies:detail' movie.id %}">{{ movie.title }}</a>
            这种方法的前提是在url中有相应的设置app_name='movies'以及name='detail'的path。
            这种a标签会自动从url列表中搜索movies下的detail的url，并且加上movie.id，构造成我们的目标url
            在系统url前置结构改变时，在movies下的所有url仍能正常工作。
    3.为项目设置主页，否则在访问根url时会出现默认的错误提示页面
        1.类似于其他app的views.py(视图)编写，返回对应的页面template(模板)即可，需要自行先在项目主目录(vidly)
            文件夹下新建一个views.py文件
        2.注意由于默认的主目录vidly不是一个app，我们应当将主页模板放在主项目的template目录下，django会自动搜索。
            如果一定要将其模板文件放在vidly下，那么要在settings.py中的INSTALLED_APPS列表中像其他app一样配
            置上vidly，否则会找不到模板文件。

5.template(模板)
6.其他：
    1.Django项目构建API(两种API框架可选)：
        1.django-tastypie 0.14.2 --> pip install django-tastypie
            简介：属于beta版本，但实际上诞生于2010年，并且已经在多个网站被用于生产
        2.djangorestframework 3.9.0 --> pip install djangorestframework
            简介：功能更加丰富，可能用于大型企业应用程序中，也因此比上一个框架显得复杂性更高(不利于新手学习)
        3.安装好合适的api框架后(本次采用第一种)，构建一个新的名为api的app，专门用于处理总项目的api：
            python manage.py startapp api
        4.在项目settings.py中配置INSTALLED_APPS列表，增加api app：
            'api.apps.ApiConfig',  # api app
        5.在新建的api app中定义项目api相关内容，如在models.py中定义电影资源类以返回电影资源数据给前端页面:
            1.调用api框架：from tastypie.resources import ModelResource
            2.自定义api资源类，继承api框架的ModelResource类：
                class MovieResource(ModelResource):  # 电影资源类
                    class Meta: # 定义元类属性，用以定义该api资源类的各元属性
                        queryset = Movie.objects.all()  # 电影资源列表，返回给前端页面的数据资源
                        resource_name = 'movies'  # 资源名称，标记该api资源名称，方便请求
                1.常见api元属性举例：
                    1.queryset = Movie.objects.all()  # 电影资源列表，返回给前端页面的数据资源
                    2.resource_name = 'movies'  # 资源名称，标记该api资源名称，方便请求
                    3.excludes = ['date_created']  # 资源排除列表,从queryset排除掉的属性键值对列表
            3.配置路由规则匹配到该api接口：
                1.在主urls.py中导入相应api资源类：
                    from api.models import MovieResource
                2.实例化该资源类，方便动态路由匹配：
                    movie_resource = MovieResource()  # 实例化电影资源类
                3.添加对应路由规则：
                    path('api/', include(movie_resource.urls))  # api movie_resource
                4.启动项目，测试api访问结果：/api/movies
    2.部署django项目到云平台(类似于github平台)
        1.一些常见的云平台(除github外)：
            Heroku、Google Cloud、亚马逊网络服务、AWS、Microsoft Azure等，不同平台部署的步骤略有不同。
        2.本次练习展示部署到Heroku的步骤：
            1.访问Heroku官网：https://www.heroku.com/
            2.注册登录
            3.安装好必备的工具(git 和 Heroku CLI(Heroku命令行工具))并检查环境变量：
                1.官网：https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli
                2.验证安装成功
                    heroku --version结果出错一般是环境变量配置问题，手动配置后可能需要重启电脑后才能恢复正常
                    >>E:\Python\pythonProject\my_django_vidly>git --version
                    git version 2.34.1.windows.1

                    >>E:\Python\pythonProject\my_django_vidly>heroku --version
                    heroku/7.53.0 win32-x64 node-v12.21.0
            4.安装python包gunicorn: pip install gunicorn
                Gunicorn是一个unix上被广泛使用的高性能的Python WSGI UNIX HTTP Server。和大多数的web框架兼容，
                并具有实现简单，轻量级，高性能等特点。
                1.简书 gunicorn详解：https://www.jianshu.com/p/69e75fc3e08e
                2.gunicorn 文档：https://docs.gunicorn.org/en/stable/
                ......
            5.准备相关配置文件
                1.Procfile：在根目录(与manage.py同级)新建一个文件Procfile(heroku用来启动应用程序的特殊文件):
                    编写：web: gunicorn vidly.wsgi
                    意义：告诉heroku该进程是一个用于Web应用程序的进程，并且要开始该进程需要加载gunicorn web服务器
                        和vidly目录下的wsgi文件
                2.static：
                    1.同上，在根目录建立static文件夹。包含项目部署的静态文件，例如css、JavaScript、图片等资源文件
                        目前没有自定义使用静态文件，但是项目默认使用了admin管理界面及其相关的静态资源。
                    2.在settings.py中STATIC_URL后如下定义：
                        STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # 静态文件资源根目录
                    3.同步项目静态资源到自定义的static目录：python manage.py collectstatic
                        执行该命令会将项目用到的admin管理界面的相关静态资源同步到新建的static文件夹中。
                    4.为了在heroku中提供静态文件，我们还应安装一个名为white noise的软件包：pip install whitenoise
                      去PyPI社区查找whitenoise查阅其说明文档：https://whitenoise.evans.io/en/stable/django.html
                      可以学习如何使用其为django项目服务
            6.建立我们的项目仓库(git仓库，好的存储库是一个包含我们源代码及其所有版本的数据库)
                我们还需要在heroku设立一个git镜像仓库，方便同步我们的更新到heroku，此处涉及git的相关操作
                1.项目git仓库初始化(第一次时要执行)：git init
                2.添加在当前目录和所有子目录中所有修改后的文件，放在下一次提交中：git add .
                3.提交操作，尽量带有提示信息，展示进行了哪些修改，方便后期检查：git commit -m "Initial commit"
                ......后期更新仓库......
            7.heroku配置，使用Heroku CLI创建heroku应用
                1.登录(根据提示可能需要跳转到浏览器登录)：heroku login
                2.创建新的heroku应用：heroku create heroku-app-name
                  得到的提示信息包含：
                    1.app的名称(默认是随机的也可自定义)，
                    2.app访问地址(点击访问是一个heroku默认的欢迎界面，由于还未部署项目)
                    3.app的heroku仓库地址(需要与git仓库建立关联)：
                        推送本地git仓库内容到heroku应用镜像仓库主分支：git push heroku master
                        关于报错：
                            ! [remote rejected] master -> master (pre-receive hook declined)
                            error: failed to push some refs to
                        解决参考：https://blog.csdn.net/weixin_44184990/article/details/100121154
                        #TODO：暂未解决
                        其它云平台使用git的流程类似

