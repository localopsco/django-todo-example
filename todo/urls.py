from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, meta_resp, health, lops_helm_values

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('meta/', meta_resp, name='meta'),
    path('health/', health, name='health'),
    path('lops-helm-values/', lops_helm_values, name='lops_helm_values')
]
