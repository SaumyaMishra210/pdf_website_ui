## for index page
# POST /api/upload-pdf/
# GET /api/upload-progress/
# GET /api/uploaded-files/

## for user registration page
# POST /api/register/
# GET /api/check-username/ or GET /api/check-email/
# GET /api/terms/

from django.urls import path , include
from pdf_web.settings import *
from django.conf.urls.static import static
from . import views

from django.urls import path
from .views import FileUploadView, UploadProgressView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('upload/progress/<str:upload_id>/', UploadProgressView.as_view(), name='upload-progress'),

    path('index',views.index_view,name='index'),
]

    

if DEBUG :
    urlpatterns+= static(MEDIA_URL,document_root = MEDIA_ROOT)