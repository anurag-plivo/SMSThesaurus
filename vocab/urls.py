from django.conf.urls import include
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Vocabulary, name="index"),
]
