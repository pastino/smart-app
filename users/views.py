import jwt
from django.conf import settings
from .models import User
from posts.models import Post
from .serializers import UserSerializer
from posts.serializers import PostSerializer
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from .permissions import IsSelf


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        print(self.action)
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif (
            self.action == "create"
            or self.action == "retrieve"
            or self.action == "login"
            or self.action == "favs"
        ):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def login(self, request):
        account_id = request.data.get("account_id")
        username = request.data.get("username")
        login_method = request.data.get("login_method")
        password = request.data.get("password")
        if not account_id and not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif account_id and not password:
            try:
                user = User.objects.get(account_id=account_id)
                encoded_jwt = jwt.encode(
                    {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
                )
                if user.login_method == "kakao":
                    avatar = None
                    if user.avatar:
                        avatar = user.avatar
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            "token": encoded_jwt,
                            "id": user.id,
                            "account_id": user.account_id,
                            "username": user.username,
                            "avatar": avatar,
                        },
                    )
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                user = User.objects.create(
                    account_id=account_id, login_method=login_method, username=username
                )
                user.set_unusable_password()
                user.save()
                return Response(status=status.HTTP_201_CREATED)

    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        serializer = PostSerializer(user.fav_posts.all(), many=True).data
        return Response(serializer)

    @favs.mapping.put
    def toggle_favs(self, request, pk):
        pk = request.data.get("pk", None)
        print(pk)
        user = request.user
        if pk is not None:
            try:
                post = Post.objects.get(pk=pk)
                if post in user.fav_posts.all():
                    user.fav_posts.remove(post)
                else:
                    user.fav_posts.add(post)
                return Response()
            except Post.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)