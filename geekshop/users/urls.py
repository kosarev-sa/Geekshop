"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import LoginListView, Logout, ProfileFormView, RegisterListView

app_name = 'users'
urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('register/', RegisterListView.as_view(), name='register'),
    path('profile/', ProfileFormView.as_view(), name='profile'),
    path('logout/', Logout.as_view(), name='logout'),
    path('verify/<str:email>/<str:activation_key>/', RegisterListView.verify, name='verify'),

]
