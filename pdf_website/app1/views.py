import requests
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.views import View
from . import serializers
from .serializers import *
import logging
from PyPDF2 import PdfReader , PdfWriter
from django.core.files.base import ContentFile
import os

# Create your views here.
def index(request):
    return render(request,"index.html")

def download_page(request):
    return render(request,"download_page.html")

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from io import BytesIO

class upload_file_apiview(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = File_upload_serializer(data=request.data)
        if serializer.is_valid():
            file_name = request.FILES['file']
            password = serializer.data['pswd']

            reader = PdfReader(file_name)
            output_file = PdfWriter()

            # Add pages to the writer object
            for page in reader.pages:
                output_file.add_page(page)

            # Encrypt the PDF with the provided password
            output_file.encrypt(password)

            # Use a BytesIO buffer to capture the encrypted PDF content
            encrypted_buffer = BytesIO()
            output_file.write(encrypted_buffer)
            encrypted_buffer.seek(0)  # Move to the start of the buffer

            # Define the output file name
            base_name, _ = os.path.splitext(file_name.name)
            output_file_name = f"{base_name}_encrypted.pdf"

            # Save the encrypted content to the media folder
            file_path = default_storage.save(f"uploads/encrypted/{output_file_name}", ContentFile(encrypted_buffer.read()))

            print("200 ok")
            return Response({'message': 'PDF protected successfully!', 'file_url': file_path}, status=status.HTTP_201_CREATED)

        print("400")
        return Response({
            'message': 'Failed to protect PDF. Please check the file format and try again.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class pdf_upload(APIView):
    parser_classes = [MultiPartParser,FormParser]
    def post(self,request):
        serializer = file_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)