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
from django.contrib.auth.views import LogoutView

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
    path("feedback/<int:booking_id>/",FeedbackCreateView.as_view(),name="feedback"),
   path("notification/<int:pk>/",views.read_notification,name="read-notification"),
   path("notifications/",NotificationListView.as_view(), name="notifications"),
   path("chat/",views.chat_view,name="chat"),
   path("admin-send-message/<int:room_id>/",views.admin_send_message,name="admin-send-message"),
   path("send-message/",views.send_message,name="send-message"),
   path("admin-chats/",views.admin_chat_list,name="admin-chat-list"),
   path("admin-chat/<int:room_id>/",views.admin_chat_detail,name="admin-chat-detail"),
   path("admin-send-message/<int:room_id>/", views.admin_send_message,name="admin-send-message"),
   path("support-chat/", views.support_chat, name="support-chat"),
   path("logout/", views.user_logout, name="logout"),

    

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)