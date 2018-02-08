from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'frontend'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_form, name='upload'),
    path('<int:imagefile_id>', views.result, name='result'),
]
