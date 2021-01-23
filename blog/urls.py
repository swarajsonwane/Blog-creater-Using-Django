from django.conf.urls import url
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [

path('login/', views.user_login, name='login'),
#path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    url(r'^(?P<pk>[0-9]+)/share/',views.post_share, name='post_share'),
    url(r'^(?P<pk>[0-9]+)/$',views.post_detail,name='post_detail'),
    path('search/', views.post_search, name='post_search'),

]
# path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail,name='post_detail'),
