from django.db import transaction 
from django.core.exceptions import ValidationError
from .models import User, Profile, Address

class AccountServices:
    @staticmethod
    @transaction.atomic
    def create_user(email, password, phone = None):
        if User.objects.filter(email = email).exists():
            raise ValidationError('User with this email already exists')
        
        user = User.objects.create_user(email = email, password = password, phone = phone)

        Profile.objects.get_or_create(user = user)

        return user
    
    @staticmethod
    def update_fcm_method(user, fcm_token):
        profile = user.profile
        profile.fcm_token = fcm_token 
        profile.save(update_fields = ['fcm_token'])
        return profile 