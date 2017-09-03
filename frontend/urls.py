from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.promo, name='promo'),
    url(r'^login/([0-9]*)', views.login, name='promo'),
    url(r'^editor/', views.editor, name='editor'),
    url(r'^weeks/([0-9]{0,2})', views.schedule, name='schedule'),
    url(r'^help/', views.help, name='help'),
    url(r'^switcher/([a-z_]*)', views.switcher, name='switcher'),
]

