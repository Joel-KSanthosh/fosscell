from django.urls import path
from . import views
from fosscell.views import institutionview,Fossview,Membersview,combined_data_view,LoginApiView,CombinedDataView,Approval,Reject,Submit,combined_data_adminview
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('user-activity/',views.UserActivityPostView.as_view(),name='send_activity'),
    path('user-activity/<str:pk>/',views.UserActivityGetView.as_view(),name='activity'),
    path('activity-table/',views.ActivityTableView.as_view(),name='activity-table'), 
    path('edit-activity/<str:pk>/',views.UserActivityPatchDeleteView.as_view(),name='edit-activity'),
    path('login/',views.LoginApiView.as_view(),name='login'),
    path('register/',views.RegisterApiView.as_view(),name='register'),
    path('activity-approve/<str:pk>/',views.AdminApprove.as_view(),name='approve-activity'),
    path('activity-disapprove/<str:pk>/',views.AdminDisapprove.as_view(),name='disapprove-activity'),
    path('institution/',institutionview),
    path('fossadvisor/',Fossview),
    path('members/',Membersview),
    path('preview/', combined_data_view),
    path('adminpreview/<str:uid>', combined_data_adminview),
    path('adminview/',CombinedDataView.as_view(),name='adminview'),
    path('approve/<str:uid>',Approval.as_view()),
    path('reject/<str:uid>',Reject.as_view()),
    path('submit/',Submit.as_view())
]


