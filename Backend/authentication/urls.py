from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('checkstatus/',views.checkstatus, name='checkstatus'),
    # path('register/',views.register, name='register'),
    path('setcreds/<str:db_type>/',views.setcreds, name='setcreds'),
]
