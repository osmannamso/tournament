from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from userinfo.serializers import UserLoginSerializer


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = UserLoginSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        access_token = RefreshToken.for_user(data.validated_data['user']).access_token

        return Response({
            'access': str(access_token)
        })
