from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .permissions import IsOwner
from rest_framework.pagination import PageNumberPagination


class CommentViewSet(ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def search(self, request):
        try:
            post_id = request.GET.get("post_id", None)

            filter_kwargs = {}
            filter_kwargs["post"] = post_id

            comments = Comment.objects.filter(**filter_kwargs)
            orderComments = comments.order_by("-created")
            serializer = CommentSerializer(orderComments, many=True)

            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"message": "not found page"}
            )
