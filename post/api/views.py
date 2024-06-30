from rest_framework.viewsets import ModelViewSet 
from post.models import Post 
from rest_framework import viewsets
from post.api.serializers import PostSerializer 
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostApiViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = (MultiPartParser,FormParser,)
    permission_classes = [IsAuthenticatedOrReadOnly]

