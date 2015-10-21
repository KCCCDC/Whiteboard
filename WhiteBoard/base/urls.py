from django.conf.urls import patterns, url

from WhiteBoard.base import views

urlpatterns = patterns(
    '',
    url(r'^login/', views.login, name='login'),
    url(r'^auth/', views.auth, name='auth'),
    url(r'^/$', views.index, name='default'),
    url(r'^$', views.index, name='default'),
    url(r'^index/', views.index, name='index'),
    url(r'^invalidLogin', views.invalidLogin, name='invalidLogin'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^home', views.home, name='home'),
    url(r'^announcements', views.announcements, name='announcments'),
    url(r'^create_announcement', views.CreateAnnouncementView.as_view(),
        name='create_announcements'),
)
