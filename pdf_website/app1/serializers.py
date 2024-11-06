from rest_framework.serializers import ModelSerializer
from . import models

class File_upload_serializer(ModelSerializer):
    class Meta:
        model = models.Uploaded_Files_Model
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}} #  makes the password write-only so it doesn’t get exposed in API responses.


class file_serializer(ModelSerializer):
    class Meta:
        model = models.file_model
        fields = ["file"]