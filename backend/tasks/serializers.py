from django.contrib.auth.models import User
from django.utils.timezone import localtime
from rest_framework import serializers

from .models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True)
    category_name = serializers.CharField(
        source='category.name', read_only=True
    )
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'category',
            'category_name',
            'created_at',
            'updated_at',
            'due_date'
        )

    def get_created_at(self, obj):
        return localtime(obj.created_at).strftime('%d.%m.%Y %H:%M')

    def create(self, validated_data):
        category_name = validated_data.pop('category', None)

        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
            validated_data['category'] = category

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        category_name = validated_data.pop('category', None)

        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
            validated_data['category'] = category

        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
