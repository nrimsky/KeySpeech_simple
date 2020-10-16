from django.urls import path
from django.conf.urls.static import static
from . import views
from KeySpeech import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('termsandcondtions/', views.tandc, name='tandc'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('uploads/<int:pk>/', views.delete_freqlist, name='delete'),
    path('<int:freqlist_id>/', views.freqlists, name='freqlists'),
    path('uploads/form', views.model_form_upload, name='model_form_upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
