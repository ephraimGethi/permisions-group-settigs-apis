from rest_framework import serializers
from .models import ConversationMessage,Conversation
from django.contrib.auth.models import User

class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        """Ensure the username is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        """Ensure the email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_password(self, value):
        """Ensure password meets security requirements."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value

    def validate(self, attrs):
        """Ensure username and password are not the same."""
        if attrs['username'].lower() == attrs['password'].lower():
            raise serializers.ValidationError({"password": "Password cannot be the same as the username."})
        return attrs  # Must return the validated attributes dictionary

    def create(self, validated_data):
        """Create and return a superuser."""
        return User.objects.create_superuser(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )



class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id','username'
        ]
class ConversationListSerializer(serializers.ModelSerializer):
    users = UserDetailSerializer(many=True,read_only = True)
    class Meta:
        model = Conversation
        fields = [
            'id',
            'users',
            'modified_at',
        ]

class ConversationDetailSerializer(serializers.ModelSerializer):
    users = UserDetailSerializer(many=True,read_only = True)
    class Meta:
        model = Conversation
        fields = [
            'id',
            'users',
            'modified_at',
        ]

class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserDetailSerializer(many=False,read_only = True)
    created_by = UserDetailSerializer(many=False,read_only = True)
    class Meta:
        model = ConversationMessage
        fields = [
            'id',
            'body',
            'sent_to',
            'created_by',
        ]