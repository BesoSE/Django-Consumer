from django.urls import path, re_path as url

from notifications import views


urlpatterns = [
    url(r'^user/?(?P<id>[0-9]+)?$', views.UserDetailView.as_view(), name='user'), 
    url(r'^users/$', views.UserListView.as_view(), name='user'), 
    path("", views.index, name="index"),
]