from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TodoListSerializer
from .models import TodoList
# Create your views here.


class TodoListViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer