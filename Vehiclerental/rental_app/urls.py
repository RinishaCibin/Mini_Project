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

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('home', HomePageView.as_view(), name='homepage'),
    path('explore_vehicle',ExploreVehicleView.as_view(),name='explore_vehicle'),
    path('carlist',CarListView.as_view(),name='carlist'),
    path('bikelist',BikeListView.as_view(),name='bikelist'),
    path('scooterlist',ScooterListView.as_view(),name='scooterlist'),
    path('vanlist',VanListView.as_view(),name='vanlist'),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)