# views.py
from django.shortcuts import render

import redis
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.core.files.uploadedfile import UploadedFile
from .models import Files  # Assuming Files is your model for uploaded files
import time

# Initialize Redis client (assuming Redis is running locally on port 6379)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a unique ID for this upload session
        upload_id = str(time.time())  # You can use any unique identifier
        
        # Track progress by reading the file in chunks
        file_size = file_obj.size
        bytes_uploaded = 0
        
        # Save file in chunks
        with open(f'media/uploads/{file_obj.name}', 'wb') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
                bytes_uploaded += len(chunk)
                
                # Update progress in Redis
                progress = (bytes_uploaded / file_size) * 100
                redis_client.set(upload_id, progress)
        
        # Save to model
        file_instance = Files(file=file_obj)
        file_instance.save()

        # Clean up Redis key after upload
        redis_client.delete(upload_id)

        return Response({'message': 'File uploaded successfully', 'upload_id': upload_id}, status=status.HTTP_201_CREATED)

class UploadProgressView(APIView):
    def get(self, request, upload_id, *args, **kwargs):
        progress = redis_client.get(upload_id)
        
        if progress:
            progress = float(progress)
            return Response({'progress': progress}, status=status.HTTP_200_OK)
        else:
            return Response({'progress': 100}, status=status.HTTP_200_OK)  # Assuming 100% if not found


def index_view(request):
    return render(request, "index_sample.html")
    