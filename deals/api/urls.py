from django.urls import path

from .views import UploadDealsListCustomerAPIView


urlpatterns = [
    path('', UploadDealsListCustomerAPIView.as_view()),
]
