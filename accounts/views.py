from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework import status


# Register
class RegisterUserView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        email = request.data.get('email')
        username = request.data.get('username')

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if serializer.is_valid():
                    user = serializer.save()

                    return Response({
                        "user": UserSerializer(user, context=self.get_serializer_context()).data,
                        "token": AuthToken.objects.create(user)[1],
                    })

                else:
                    print('error', serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"msg": "This email is already registered."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"msg": "Username exists.Please try another."}, status=status.HTTP_400_BAD_REQUEST)


# Login
class LoginUserView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
              "user": UserSerializer(user, context=self.get_serializer_context()).data,
              "token": AuthToken.objects.create(user)[1],
              "msg": "Successfully Logged In!"
            })

        else:
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get User
class GetUserView(generics.RetrieveAPIView):
    permission_classes = [
      permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
