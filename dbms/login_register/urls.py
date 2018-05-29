from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('share/', views.share, name='share'),
    path('fix_p', views.fix_personal_information, name='fix_p'),
    path('fix_e', views.fix_educational_information, name='fix_e'),
    path('fix_w', views.fix_work_information, name='fix_w'),
    path('show_logs', views.show_logs, name='show_logs'),
    path('show_p', views.show_personal_information, name='show_p'),
    path('add_log', views.add_log, name='add_log'),
    path('add_friend', views.add_friend, name='add_friend'),
    path('show_friends', views.show_friends, name='show_friends'),
    path('add_reply', views.add_reply, name='add_reply'),
    path('share_log', views.share_log, name='share_log'),
    path('search_friend', views.search_friend, name='search_friend'),
    path('delete_friend', views.delete_friend, name='delete_friend'),
    path('delete_group', views.delete_group, name='delete_group'),
    path('fix_g', views.update_group, name='fix_g'),
]