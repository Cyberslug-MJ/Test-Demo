from rest_framework import serializers
from accounts.models import CustomUser
import uuid

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8,write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    role = serializers.ChoiceField(choices=(("Parent","Parent"),("Student","Student"),("Teacher","Teacher")))
    class Meta:
        model = CustomUser
        fields = ['email','role','first_name','last_name','password']

    #CHECK THE EMAIL 
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
        role = validated_data['role'],
        first_name = validated_data['first_name'],
        last_name = validated_data['last_name'],
        school_name = "King Edward Preparatory School",
        username = username
        )
        user.set_password(validated_data['password'])
        user.save()
        return user