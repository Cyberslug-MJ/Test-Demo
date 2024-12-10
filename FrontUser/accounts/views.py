from django.shortcuts import render
from rest_framework.response import Response
from . serializers import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from . models import *


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method =="POST":
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = loginSerializer(data = request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data,status=status.HTTP_200_OK)
    
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT','PATCH']) #PATCH is for testing purposes 
def SchoolProfileManager(request):
    try:
        school_profile = SchoolProfile.objects.get(user_id=request.user.pk)
    except SchoolProfile.DoesNotExist:
        return Response({"message":"Profile does not exist"},status=status.HTTP_404_NOT_FOUND)
    
    if request.method in ['PATCH','PUT']:
        partial = request.method == 'PATCH' # will validate to True if it is 
    serializer = SchoolProfileSerializer(school_profile,data=request.data,partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Profile updated successfully","data":serializer.data},status=status.HTTP_200_OK)
    else:
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT','PATCH']) #PATCH is for testing purposes 
def SchoolProfileManager(request):
    try:
        school_profile = SchoolProfile.objects.get(user_id=request.user.pk)
    except SchoolProfile.DoesNotExist:
        return Response({"message":"Profile does not exist"},status=status.HTTP_404_NOT_FOUND)
    
    if request.method in ['PATCH','PUT']:
        partial = request.method == 'PATCH' # will validate to True if it is 
    serializer = SchoolProfileSerializer(school_profile,data=request.data,partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Profile updated successfully","data":serializer.data},status=status.HTTP_200_OK)
    else:
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)