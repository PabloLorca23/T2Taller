from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Artist, Album, Cancion
from . serializers import ArtistSerializer, AlbumSerializer, CancionSerializer
from base64 import b64encode


class ArtistList(APIView):

    def get(ArtistList, request):
        artists1 = Artist.objects.all()
        serializer = ArtistSerializer(artists1, many=True)
        return Response(serializer.data)

    def post(ArtistList, request):
        post_data = request.data
        id = b64encode(post_data['name'].encode()).decode('utf-8')
        albums = f"http://localhost:8000/artists/{id}/albums"
        tracks = f"http://localhost:8000/artists/{id}/tracks"
        nuevo_artista = Artist.objects.create(id = id, name = post_data['name'], age = post_data['age'], albums = albums, tracks = tracks)
        nuevo_artista.save()
        serializer = ArtistSerializer(nuevo_artista)
        return Response(serializer.data)

class AlbumList(APIView):

    def get(self, request):
        albums1 = Album.objects.all()
        serializer=AlbumSerializer(albums1, many=True)
        return Response(serializer.data)
    

class CancionList(APIView):

    def get(self, request):
        canciones1 = Cancion.objects.all()
        serializer=CancionSerializer(canciones1, many=True)
        return Response(serializer.data)


class ArtistById(APIView):

    def get(self, request,id):
        artist = Artist.objects.get(id = id)
        serializer = ArtistSerializer(artist)
        
        return Response(serializer.data)

    def delete(self,request):
        artist = Artist.objects.get(id = id)
        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class AlbumById(APIView):

    def get(self, request,id):
        album = Album.objects.get(id = id)
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    def delete(self,request):
        album = Album.objects.get(id = id)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CancionById(APIView):

    def get(self, request,id):
        cancion = Cancion.objects.get(id = id)
        serializer = CancionSerializer(cancion)
        return Response(serializer.data)

    def delete(self,request):
        cancion = Cancion.objects.get(id = id)
        cancion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class AlbumByArtist(APIView):

    def get(self, request, artist_id):
        url_artist = f"http://localhost:8000/artists/{artist_id}"
        album = Album.objects.get(artist = url_artist)
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    def post(self, request, artist_id):
        post_data = request.data
        nombre = post_data['name']+":"+artist_id
        id = b64encode(nombre.encode()).decode('utf-8')
        artista = f"http://localhost:8000/artists/{artist_id}"
        tracks = f"http://localhost:8000/albums/{id}/tracks"
        dependencia = Artist.objects.get(id = artist_id)
        nuevo_album = Album.objects.create(id = id, name = post_data['name'], genre = post_data['genre'], artist = artista, tracks = tracks, dependencia = dependencia, artist_id = artist_id)
        nuevo_album.save()
        serializer = AlbumSerializer(nuevo_album)
        return Response(serializer.data)

class CancionByArtist(APIView):

    def get(self, request, artist_id):
        url_artist = f"http://localhost:8000/artists/{artist_id}"
        canciones = Cancion.objects.get(artist = url_artist)
        serializer = CancionSerializer(canciones)
        return Response(serializer.data)


class CancionByAlbum(APIView):

    def get(self, request, album_id):
        url_album = f"http://localhost:8000/albums/{album_id}"
        tracks = Cancion.objects.get(album = url_album, many = True)
        serializer = CancionSerializer(tracks)
        return Response(serializer.data)

    def post(self, request, album_id):
        post_data = request.data
        nombre = post_data['name']+":"+album_id
        id = b64encode(nombre.encode()).decode('utf-8')
        album = f"http://localhost:8000/albums/{album_id}"
        dependencia = Album.objects.get(id = album_id)
        artist = f"http://localhost:8000/artists/{dependencia.dependencia.id}"
        nueva_cancion = Cancion.objects.create(id = id, name = post_data['name'], duration = post_data['duration'], times_played = 0, artist = artist, album = album, dependencia = dependencia, album_id = album_id)
        nueva_cancion.save()
        serializer = CancionSerializer(nueva_cancion)
        return Response(serializer.data)


class PlayByArtist(APIView):

    def put(self, request, artist_id):
        url_artist = f"http://localhost:8000/artists/{artist_id}"
        canciones = Cancion.objects.get(artist = url_artist, many = True)
        canciones.times_played +=1
        canciones.save()
        serializer = CancionSerializer(canciones)
        return Response(status = status.HTTP_200_OK)
        

class PlayByAlbum(APIView):

    def put(self, request, album_id):
        canciones = Cancion.objects.get(album_id = album_id, many = True)
        canciones.times_played +=1
        canciones.save()
        serializer = CancionSerializer(canciones)
        return Response(serializer.data)

class PlayByTrack(APIView):

    def put(self, request, track_id):
        canciones = Cancion.objects.get(id = track_id, many = True)
        canciones.times_played +=1
        serializer = CancionSerializer(canciones)
        canciones.save()
        return Response(serializer.data)






