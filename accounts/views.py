import logging

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, logout

from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

from .selectors import get_user
from .services import get_tokens_for_user

logger = logging.getLogger('common')
User = get_user_model()


class LoginAPI(APIView):
    '''
    Four type of return status:
        invalid - data invalid
        issue - known server issue
        unexpected - unknown server issue
        success - valid data
    '''

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(required=True)
        password = serializers.CharField(
            write_only=True, required=True,
            style={'input_type': 'password', 'placeholder': 'Password'}
        )

    def post(self, request):
        serialized_data = self.InputSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)

        username = serialized_data.validated_data['username']
        password = serialized_data.validated_data['password']
        user = get_user(username)

        if user is None:
            return Response({
                'status': 'issue',
                'response': {'message': 'Server Issue'}}, status=500)

        elif isinstance(user, ObjectDoesNotExist):
            return Response({
                'status': 'invalid',
                'response': {'message': 'User does not exist'}
            }, status=400)

        elif isinstance(user, User):
            if user.active == False:
                return Response({
                    'status': 'invalid',
                    'response': {'message': 'Your account has been suspended'}
                }, status=400)

            # have to check account confirmation

            is_valid_user = authenticate(
                username=user.username, password=password
            )
            if not is_valid_user:
                return Response({
                    'status': 'invalid',
                    'response': {'message': 'Password is incorrect'}
                }, status=400)

            tokens = get_tokens_for_user(user)
            return Response({
                'status': 'success',
                'response': {'data': tokens}}, status=200)

        logger.error('Found error in LoginAPI user response return')
        return Response({
            'status': 'unexpected',
            'response': {'message': 'Server Issue'}
        }, status=500)


class LogoutAPI(APIView):
    def get(self, request):
        # have to delete current user token (if user is logged in and token is valid)
        return Response(status=200)
