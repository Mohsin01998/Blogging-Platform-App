from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from smtplib import SMTPServerDisconnected


urlpatterns = [

    path('accounts/', include('django.contrib.auth.urls')),
    path('',views.login_page,name=''),
    path('home',views.home,name='home'),
    path('login',views.login_page,name='login'),
    path('register',views.register,name='register'),
    path('about_us', views.about_us, name='about_us'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('logout',views.logout_view,name='logout'),
    path('token',views.token,name='token'),
    path('success',views.success,name='success'),
    path('verify/<auth_token>',views.verify,name='verify'),
    path('error',views.error,name='error'),
    path('post_create',views.post_create,name='post_create'),
    path('post/<int:post_id>/edit/',views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/',views.post_delete,name='post_delete'),
    path('add/<int:post_id>/comment/',views.add_comment,name='add_comment'),
    # Password Reset
    # _________________
    path('reset_password/',

         auth_views.PasswordResetView.as_view(
             template_name="password_reset.html",
             email_template_name="password_reset_email.html",
             subject_template_name="password_reset_subject.txt",
             success_url=reverse_lazy('password_reset_done')
         ),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="password_reset_sent.html"
         ),
         name="password_reset_done"),

    path('reset_password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="password_reset_form.html",
             success_url=reverse_lazy('password_reset_complete')
         ),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="password_reset_complete.html"
         ),
         name="password_reset_complete"),

]

