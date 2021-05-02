from rest_framework import serializers
from . models import Artist, Album, Cancion
from base64 import b64encode

class ArtistSerializer(serializers.ModelSerializer):
    self = serializers.SerializerMethodField('crear_self')
    
    def crear_self(ArtistSerializer, artist):
        url_self = f"http://tarea2--taller.herokuapp.com/artists/{artist.id}"
        return url_self

    class Meta:
        model = Artist
        fields = ('id','name', 'age', 'albums','tracks', 'self')

class AlbumSerializer(serializers.ModelSerializer):
    self = serializers.SerializerMethodField('crear_self')
    
    def crear_self(AlbumSerializer, album):
        url_self = f"http://tarea2--taller.herokuapp.com/albums/{album.id}"
        return url_self

    class Meta:
        model = Album
        
        fields = ('id', 'artist_id','name', 'genre', 'artist','tracks', 'self')

class CancionSerializer(serializers.ModelSerializer):
    self = serializers.SerializerMethodField('crear_self')
    
    def crear_self(CancionSerializer, track):
        url_self = f"http://tarea2--taller.herokuapp.com/tracks/{track.id}"
        return url_self

    class Meta:
        model = Cancion
        fields = ('id', 'album_id', 'name', 'duration', 'times_played','artist','album', 'self')
