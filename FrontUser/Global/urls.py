from . import views 
from django.urls import path


urlpatterns = [
    path('accounts/register',views.register,name='global-register'),
]