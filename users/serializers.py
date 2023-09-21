from users.models import MCPUser
from django.contrib import auth
from rest_framework.serializers import ModelSerializer, CharField, ValidationError, SerializerMethodField, Serializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class MCPUserSerializer(ModelSerializer):
    class Meta:
        model = MCPUser
        fields = ['id', 'email', 'username', 'address', 'phoneNumber', 'city', 'state', 'area', 'age', 'gender', 'aadhar', 'profileImage', 'isDoctor', 'createdAt', 'updatedAt', 'is_active', 'is_admin', 'is_staff', 'is_superuser']

class RegisterSerializer(ModelSerializer):
    password = CharField(min_length=6, write_only=True)
    class Meta:
        model = MCPUser
        fields = ['username', 'email', 'password', 'city', 'state', 'area', 'phoneNumber', 'age', 'bloodGroup', 'gender', 'aadhar']
    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise ValidationError(self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return MCPUser.objects.create_user(**validated_data)
    
class LoginSerializer(ModelSerializer):
    password = CharField(min_length=6, write_only=True)
    username = CharField(max_length=255, min_length=3)
    tokens = SerializerMethodField()
    def get_tokens(self, obj):
        user = MCPUser.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    class Meta:
        model = MCPUser
        fields = ['password','username','tokens']
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = auth.authenticate(username=username,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

class LogoutSerializer(Serializer):
    refresh = CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')