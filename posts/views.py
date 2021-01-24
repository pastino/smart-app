from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .permissions import IsOwner


class PostViewSet(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if (
            self.action == "list"
            or self.action == "retrieve"
            or self.action == "search"
        ):
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def search(self, request):
        try:
            type = request.GET.get("type", None)
            paginator = PageNumberPagination()
            paginator.page_size = 10
            filter_kwargs = {}
            filter_kwargs["type"] = type
            posts = Post.objects.filter(**filter_kwargs)
            orderPosts = posts.order_by("-created")
            results = paginator.paginate_queryset(orderPosts, request)
            serializer = PostSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"message": "not found page"}
            )
