from django.urls import path
from users.views import (
    UserLoginView,
    UserLogoutView,
    student_signup,
    tutor_signup,
    PersonDetailUpdateView,
    PublicProfileView,
    activate,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("signup/tutor/", tutor_signup, name="tutor-signup"),
    path("signup/student/", student_signup, name="student-signup"),
    path("profile/", PersonDetailUpdateView.as_view(), name="profile"),
    path("profile/<int:pk>", PublicProfileView.as_view(), name="public-profile"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
