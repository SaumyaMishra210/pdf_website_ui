from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('download',views.download_page,name='download_page'),
    path('api/pdf/',views.upload_file_apiview.as_view(),name='protect-pdf'),
    path('file/',views.pdf_upload.as_view(),name ="file"),
]