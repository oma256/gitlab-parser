from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('issues_parse.urls', 'issues_parse'),
         namespace='issues_parse'))
]
