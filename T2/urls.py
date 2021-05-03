"""T2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from Tarea2 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^artists/?$', views.ArtistList.as_view()),
    re_path(r'^albums/?$', views.AlbumList.as_view()),
    re_path(r'^tracks/?$', views.CancionList.as_view()),
    path('artists/<str:id>', views.ArtistById.as_view()),
    path('albums/<str:id>', views.AlbumById.as_view()),
    path('tracks/<str:id>', views.CancionById.as_view()),
    path('artists/<str:artist_id>/albums', views.AlbumByArtist.as_view()),
    path('artists/<str:artist_id>/tracks', views.CancionByArtist.as_view()),
    path('albums/<str:album_id>/tracks', views.CancionByAlbum.as_view()),
    path('artists/<str:artist_id>/albums/play', views.PlayByArtist.as_view()),
    path('albums/<str:album_id>/tracks/play', views.PlayByAlbum.as_view()),
    path('tracks/<str:track_id>/play', views.PlayByTrack.as_view())
]
