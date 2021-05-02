from django.db import models


class Artist(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=1000)
    age = models.IntegerField()
    albums = models.CharField(max_length=1000)
    tracks = models.CharField(max_length=1000)

    

class Album(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    artist_id = models.CharField(max_length=22)
    name = models.CharField(max_length=1000)
    genre = models.CharField(max_length=1000)
    artist = models.CharField(max_length=1000)
    tracks = models.CharField(max_length=1000)
    dependencia = models.ForeignKey(Artist, on_delete=models.CASCADE)



class Cancion(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    album_id = models.CharField(max_length=22)
    name = models.CharField(max_length=1000)
    duration = models.FloatField()
    times_played = models.IntegerField()
    artist = models.CharField(max_length=1000)
    album = models.CharField(max_length=1000)
    dependencia = models.ForeignKey(Album, on_delete=models.CASCADE)


