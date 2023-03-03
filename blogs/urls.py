from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login_page,name='login'),
    path('register',views.register,name='register'),
    path('about_us', views.about_us, name='about_us'),
    path('blogs', views.blogs, name='blogs'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('logout',views.logout_view,name='logout'),

]
