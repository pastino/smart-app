from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """Custom User Model"""

    KAKAO_LOGIN = "kakao"
    NAVER_LOGIN = "naver"
    GOOGLE_LOGIN = "google"
    NORMAL_LOGIN = "normal"

    LOGIN_METHOD_CHOICES = (
        (KAKAO_LOGIN, "Kakao"),
        (NAVER_LOGIN, "Naver"),
        (GOOGLE_LOGIN, "Google"),
        (NORMAL_LOGIN, "Normal"),
    )

    account_id = models.CharField(max_length=50, blank=True)
    login_method = models.CharField(
        choices=LOGIN_METHOD_CHOICES, max_length=8, null=True
    )
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    fav_posts = models.ManyToManyField("posts.Post", related_name="fav_posts")
    superhost = models.BooleanField(default=False)
