from rest_framework.serializers import ModelSerializer
from img.models import *

class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
