from django.db import models
from core.models import CoreModel


class Post(CoreModel):

    BLOG = "blog"
    SMART_STORE = "smart_store"
    SMART_PLACE = "smart_place"

    LOGIN_METHOD_CHOICES = (
        (BLOG, "blog"),
        (SMART_STORE, "smart_store"),
        (SMART_PLACE, "smart_place"),
    )

    text = models.TextField()
    type = models.CharField(choices=LOGIN_METHOD_CHOICES, max_length=15, null=True)
    photoes = models.ImageField(blank=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="posts"
    )

    def total_comment(self):
        all_comments = self.comments.all()
        return len(all_comments)