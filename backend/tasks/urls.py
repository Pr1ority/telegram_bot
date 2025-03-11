from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, CategoryViewSet, RegisterView


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]
