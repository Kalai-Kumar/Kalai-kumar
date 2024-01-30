from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.loginpage,name='login'),
    path('signup/',views.signuppage,name='signup'),
    path('room/',views.roomview,name='room'),
    path('<str:room_name>/<str:username>/', views.MessageView, name='room'),
    path('logout/',views.logoutpage,name='logout')
]