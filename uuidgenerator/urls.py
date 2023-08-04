from django.urls import path, include
from .views import UUIDViewSet, EmailSender, SmsSender
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'uuids', UUIDViewSet, basename='uuid')
router.register(r'emails', EmailSender, basename='email')
router.register(r'sms', SmsSender, basename='sms')

urlpatterns = [
    path('', include(router.urls)),
]