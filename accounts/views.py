from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.utils import timezone
from accounts.models import CustomUser, UserConfirmation
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import (
    RegisterSerializer, RegisterVerifySerializer,
    PasswordResetRequestSerializer, PasswordResetVerifySerializer,
    PasswordResetSerializer, ResendCodeSerializer,
    LoginSerializer,
)


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterVerifyApiView(generics.GenericAPIView):
    serializer_class = RegisterVerifySerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = CustomUser.objects.get(email=email)
            confirmation = UserConfirmation.objects.get(code=code)

            if confirmation and confirmation.expires > timezone.now():
                user.is_active = True
                user.save()
                confirmation.is_used = True
                confirmation.save()
                return Response({'message': 'User verified successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired code'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)


class ResendCodeApiView(generics.GenericAPIView):
    serializer_class = ResendCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        code = user.generate_verify_code()
        return Response({'code': code})


class PasswordResetRequestApiView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user is None:
                return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
            code = user.generate_verify_code()
            return Response({'message': 'Verification code is sent to your email, please check inbox', 'code': code}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerifyApiView(generics.GenericAPIView):
    serializer_class = PasswordResetVerifySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.data['code']
            user = request.user
            otp_code = UserConfirmation.objects.filter(code=code).first()
            if user is None:
                return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
            if otp_code is None or otp_code.expires < timezone.now():
                return Response({'message': 'Incorrect verification code'}, status=status.HTTP_401_UNAUTHORIZED)
            otp_code.is_used = True
            otp_code.save()
            return Response({'message': 'Verification code is correct! Now you can change your password'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class PasswordResetApiView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            new_password = serializer.data['new_password']
            confirm_password = serializer.data['confirm_password']
            user = CustomUser.objects.filter(email=email).first()
            otp_code = UserConfirmation.objects.filter(user=user, is_used = True).first()
            if user is None:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            if otp_code is None:
                return Response({'message': 'Verification code not confirmed'}, status=status.HTTP_401_UNAUTHORIZED)
            if not otp_code.is_used:
                return Response({'message': 'Verification not confirmed'}, status=status.HTTP_401_UNAUTHORIZED)
            user.set_password(confirm_password)
            user.save()
            return Response({'message': 'Your password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = CustomUser.objects.filter(email=email).first()
            if user is None:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if not user.is_active:
                return Response({'message': 'User is not activated'}, status=status.HTTP_403_FORBIDDEN)
            
            if not user.check_password(password):
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            