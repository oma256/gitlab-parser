from django.urls import path

from .views import UserListView, TimeTrackList

urlpatterns = [
    path('', UserListView.as_view(), name='index'),
    path('get_time_track/<str:gitlab_username>', TimeTrackList.as_view(),
         name='get_time_track'),
]