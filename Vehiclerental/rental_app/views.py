from django.shortcuts import render,redirect
from rental_app.forms import*
from django.views.generic import *
from django.views import View
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from rental_app.models import *
from django.views.generic import ListView
import uuid
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from datetime import date
from django.utils import timezone
from decimal import Decimal
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse





client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

# Create your views here.

class SignupView(CreateView):
    template_name="signup.html"
    form_class=SignupForm
    success_url=reverse_lazy("signin")

# class SigninView(FormView):
#     template_name="signin.html"
#     form_class=SigninForm
#     def post(self, request):
#         form_data=SigninForm(data=request.POST)
#         if form_data.is_valid():
#             uname=form_data.cleaned_data.get('username')
#             pswd=form_data.cleaned_data.get('password')
#             user=authenticate(request,username=uname,password=pswd)
#             if user:
#                 login(request,user)
#                 if user.is_superuser==False:
#                     return redirect('homepage')
#                 elif user.is_superuser:
#                     return redirect(reverse('admin:index'))
#                 else:
#                     messages.error(request,"Invalid Username or Password")
#                     return redirect('signin')
#             return render(request,"signin.html",{"form":form_data})


class SigninView(FormView):
    template_name="signin.html"
    form_class=SigninForm
    def post(self, request):
        form_data=SigninForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                if user.is_superuser:
                    return redirect(reverse('admin:index'))

                if User_profile.objects.filter(user=user).exists():
                    return redirect('homepage')
                else:
                    return redirect('profile')

class HomePageView(ListView):
    model = Vehicle                 
    template_name = "home.html"
    context_object_name = "vehicles"
    def get_queryset(self):
        return Vehicle.objects.all()[:4]

class ExploreVehicleView(ListView):
    model = Vehicle
    template_name = "Explore_vehicles.html"
    context_object_name = "vehicles"

class CarListView(ListView):
    model = Vehicle
    template_name = "carlist.html"
    context_object_name = "vehicles"
    def get_queryset(self):
        return Vehicle.objects.filter(vehicle_type='Car')
    
class BikeListView(ListView):
    model = Vehicle
    template_name = "bikelist.html"
    context_object_name = "vehicles"
    def get_queryset(self):
        return Vehicle.objects.filter(vehicle_type='Bike')
    
class ScooterListView(ListView):
    model = Vehicle
    template_name = "scooterlist.html"
    context_object_name = "vehicles"
    def get_queryset(self):
        return Vehicle.objects.filter(vehicle_type='Scooter')
    
class VanListView(ListView):
    model = Vehicle
    template_name = "vanlist.html"
    context_object_name = "vehicles"
    def get_queryset(self):
        return Vehicle.objects.filter(vehicle_type='van')
    

class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = "vehicle_detail.html"
    context_object_name = "vehicle"

class ProfileCreateView(CreateView):
    model = User_profile
    form_class = UserProfileForm
    template_name = "userProfile.html"
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
  
    
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "booking.html"
    success_url = reverse_lazy("my-bookings")

    def form_valid(self, form):
        vehicle = get_object_or_404(Vehicle, pk=self.kwargs["pk"])

        # Check if vehicle is under maintenance
        if vehicle.status == "Maintenance":
            messages.error(
                self.request,
                "This vehicle is currently under maintenance."
            )
            return redirect("vehicle_detail", pk=vehicle.pk)

        # Assign user and vehicle
        form.instance.user = self.request.user
        form.instance.vehicle = vehicle
        form.instance.booking_number = str(uuid.uuid4()).split("-")[0]

        pickup_date = form.cleaned_data.get("pickup_date")
        return_date = form.cleaned_data.get("return_date")

        # Check for overlapping bookings
        existing_booking = Booking.objects.filter(
            vehicle=vehicle,
            booking_status__in=["Pending", "Approved"]
        ).filter(
            Q(pickup_date__lte=return_date) &
            Q(return_date__gte=pickup_date)
        )

        if existing_booking.exists():
            form.add_error(
                None,
                "This vehicle is already booked for the selected dates."
            )
            return self.form_invalid(form)

        # Calculate booking amount
        if pickup_date and return_date:
            duration = (return_date - pickup_date).days

            if duration <= 0:
                duration = 1

            amount = duration * vehicle.rent_per_day
            form.instance.booking_amount = amount
            form.instance.final_amount = amount
        else:
            form.instance.booking_amount = 0
            form.instance.final_amount = 0

        # Save the booking
        return super().form_valid(form)


# 2. Enforce login when viewing the bookings list
class MyBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "my_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        # This guarantees you only pull bookings belonging to the logged-in user
        return Booking.objects.filter(user=self.request.user).order_by("-created_at")
    


def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    booking.booking_status = "Cancelled"
    booking.save()

    return redirect("my-bookings")



def return_booking(request, pk):

    booking = get_object_or_404(Booking, pk=pk)

    if request.method == "POST":

        form = ReturnBookingForm(request.POST, instance=booking)

        if form.is_valid():
            print("Expected:", booking.return_date)
            print("Actual:", booking.actual_return_date)

            booking = form.save(commit=False)

            # Late Fee Per Day
            late_fee_per_day = Decimal("500")

            # Late days
            if booking.actual_return_date > booking.return_date:

                late_days = (
                    booking.actual_return_date - booking.return_date
                ).days

                booking.late_fee = late_days * late_fee_per_day

            else:

                booking.late_fee = Decimal("0")

            # Update Total Amount
            booking.final_amount = booking.booking_amount + booking.late_fee
            booking.booking_status = "Completed"
            booking.save()

            # Change Status
            booking.booking_status = "Completed"

            booking.save()

            return redirect("my-bookings")

    else:

        form = ReturnBookingForm(instance=booking)

    return render(
        request,
        "return_booking.html",
        {
            "form": form,
            "booking": booking,
        },
    )



@login_required
def create_payment(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    # Already paid ആണെങ്കിൽ വീണ്ടും payment വേണ്ട
    if booking.payment_status == "Paid":
        messages.info(request, "Payment already completed.")
        return redirect("my-bookings")

    amount = 100

    # 🔽 ഈ ഭാഗം ഇവിടെ ചേർക്കുക
    print("KEY ID:", settings.RAZORPAY_KEY_ID)
    print("SECRET:", settings.RAZORPAY_KEY_SECRET)

    try:
        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
        })
        print("ORDER CREATED:", razorpay_order)

    except Exception as e:
        print("RAZORPAY ERROR:", e)
        return HttpResponse(f"Error: {e}")

    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            "amount": booking.final_amount,
            "razorpay_order_id": razorpay_order["id"],
        }
    )

    if not created:
        payment.amount = booking.final_amount
        payment.razorpay_order_id = razorpay_order["id"]
        payment.save()

    context = {
        "booking": booking,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "order_id": razorpay_order["id"],
    }

    return render(request, "payment.html", context)
    






@csrf_exempt
@login_required
def verify_payment(request):
    if request.method == "POST":
        order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")
        signature = request.POST.get("razorpay_signature")

        payment = Payment.objects.get(razorpay_order_id=order_id)

        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.payment_status = "Success"
        payment.payment_date = timezone.now()
        payment.save()

        booking = payment.booking
        booking.payment_status = "Paid"
        booking.save()

        return JsonResponse({"status": "success"})


def payment_success(request):
    return render(request,"payment_success.html")