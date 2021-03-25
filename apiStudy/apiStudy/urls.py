from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from api.views import QuestionViewSet, CommentViewSet, CommentOnlyViewSet, createUser, login

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'comments', CommentViewSet)
router.register(r'view/comment', CommentOnlyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('create/', createUser, name='create'),
    path('login/', login, name='login')
]
