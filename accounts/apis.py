import logging

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, logout, login as django_login

from rest_framework.views import APIView, View
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from .selectors import get_user
from .services import get_tokens_for_user

logger = logging.getLogger('common')
User = get_user_model()


class LoginAPI(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(required=True)
        password = serializers.CharField(
            write_only=True, required=True,
            style={'input_type': 'password'}
        )

    def post(self, request):
        serialized_data = self.InputSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)

        username = serialized_data.validated_data['username']
        password = serialized_data.validated_data['password']
        user = get_user(username)

        if user is None:
            return Response({'message': 'Server Issue'}, status=500)

        elif isinstance(user, ObjectDoesNotExist):
            return Response({'message': 'User does not exist'}, status=400)

        elif isinstance(user, User):
            if user.active == False:
                if user.accountconfirmation.confirmation_status == False:
                    return Response({'message': 'Account confirmation required before login'})
                else:
                    return Response({
                        'message': user.accountstatus.inactive_reason,
                        'extra': {
                            'description': user.accountstatus.description
                        }}, status=400)

            is_valid_user = authenticate(
                username=user.username, password=password
            )
            if not is_valid_user:
                return Response({'message': 'Password is incorrect'}, status=400)

            if request.data.get('csrfmiddlewaretoken'):
                print(request.data['csrfmiddlewaretoken'])
                django_login(request, user)
            else:
                print('NO token found')

            tokens = get_tokens_for_user(user)
            return Response({'message': 'success', 'extra':{'data':tokens}}, status=200)

        logger.error('Found error in LoginAPI user response return')
        return Response({'message': 'Server Issue'}, status=500)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_token = OutstandingToken.objects.filter(user=request.user)
        for token in user_token:
            token.delete()
        logout(request)
        return Response(status=200)
