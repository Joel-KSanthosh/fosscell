from fosscell.views import institutionview,Fossview,Membersview,combined_data_view,LoginApiView,CombinedDataView,Approval,Reject,Submit,combined_data_adminview
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt





urlpatterns = [
    path('institution/',institutionview),
    path('fossadvisor/',Fossview),
    path('members/',Membersview),
    path('preview/', combined_data_view),
    path('adminpreview/<str:uid>', combined_data_adminview),
    path('login/',LoginApiView.as_view(),name='login'),
    path('adminview/',CombinedDataView.as_view(),name='adminview'),
    path('approve/<str:uid>',Approval.as_view()),
    path('reject/<str:uid>',Reject.as_view()),
    path('submit/',Submit.as_view())
#     # path('upload-csv/', upload_csv, name='upload_csv'),
]