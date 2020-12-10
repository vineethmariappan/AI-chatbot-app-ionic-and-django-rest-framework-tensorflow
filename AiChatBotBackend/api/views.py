from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
# from models import User
from rest_framework.decorators import api_view
from .chatbot import chatbot as c
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer

@api_view(['GET','POST'])
def chat(request):
    inp = request.data['msg']
    resp = c.chat(inp)
    return Response({'message' : resp})