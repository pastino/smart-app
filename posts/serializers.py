from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    total_comments_num = serializers.CharField(source="total_comment", read_only=True)
    is_fav = serializers.SerializerMethodField(method_name="get_is_fav")

    class Meta:
        model = Post
        exclude = ("modified",)
        read_only_fields = [
            "user",
            "id",
            "created",
            "updated",
            "total_comments_num",
        ]

    def get_is_fav(self, obj):
        request = self.context.get("request")
        print(request)
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.fav_posts.all()
        return False

    def create(self, validated_data):
        request = self.context.get("request")
        post = Post.objects.create(**validated_data, user=request.user)
        return post
