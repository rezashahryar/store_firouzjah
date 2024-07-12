from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from core.models import OtpRequest, User

from .serializers import RequestSendOtpSerializer, VerifyOtpSerializer

# create your views here

class SendOtpView(generics.CreateAPIView):
    queryset = OtpRequest.objects.all()
    serializer_class = RequestSendOtpSerializer


class CheckOtp(APIView):
    serializer_class = VerifyOtpSerializer

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = User.objects.get(mobile=serializer.validated_data.get('mobile'))

            if user is not None:
                token = Token.objects.get(user=user)

                try:
                    token = Token.objects.get(user_id=user.id)

                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)

                return Response({
                    "token": str(token)
                })

        except User.DoesNotExist:
            user = User.objects.create(mobile=serializer.validated_data.get('mobile'))
            user.save()
            user.username = f'user_{user.pk}'
            user.save()

            try:
                token = Token.objects.get(user_id=user.id)

            except Token.DoesNotExist:
                token = Token.objects.create(user=user)

            return Response({
                "token": str(token)
            })



        return Response(status=status.HTTP_200_OK)
