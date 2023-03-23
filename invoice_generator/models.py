from django.db import models

class Ride(models.Model):
    day = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    customer = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    pick_up_address = models.CharField(max_length=200)
    drop_off_address = models.CharField(max_length=200)
    driver_name = models.CharField(max_length=100)
    driver_badge = models.CharField(max_length=20)
    vehicle_reg = models.CharField(max_length=20)
    license_vehicle = models.CharField(max_length=20)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50)
    date_booked = models.DateField()
    time_booked = models.TimeField()
    status = models.CharField(max_length=50)
    job_source = models.CharField(max_length=100)


# Create your models here.
