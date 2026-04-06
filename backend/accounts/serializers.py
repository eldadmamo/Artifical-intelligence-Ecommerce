from rest_framework import serializers
from .models import User, Profile, Address 


class UserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only= True, min_length = 8)
    phone = serializers.CharField(required = False, allow_blank= True) 

    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError('User with this email already exists')
        return value 
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True, min_length = 8)
    phone = serializers.CharField(required = False, allow_blank = True)

    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError('User with this email already exists')
        return value 

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

class ProfileSerializers(serializers.ModelSerializer):
    user = UserSeralizer(read_only = True)
    class Meta:
        model = Profile 
        fields = [
            'user', 'avatar', 'gender', 'preferred_size', 'style_preferences', 'height_cm', 'weight_kg', 'size_system', 'currency', 'language', 'country', 'created_at', 'updated_at', 'name'
        ]
        read_only_fields = ['created_at', 'updated_at']

class AddressSerializers(serializers.ModelSerializers):
    class Meta:
        model = Address
        fields = [
            'id', 'address_type', 'full_name', 'phone', 'street_address', 'city', 'id', 'district', 'postal_code', 'country', 'is_default', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id','created_at', 'updated_at']

