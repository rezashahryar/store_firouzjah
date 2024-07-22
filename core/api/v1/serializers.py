import requests
import json
import random

from django.utils import timezone
from rest_framework import serializers
from django.conf import settings

from core.models import OtpRequest

# create your serializers here

class RequestSendOtpSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    mobile = serializers.CharField(max_length=11, allow_null=False)

    def create(self, validated_data):
        req_otp = OtpRequest.objects.create(
            mobile=validated_data['mobile'],
            otp_code=self._random_code()
        )
        req_otp.save()

        request_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        }

        data = {
            "UserName": settings.WEB_SERVICE_OTP_USERNAME,
            "Password": settings.WEB_SERVICE_OTP_PASSWORD,
            "From": settings.SEND_OTP_CODE_FROM,
            "To": req_otp.mobile,
            "Message": f"کد بازیابی شما : {req_otp.otp_code}",
        }

        res = requests.post(
            url='https://webone-sms.ir/SMSInOutBox/Send',
            data=json.dumps(data),
            headers=request_headers
        )

        return req_otp
    
    def _random_code(self):
        return int(random.randint(10000, 99999))
    

class VerifyOtpSerializer(serializers.Serializer):
    id = serializers.UUIDField(allow_null=False)
    otp_code = serializers.CharField(max_length=5)
    mobile = serializers.CharField(max_length=11)


    def validate(self, attrs):
        try:
            otp_req = OtpRequest.objects.get(
                id=attrs['id'],
                otp_code=attrs['otp_code']
            )

            if otp_req.valid_until < timezone.now():
                raise serializers.ValidationError("this code expired")
        except OtpRequest.DoesNotExist:
            raise serializers.ValidationError("serializer error")
        

            
        return super().validate(attrs)
