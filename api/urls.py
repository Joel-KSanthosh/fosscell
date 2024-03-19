from django.urls import path
from . import views

urlpatterns = [
    path('user-activity/',views.UserActivityPostView.as_view(),name='send_activity'),
    path('user-activity/<str:pk>/',views.UserActivityGetView.as_view(),name='activity'),
    path('activity-table/',views.ActivityTableView.as_view(),name='activity-table'), 
    path('edit-activity/<str:pk>/',views.UserActivityPatchDeleteView.as_view(),name='edit-activity'),
    path('login/',views.LoginApiView.as_view(),name='login'),
    path('register/',views.RegisterApiView.as_view(),name='register'),
    path('activity-approval/<str:pk>/',views.AdminApprovalView.as_view(),name='approve-activity'),
    
]
