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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(ArtistList, request):
        if request.data and ('name' in request.data.keys()) and ('age' in request.data.keys()):
            if type(request.data['name'])== str and type(request.data['age'])== int:
                post_data = request.data
                id = b64encode(post_data['name'].encode()).decode('utf-8')
                id = id[0:22]
                if len(Artist.objects.filter(id = id))>0:
                    artista_viejo = Artist.objects.get(id = id)
                    serializer = ArtistSerializer(artista_viejo)
                    return Response(serializer.data, status = status.HTTP_409_CONFLICT)
                else:
                    albums = f"https://tarea2--taller.herokuapp.com/artists/{id}/albums"
                    tracks = f"https://tarea2--taller.herokuapp.com/artists/{id}/tracks"
                    nuevo_artista = Artist.objects.create(id = id, name = post_data['name'], age = post_data['age'], albums = albums, tracks = tracks)
                    nuevo_artista.save()
                    serializer = ArtistSerializer(nuevo_artista)
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
            else:
                return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status= status.HTTP_400_BAD_REQUEST)

    def put(ArtistList,request):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(ArtistList,request):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

class AlbumList(APIView):

    def get(self, request):
        albums1 = Album.objects.all()
        serializer=AlbumSerializer(albums1, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(AlbumList, request):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(AlbumList, request):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED) 
    def delete(AlbumList, request):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)   

class CancionList(APIView):

    def get(self, request):
        canciones1 = Cancion.objects.all()
        serializer=CancionSerializer(canciones1, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArtistById(APIView):

    def get(self, request,id):
        if len(Artist.objects.filter(id = id))>0:
            artist = Artist.objects.get(id = id)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self,request, id):
        if len(Artist.objects.filter(id = id))>0:
            artist = Artist.objects.get(id = id)
            artist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)




class AlbumById(APIView):

    def get(self, request,id):
        if len(Album.objects.filter(id = id))>0:
            album = Album.objects.get(id = id)
            serializer = AlbumSerializer(album)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self,request, id):
        if len(Album.objects.filter(id = id))>0:
            album = Album.objects.get(id = id)
            album.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CancionById(APIView):

    def get(self, request,id):
        if len(Cancion.objects.filter(id = id))>0:
            cancion = Cancion.objects.get(id = id)
            serializer = CancionSerializer(cancion)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self,request, id):
        if len(Cancion.objects.filter(id = id))>0:
            cancion = Cancion.objects.get(id = id)
            cancion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class AlbumByArtist(APIView):

    def get(self, request, artist_id):
        if len(Artist.objects.filter(id = artist_id))>0:
            url_artist = f"http://tarea2--taller.herokuapp.com/artists/{artist_id}"
            album = Album.objects.filter(artist = url_artist)
            serializer = AlbumSerializer(album, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, artist_id):
        if len(Artist.objects.filter(id = artist_id))>0:
            if request.data and ('name' in request.data.keys()) and ('genre' in request.data.keys()): 
                if type(request.data['name'])== str and type(request.data['genre'])==str:
                    post_data = request.data
                    nombre = post_data['name']+":"+artist_id
                    id = b64encode(nombre.encode()).decode('utf-8')
                    id = id[0:22]
                    if len(Album.objects.filter(id = id))>0:
                        album_viejo = Album.objects.get(id = id)
                        serializer = AlbumSerializer(album_viejo)
                        return Response(serializer.data, status= status.HTTP_409_CONFLICT)
                    else:
                        artista = f"http://tarea2--taller.herokuapp.com/artists/{artist_id}"
                        tracks = f"http://tarea2--taller.herokuapp.com/albums/{id}/tracks"
                        dependencia = Artist.objects.get(id = artist_id)
                        nuevo_album = Album.objects.create(id = id, name = post_data['name'], genre = post_data['genre'], artist = artista, tracks = tracks, dependencia = dependencia, artist_id = artist_id)
                        nuevo_album.save()
                        serializer = AlbumSerializer(nuevo_album)
                        return Response(serializer.data, status = status.HTTP_201_CREATED)
                else:
                    return Response(status= status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status= status.HTTP_422_UNPROCESSABLE_ENTITY)

class CancionByArtist(APIView):

    def get(self, request, artist_id):
        if len(Artist.objects.filter(id = artist_id))>0:
            url_artist = f"http://tarea2--taller.herokuapp.com/artists/{artist_id}"
            canciones = Cancion.objects.filter(artist = url_artist)
            serializer = CancionSerializer(canciones, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class CancionByAlbum(APIView):

    def get(self, request, album_id):
        if len(Album.objects.filter(id = album_id))>0:
            url_album = f"http://tarea2--taller.herokuapp.com/albums/{album_id}"
            tracks = Cancion.objects.filter(album = url_album)
            serializer = CancionSerializer(tracks, many = True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, album_id):
        if len(Album.objects.filter(id = album_id))>0:
            if request.data and ('name' in request.data.keys()) and ('duration' in request.data.keys()): 
                if type(request.data['name'])== str and type(request.data['duration'])== float:
                    post_data = request.data
                    nombre = post_data['name']+":"+album_id
                    id = b64encode(nombre.encode()).decode('utf-8')
                    id = id[0:22]
                    if len(Cancion.objects.filter(id = id))>0:
                        cancion_vieja = Cancion.objects.get(id = id)
                        serializer = CancionSerializer(cancion_vieja)
                        return Response(serializer.data, status= status.HTTP_409_CONFLICT)
                    else:
                        album = f"http://tarea2--taller.herokuapp.com/albums/{album_id}"
                        dependencia = Album.objects.get(id = album_id)
                        artist = f"http://tarea2--taller.herokuapp.com/{dependencia.dependencia.id}"
                        nueva_cancion = Cancion.objects.create(id = id, name = post_data['name'], duration = post_data['duration'], times_played = 0, artist = artist, album = album, dependencia = dependencia, album_id = album_id)
                        nueva_cancion.save()
                        serializer = CancionSerializer(nueva_cancion)
                        return Response(serializer.data, status = status.HTTP_201_CREATED)
                else:
                    return Response(status= status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status= status.HTTP_422_UNPROCESSABLE_ENTITY)



class PlayByArtist(APIView):

    def put(self, request, artist_id):
        if len(Artist.objects.filter(id = artist_id))>0:
            url_artist = f"http://tarea2--taller.herokuapp.com/artists/{artist_id}"
            canciones = Cancion.objects.filter(artist = url_artist)
            for cancion in canciones:
                cancion.times_played +=1
                cancion.save()
            serializer = CancionSerializer(canciones, many=True)
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PlayByAlbum(APIView):

    def put(self, request, album_id):
        if len(Album.objects.filter(id = album_id))>0:
            url_album = f"http://tarea2--taller.herokuapp.com/albums/{album_id}"
            canciones = Cancion.objects.filter(album = url_album)
            for cancion in canciones:
                cancion.times_played +=1
                cancion.save()
            serializer = CancionSerializer(canciones, many=True)
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PlayByTrack(APIView):

    def put(self, request, track_id):
        if len(Cancion.objects.filter(id = track_id))>0:
            cancion = Cancion.objects.get(id = track_id)
            cancion.times_played +=1
            cancion.save()
            serializer = CancionSerializer(cancion)
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)






