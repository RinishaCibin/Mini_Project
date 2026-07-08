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
    
# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     BOOKING_STATUS = (('Pending', 'Pending'),('Approved', 'Approved'),('Completed', 'Completed'),('Cancelled', 'Cancelled'),)
#     PAYMENT_STATUS = (('Pending', 'Pending'),('Paid', 'Paid'),)
#     # pickup_location = models.CharField(max_length=255)
#     PICKUP_LOCATIONS = [
#     ("Kochi", "Kochi"),
#     ("Thrissur", "Thrissur"),
#     ("Kozhikode", "Kozhikode"),
#     ("Kannur", "Kannur"),
#     ("Thiruvananthapuram", "Thiruvananthapuram"),
# ]

# class Booking(models.Model):
#     pickup_location = models.CharField(
#         max_length=100,
#         choices=PICKUP_LOCATIONS)

#     pickup_date = models.DateField()
#     return_date = models.DateField()
#     actual_return_date = models.DateField(blank=True, null=True)
   

#     # Return സമയത്ത് calculate ചെയ്യുന്ന late fee
#     late_fee = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=0
#     )
#     final_amount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=0
#     )

#     booking_amount = models.DecimalField(max_digits=10,decimal_places=2, default=0)
#     booking_status = models.CharField(max_length=20,choices=BOOKING_STATUS,default='Pending')
#     payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default='Pending'
# )

#     notes = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     booking_number = models.CharField( max_length=20,unique=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.vehicle.vehicle_name}"


class Booking(models.Model):

    BOOKING_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )

    PICKUP_LOCATIONS = [
        ("Kochi", "Kochi"),
        ("Thrissur", "Thrissur"),
        ("Kozhikode", "Kozhikode"),
        ("Kannur", "Kannur"),
        ("Thiruvananthapuram", "Thiruvananthapuram"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    pickup_location = models.CharField(
        max_length=100,
        choices=PICKUP_LOCATIONS
    )

    pickup_date = models.DateField()
    return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)

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

    booking_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    booking_status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default='Pending'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='Pending'
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    booking_number = models.CharField(max_length=20, unique=True)

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
    
class Feedback(models.Model):
    RATING_CHOICES = (
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)

    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle.vehicle_name} ({self.rating}⭐)"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class ChatRoom(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username
    
    
class ChatMessage(models.Model):

    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username} : {self.message[:25]}"











    













