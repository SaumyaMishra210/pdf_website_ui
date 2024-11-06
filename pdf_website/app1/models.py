from django.db import models


# Create your models here.
class Uploaded_Files_Model(models.Model):
    file = models.FileField(upload_to="uploads/")
    encrypted_file = models.FileField(upload_to="encrypted/")
    pswd = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.file}"


class file_model(models.Model):
    file = models.FileField(upload_to='uploads/')
