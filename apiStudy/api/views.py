from django.shortcuts import render
from .serializers import UserCreateSerializer, QuestionSerializer, CommentSerializer, QuestionOnlySerializer, UserLoginSerializer
from rest_framework import viewsets
from .models import Question, Comment
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request) :
    if request.method == 'POST' :
        serializer = UserLoginSerializer(data= request.data)

        if not serializer.is_valid(raise_exception=True) :
            return Response({"message" : "Request Body Error"}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['username'] == "None" :
            return Response({"message" : "fail"}, status=status.HTTP_409_CONFLICT)
        
        return Response({
            'success' : 'True',
            'token' : serializer.data['token']
        },status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def createUser(request):
    if request.method == 'POST' :
        serializer = UserCreateSerializer(data= request.data)
        if not serializer.is_valid(raise_exception=True) :
            return Response({"message" : "Request Body Error"}, status=status.HTTP_409_CONFLICT)
        
        if User.objects.filter(username=serializer.validated_data['username']).first() is None:
            serializer.save()
            return Response({"message" : "account ok!!"}, status=status.HTTP_201_CREATED)
        return Response({"message" : "duplicate username"}, status=status.HTTP_409_CONFLICT)

class QuestionViewSet(viewsets.ModelViewSet) :
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet) :
    queryset = Comment.objects.filter(parent = None).order_by('-created_at')
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionOnlySerializer
    permission_classes = [AllowAny]
    