import uuid
from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8,write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email','password']

    #CHECK  THE EMAIL 
    def validate_email(self,value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use")
        return value

    

    def create(self,validated_data):

        unique_id = uuid.uuid4().hex[:6] # this generates a short unique id
        username = f"user_{unique_id}"

        while CustomUser.objects.filter(username=username).exists():
            unique_id = uuid.uuid4().hex[:6]
            username = f"user_{unique_id}"

        user = CustomUser(
        email = validated_data['email'],
        role = "Admin",
        username = username
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class loginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254,write_only=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email','password']

    def validate_email(self,value):
        if CustomUser.objects.filter(email=value).exists():
            return value 
        else:
            raise serializers.ValidationError("Invalid credentials provided")
    
    def validate(self,data):
        email = data['email']
        password = data['password']

        user = authenticate(email=email,password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            data.pop('email',None)
            data.pop('password',None)
            data["refresh_token"] = str(refresh)
            data["access_token"] = str(refresh.access_token)
            return data 

        else:
            raise serializers.ValidationError("Invalid credentials provided")
        

class SchoolProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    name = serializers.CharField(max_length=255)
    logo = serializers.URLField(default="https://my-bucket.s3.amazonaws.com/my-folder/my-image.jpg?AWSAccessKeyId=EXAMPLE&Expires=1672531199&Signature=abcdef")
    address = serializers.CharField(max_length=255)
    bio = serializers.CharField(max_length=500)
    theme = serializers.CharField(min_length=7)

    class Meta:
        model = SchoolProfile
        fields = ['user','name','logo','address','bio','theme']

    def validate_name(self,value):
        if SchoolProfile.objects.filter(name=value).exists():
            raise serializers.ValidationError(f"Sorry, {value} is not available")
        return value


    def create(self,validated_data):
        school_profile = SchoolProfile(
            name = validated_data['name'],
            logo = validated_data['logo'],
            address = validated_data['address'],
            bio = validated_data['bio'],
            theme = validated_data['theme']
        )
        school_profile.save()
        return school_profile