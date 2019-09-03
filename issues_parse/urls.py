from django.urls import path

from .views import UserListView, WorkLogList

urlpatterns = (
    path('', UserListView.as_view(), name='index'),
    path('work-logs/<str:gitlab_username>', WorkLogList.as_view(),
         name='get_time_track'),
)
