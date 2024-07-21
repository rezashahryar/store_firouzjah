from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# create your urls here


router = DefaultRouter()
router.register('staffs', views.StaffViewSet, basename='staff')

urlpatterns = [
    path('staff-staff/', views.SayHello.as_view()),
    path('list/staff/permissions/', views.StaffListPermissionApiView.as_view()),
    path('', include(router.urls)),
]
