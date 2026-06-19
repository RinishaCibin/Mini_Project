from django.urls import path
from rental_app.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns =[
    path('signup',SignupView.as_view(),name='signup'),
    path('home',HomePageView.as_view(),name='homepage')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




