# Create your views here.
from rest_framework.generics import CreateAPIView

from authentication.serializers import RequestOTPSerializer


class RequestOTPView(CreateAPIView):
    serializer_class = RequestOTPSerializer

    def perform_create(self, serializer):
        pass
