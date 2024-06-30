from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers
from post.models import Post 

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image','price']

