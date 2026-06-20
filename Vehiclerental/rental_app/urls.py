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
]

# ഇതിലേക്ക് മാറ്റുക (STATIC-നൊപ്പം MEDIA കോഡും ചേർക്കുക)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)