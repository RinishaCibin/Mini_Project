from django.contrib import admin
from rental_app.models import *

# Register your models here.

# admin.site.register(User)
admin.site.register(Vehicle)
# admin.site.register(Booking)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "booking_number",
        "user",
        "vehicle",
        "pickup_date",
        "return_date",
        "booking_amount",
        "late_fee",
        "final_amount",
        "payment_status",
        "booking_status",
        
    )

    list_filter = (
        "booking_status",
        "pickup_date",
    )

    search_fields = (
        "booking_number",
        "user__username",
        "vehicle__vehicle_name",
    )
 

    def save_model(self, request, obj, form, change):

        super().save_model(request, obj, form, change)

        if obj.booking_status == "Approved":
            obj.vehicle.status = "Booked"

        elif obj.booking_status in ["Completed", "Cancelled"]:
            obj.vehicle.status = "Available"

        obj.vehicle.save()

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["booking", "amount", "payment_status", "payment_date"]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["user", "vehicle", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["user__username", "vehicle__vehicle_name"]


admin.site.register(Notification)

admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
