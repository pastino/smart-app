from rest_framework.routers import DefaultRouter
from . import views

app_name = "comments"

router = DefaultRouter()
router.register("", views.CommentViewSet)
urlpatterns = router.urls
