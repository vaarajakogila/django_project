from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('forgotpassword/', views.forgotpassword, name='forgot_password'),
    path('changepassword/', views.changepassword, name='password_change'),
    # path('resetpassword/<str:token>/', views.resetpassword, name='reset_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
