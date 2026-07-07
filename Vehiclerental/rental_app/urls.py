# from django.urls import path
# from rental_app.views import *
# from django.conf import settings
# from django.conf.urls.static import static


# urlpatterns =[
#     path('signup',SignupView.as_view(),name='signup'),
#     path('home',HomePageView.as_view(),name='homepage')
# ]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from rental_app.views import *
from django.conf import settings
from django.conf.urls.static import static
from rental_app import views

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('home', HomePageView.as_view(), name='homepage'),
    path('explore_vehicle',ExploreVehicleView.as_view(),name='explore_vehicle'),
    path('carlist',CarListView.as_view(),name='carlist'),
    path('bikelist',BikeListView.as_view(),name='bikelist'),
    path('scooterlist',ScooterListView.as_view(),name='scooterlist'),
    path('vanlist',VanListView.as_view(),name='vanlist'),
    path('vehicle/<int:pk>/', VehicleDetailView.as_view(), name='vehicle_detail'),
    path("profile/", ProfileCreateView.as_view(), name='profile'),
    path( "booking/<int:pk>/",BookingCreateView.as_view(),name="booking"),
    path("my-bookings/", MyBookingListView.as_view(), name="my-bookings"),
    path("cancel-booking/<int:pk>/", cancel_booking, name="cancel_booking"),
    path("return-booking/<int:pk>/",return_booking,name="return-booking"),
    path("payment/<int:booking_id>/",views.create_payment,name="create_payment"),
    path("payment-success/",views.payment_success,name="payment_success"),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
    

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)