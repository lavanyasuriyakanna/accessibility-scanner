from django.urls import path
from .views import ScanWebpageView

urlpatterns = [
    path('scan/', ScanWebpageView.as_view(), name='scan_webpage'),
]
