from rest_framework import serializers
from .models import Question, Comment, University
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)

        if user is None:
            return {
                'username' : 'None'
            }
        try : 
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exists'
            )
        return {
            'username' : user.username,
            'token' : jwt_token
        }

User = get_user_model()
class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    university = serializers.CharField(required=True)

    def create(self, validate_data):
        user = User.objects.create(
            username = validate_data['username'],
            university = get_object_or_404(University, name= validate_data['university'])
        )
        user.set_password(validate_data['password'])
        user.save()
        return user

class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Question
        fields = ['id', 'url', 'title', 'body', 'author']
    
    def validate(self, data):
        if len(data['title']) < 5 :
            raise serializers.ValidationError("very short")
        return data

class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        fields = ['id', 'url', 'question', 'parent', 'content', 'user', 'reply']

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data

class QuestionOnlySerializer(serializers.ModelSerializer):
    parent_comments = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'parent_comments']

    def get_parent_comments(self, question):
        parent_comments = Comment.objects.filter(question = question, parent = None)
        serializer = CommentSerializer(parent_comments, many = True, context=self.context)
        return serializer.data