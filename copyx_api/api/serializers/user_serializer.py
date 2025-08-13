from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value.lower()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
    
class UserLoginSerializer(serializers.Serializer):
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

class FollowSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'followers_count', 'following_count', 'is_following' ]

        def get_is_following(self, obj):
            request = self.context.get('request')
            if request and request.user.is_authenticated:
                return request.user.is_following(obj)
            return False