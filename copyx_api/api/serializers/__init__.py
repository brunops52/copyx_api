from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_namw=validated_data.get('last_name', '')
        )
        return user
    
class UserLoginSerializeR(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        if '@' in username_or_email:
            kwargs = {'email': username_or_email}
        else:
            kwargs = {'username': username_or_email}

        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
            raise serializers.ValidationError("Senha incorreta.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não encontrado.")
        
class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'bio', 'profile_picture', 'cover_photo', 
                  'followers_count', 'following_count')
        read_only_fields = ('id', 'username', 'email',)