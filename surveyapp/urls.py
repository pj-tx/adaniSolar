from django.urls import path, include
from .views import SurveyViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'surveys', SurveyViewSet, basename='survey')

urlpatterns = [
    path('', include(router.urls)),
]