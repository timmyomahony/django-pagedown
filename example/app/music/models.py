from django.db import models


class Artist(models.Model):
    '''A music artist'''
    name = models.CharField(max_length=128)
    about = models.TextField(blank=True)  


class Album(models.Model):
    '''A music album.'''
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


class Song(models.Model):
    '''A music song.'''
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    lyrics = models.TextField(blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
