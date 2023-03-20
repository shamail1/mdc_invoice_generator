from django.urls import path
from .views import upload_csv
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', upload_csv, name='upload_csv'),
]

urlpatterns += staticfiles_urlpatterns()