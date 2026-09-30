from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer

User = get_user_model()


# ─────────────────────────────────────────────
# REGISTER — CreateAPIView
# ─────────────────────────────────────────────
@extend_schema_view(
    post=extend_schema(
        summary="Register a new user",
        description="Create a new account. Password is hashed automatically.",
        tags=["Auth"],
        request=RegisterSerializer,
        responses={
            201: RegisterSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
    ),
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# ─────────────────────────────────────────────
# LOGIN — TokenObtainPairView (JWT)
# ─────────────────────────────────────────────
@extend_schema_view(
    post=extend_schema(
        summary="Login (obtain JWT)",
        description="Returns access + refresh tokens and basic user info.",
        tags=["Auth"],
        request=LoginSerializer,
        responses={200: LoginSerializer, 401: OpenApiResponse(description="Invalid credentials")},
    ),
)
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]


# ─────────────────────────────────────────────
# ME — RetrieveUpdateAPIView (GET, PUT, PATCH)
# ─────────────────────────────────────────────
@extend_schema_view(
    get=extend_schema(
        summary="Get current user",
        tags=["Users"],
        responses={200: UserSerializer},
    ),
    put=extend_schema(
        summary="Full update current user",
        tags=["Users"],
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
    patch=extend_schema(
        summary="Partial update current user",
        tags=["Users"],
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
)
class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# ─────────────────────────────────────────────
# USER LIST — ListAPIView
# ─────────────────────────────────────────────
@extend_schema_view(
    get=extend_schema(
        summary="List all users",
        description="Returns all users, newest first. Tighten permissions in production.",
        tags=["Users"],
        responses={200: RegisterSerializer(many=True)},
    ),
)
class UserListCreateView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]   # change to IsAdminUser in prod


    