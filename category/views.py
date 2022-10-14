from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Category
from . import serializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializer.CategorySerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]



