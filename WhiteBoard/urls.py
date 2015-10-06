from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('WhiteBoard.base.urls', namespace='base')),
	url(r'^', include('WhiteBoard.grades.urls', namespace='grades')),
]
