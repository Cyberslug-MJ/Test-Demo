import uuid
from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import re

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
    name = serializers.CharField(max_length=255)
    logo = serializers.URLField()
    address = serializers.CharField(max_length=255)
    bio = serializers.CharField(max_length=500)
    theme = serializers.CharField(min_length=7)

    class Meta:
        model = SchoolProfile
        fields = ['name','logo','address','bio','theme']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.is_updatable:
            self.fields['name'].read_only = True


    def validate_name(self,value):
        if SchoolProfile.objects.filter(name=value).exists():
            raise serializers.ValidationError(f"Sorry, {value} is not available")
        return value
    

    def validate_theme(self, value):
        """Ensure theme is a valid hex color."""
        if not re.match(r'^#[0-9A-Fa-f]{6}$', value):
            raise serializers.ValidationError("Invalid theme color. Must be a valid hex color code.")
        return value


    def create(self,validated_data):
        return super().create(validated_data)
    

class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.URLField()
    firstname = serializers.CharField(max_length=100,required=False,default="N/A")
    lastname = serializers.CharField(max_length=100,required=False,default="N/A")
    email = serializers.EmailField(required=False,read_only=True)
    #phone_number = serializers.CharField(required=False,default="N/A")
    address = serializers.CharField(max_length=255,required=False)

    def validate_phone_number(self,value):
        if UserProfile.objects.filter(phone_number=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Phone number is already in use")
        else:
            return value
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture','firstname','lastname','email','address']

    def update(self, instance, validated_data):
        # Updates the fields if data is provided and fills them with the old data if none is
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        #instance.email = validated_data.get('email', instance.email)
        #instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance