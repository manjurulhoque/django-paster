from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'pasteapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('pastes/<slug:slug>', PasteDetailsView.as_view(), name='paste-details'),
    path('pastes/<slug:slug>/download', DownloadView.as_view(), name='paste-download'),
    path('pastes/<slug:slug>/clone', CloneCreateView.as_view(), name='paste-clone'),
    path('pastes/<slug:slug>/clone-redirect', CloneRedirectView.as_view(), name='paste-clone-redirect'),
]
