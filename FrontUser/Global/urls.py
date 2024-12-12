from . import views 
from django.urls import path


urlpatterns = [
    path('accounts/register',views.register,name='global-register'),
    path('accounts/login',views.login,name='global-login'),
]