from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ExamplePost

User = get_user_model()
class PostSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        queryset=User.objects.filter(), slug_field='username'
    )

    class Meta:
        model = ExamplePost
        fields = ('id', 'author', 'text', 'created', 'updated')