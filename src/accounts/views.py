from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView
from rest_framework import status

from accounts.exceptions import AccountException
from accounts.serializers import LoginSerializer, SignupSerializer
from core.authentications import CsrfExemptSessionAuthentication


class LoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: OpenApiResponse(description="로그인 성공")},
        description="로그인 API",
    )
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)
        if not user:
            raise AccountException.LoginFailException
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class SignupView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    @extend_schema(
        request=SignupSerializer,
        responses={
            200: OpenApiResponse(description="회원가입 성공")},
        description="회원가입 API",
    )
    def post(self, request: Request) -> Response:
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(description="로그아웃 성공")},
        description="로그아웃 API",
    )
    def post(self, request: Request) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)
