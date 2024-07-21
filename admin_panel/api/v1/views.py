from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication


from admin_panel import models

from . import serializers
from .permissions import IsWebMailPermission


from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# create your views here


class StaffListPermissionApiView(generics.ListAPIView):
    serializer_class = serializers.ListPermissionSerializer

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(models.Staff)
        student_permissions = Permission.objects.filter(content_type=content_type)[4:]

        return student_permissions


class StaffViewSet(ModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer


class SayHello(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsWebMailPermission]

    def get(self, request):
        content_type = ContentType.objects.get_for_model(models.Staff, for_concrete_model=False)
        student_permissions = Permission.objects.filter(content_type=content_type)
        print('=' * 40)
        for p in student_permissions:
            request.user.user_permissions.add(p) 
            request.user.save()
        return Response('salam')

