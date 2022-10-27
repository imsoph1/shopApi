from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView
from .send_email import send_confirmation_email, send_code_password_reset
from . import serialzers
from django.contrib.auth import get_user_model
# Create your views here

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serialzers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(user.email, user.activation_code)
            return Response(serializer.data, status=201)
        return Response('Bad request', status=400)


class ActivationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'Successfully activated1'}, status=200)
        except User.DoesNotExist:
            return Response({'msg': 'Link expired!'}, status=400)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class LogoutView(GenericAPIView):
    serializer_classes = serialzers.LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully logged out!', status=204)


class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
       serializer = serialzers.ForgotPasswordSerializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       try:
           email = serializer.data.get('email')
           user = User.objects.get(email=email)
           user.create_activation_code()
           user.save()
           send_code_password_reset(user)
           return Response('check ur email we sent u a code!')
       except User.DoesNotExist:
           return Response(
               'User with this email does not exist!', status=400
           )


class RestorePasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serialzer = serialzers.RestorePasswordserializer(data=request.data)
        serialzer.is_valid(raise_exception=True)
        serialzer.save()
        return Response('Password has changed successfully!!!')



