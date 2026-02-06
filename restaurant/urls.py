from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
  # path(r'', views.home, name="home"),
  path(r'', views.main, name="home_page"),
  path(r'order', views.order_page, name="order_page"),
  path(r'submit', views.submit, name="submit"),

]