from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'login'

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^home/', views.postlogin, name='logging'),
    url(r'^useradmin/', views.admin, name='admin'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^assign/', views.expertassign, name='assign_expert'),
    url(r'^addexpert/', views.addexpert, name='addexpert'),
    url(r'^postaddexpert/', views.postaddexpert, name='postaddexpert'),
]