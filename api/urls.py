from fosscell.views import institutionview,Fossview,Membersview,combined_data_view,LoginApiView,CombinedDataView
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt





urlpatterns = [
    path('institution/',institutionview),
    path('fossadvisor/',Fossview),
    path('members/',Membersview),
    path('preview/', combined_data_view),
    path('login/',LoginApiView.as_view(),name='login'),
    path('adminview/',CombinedDataView.as_view(),name='adminview'),
   
#     # path('upload-csv/', upload_csv, name='upload_csv'),
]