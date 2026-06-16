from django.urls import path
from rental_app.views import *

urlpatterns =[
    path('signup',SignupView.as_view(),name='signup'),
    path('home',HomePageView.as_view(),name='home')
]



