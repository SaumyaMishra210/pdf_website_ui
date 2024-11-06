from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

class FileUploadTests(APITestCase):
    def test_file_upload(self):
        url = 'file/'
        file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        data = {'file': file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.data['message'], 'File uploaded successfully!')
