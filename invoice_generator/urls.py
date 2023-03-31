from django.urls import path
from .views import upload_csv
from .views import log_ride
from .views import view_bookings
from .views import home
from .views import delete_row
from .views import edit_row
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name='home'),
    path('create_invoice/', upload_csv, name='upload_csv'),
    path('input_booking_data/', log_ride, name='log_ride'),
    path('view_booking_data/', view_bookings, name='view_bookings'),
    path('delete/<str:id>/', delete_row, name='del_row'),
    path('edit/<str:id>/', edit_row, name='edit_row'),
]

urlpatterns += staticfiles_urlpatterns()