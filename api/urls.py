from django.urls import path
from . import views

urlpatterns = [
    path('user-activity/',views.UserActivityView.as_view(),name='activity'),
    path('login/',views.LoginApiView.as_view(),name='login')
]
