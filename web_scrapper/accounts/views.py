from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import (
    UserRegistrationSerializer, )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
       Custom serializer for JWT token generation, extending TokenObtainPairSerializer.

       This serializer modifies the token payload to include additional user-related fields:
       - 'username': The username of the authenticated user.
       - 'is_admin': A boolean indicating if the user has admin privileges (is_staff).

       Methods:
           - get_token: Customizes the token by adding extra claims such as username and admin status.
       """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_admin'] = user.is_staff
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    """
        A custom view to obtain a JWT token using MyTokenObtainPairSerializer.

        Inherits from TokenObtainPairView and returns a token with additional claims like username and admin status.
        """
    serializer_class = MyTokenObtainPairSerializer


class userRegistrationView(APIView):
    """
        API view for handling user registration.

        This view processes user registration requests, ensuring that the email is unique
        and validating the provided data using UserRegistrationSerializer. If the registration is successful,
        a response containing the user data is returned; otherwise, appropriate error messages are returned.

        Methods:
            - post: Handles the POST request to register a new user. Validates the email for uniqueness
                    and creates a new user if valid.
        """

    def post(self, request, ):
        """
                Returns:
                    Response:a
                        - 201: If the user is successfully created, returns the created user data.
                        - 400: If the email already exists or validation errors occur.
                        - 500: If any unexpected server error happens during the process.
                """
        try:
            email = request.data.get('email')
            if User.objects.filter(email=email).exists():
                return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
