from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('home/', views.home, name="home"),
    path('profile/',views.profile,name='profile'),
    path('proupdate/',views.proupdate,name='proupdate'),
    path('logout/',views.logoutv,name='logout'),
    path('checkdisease/',views.checkdisease,name='checkdisease'),
    path('fileupload/',views.checkdisease,name='fileupload'),
    path('xray/',views.xrayupload,name='xray'),
    
]
