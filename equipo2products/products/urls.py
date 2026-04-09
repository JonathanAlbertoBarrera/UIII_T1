from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductoViewSet

router = DefaultRouter()
router.register(r'products', ProductoViewSet, basename='producto')

urlpatterns = [
    path('', include(router.urls)),
]