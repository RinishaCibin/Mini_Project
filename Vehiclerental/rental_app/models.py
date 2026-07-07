from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.
class User_profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone=models.CharField(max_length=15)
    address=models.TextField()
    profile_picture=models.ImageField(upload_to='user_profile_pictures/',blank=True,null=True)
    driving_license = models.ImageField(upload_to='licenses/',blank=True,null=True)
    license_number = models.CharField( max_length=50,blank=True, null=True)
    license_expiry_date = models.DateField(blank=True,null=True)
    is_license_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    

    
# class Vehicle(models.Model):
#     STATUS_CHOICES = ( ('Available', 'Available'),('Booked', 'Booked'),('Maintenance', 'Maintenance'),)
#     VEHICLE_TYPES = (('Car', 'Car'),('Bike', 'Bike'),('Scooter', 'Scooter'),('van','van'))
#     FUEL_TYPES = (('Petrol', 'Petrol'),('Diesel', 'Diesel'),('Electric', 'Electric'),('Hybrid', 'Hybrid'),)
#     vehicle_name = models.CharField(max_length=100)
#     brand = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#     year = models.PositiveIntegerField()
#     registration_number = models.CharField(max_length=50,unique=True)
#     vehicle_type = models.CharField(max_length=50,choices=VEHICLE_TYPES)
#     fuel_type = models.CharField(max_length=50,choices=FUEL_TYPES)
#     seating_capacity = models.PositiveIntegerField(default=2)
#     rent_per_day = models.DecimalField(max_digits=10,decimal_places=2)
#     image = models.ImageField(upload_to='vehicles/')
#     description = models.TextField()
#     status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Available')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.vehicle_name} ({self.registration_number})"

    
class Vehicle(models.Model):
    STATUS_CHOICES =  (
    ("Available", "Available"),
    ("Maintenance", "Maintenance"),
)
    VEHICLE_TYPES = (('Car', 'Car'),('Bike', 'Bike'),('Scooter', 'Scooter'),('van','van'))
    FUEL_TYPES = (('Petrol', 'Petrol'),('Diesel', 'Diesel'),('Electric', 'Electric'),('Hybrid', 'Hybrid'),)
    vehicle_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=50,unique=True)
    vehicle_type = models.CharField(max_length=50,choices=VEHICLE_TYPES)
    fuel_type = models.CharField(max_length=50,choices=FUEL_TYPES)
    seating_capacity = models.PositiveIntegerField(default=2)
    rent_per_day = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='vehicles/')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Available")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_name} ({self.registration_number})"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    BOOKING_STATUS = (('Pending', 'Pending'),('Approved', 'Approved'),('Completed', 'Completed'),('Cancelled', 'Cancelled'),)
    PAYMENT_STATUS = (('Pending', 'Pending'),('Paid', 'Paid'),)
    pickup_location = models.CharField(max_length=255)
    pickup_date = models.DateField()
    return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
   

    # Return സമയത്ത് calculate ചെയ്യുന്ന late fee
    late_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    booking_amount = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    booking_status = models.CharField(max_length=20,choices=BOOKING_STATUS,default='Pending')
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default='Pending'
)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    booking_number = models.CharField( max_length=20,unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle.vehicle_name}"
         
    

  
    
class Payment(models.Model):
    PAYMENT_STATUS = (('Pending', 'Pending'),('Success', 'Success'),('Failed', 'Failed'),('Refunded', 'Refunded'),)
    booking = models.OneToOneField(Booking,on_delete=models.CASCADE)
    currency = models.CharField(max_length=10,default='INR')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    refund_date = models.DateTimeField(null=True, blank=True)
    refund_reason = models.TextField(blank=True)
    # remarks = models.TextField(blank=True,null=True)
    razorpay_order_id = models.CharField(max_length=100,unique=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_signature = models.CharField(max_length=255,blank=True,null=True)
    payment_method = models.CharField(max_length=50,blank=True,null=True)
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default='Pending')
    payment_date = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField( auto_now_add=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.razorpay_order_id
    
# class Feedback(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         unique_together = ('user', 'vehicle')
#     def __str__(self):
#         return f"{self.user.username} - {self.vehicle.vehicle_name}"











    













