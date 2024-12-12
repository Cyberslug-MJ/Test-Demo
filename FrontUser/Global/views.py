from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from . serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method =='POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user created successfully","data":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response({"data":serializer.data,"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)