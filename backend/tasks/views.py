from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import Task, Category
from .permissions import IsBotOrAuthenticated
from .serializers import TaskSerializer, CategorySerializer, RegisterSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBotOrAuthenticated]

    def get_queryset(self):
        """Фильтруем задачи по пользователю"""
        user = self.request.user
        user_id = self.request.headers.get('X-User-ID')

        if user.is_authenticated:
            return Task.objects.filter(user=user).select_related('category')
        if user_id:
            user, _ = User.objects.get_or_create(
                id=user_id, defaults={'username': f'user_{user_id}'}
            )
            return Task.objects.filter(user=user).select_related('category')

        return Task.objects.none()

    def perform_create(self, serializer):
        """Привязываем задачу к пользователю"""
        user = self.request.user
        user_id = self.request.headers.get('X-User-ID')
        print(self.request.headers)
        if user.is_authenticated:

            serializer.save(user=user)
        elif user_id:

            user, created = User.objects.get_or_create(
                id=user_id, defaults={'username': f'user_{user_id}'}
            )

            serializer.save(user=user)


class AnonTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class RegisterView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Пользователь успешно создан'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
