from rest_framework.serializers import ModelSerializer
from .models import Comment
from users.serializers import UserSerializer
from posts.serializers import PostSerializer
from .models import Comment


class CommentSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)
    # post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ("modified",)
        read_only_fields = [
            "user",
            # "post",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        commnet = Comment.objects.create(**validated_data, user=request.user)
        return commnet
