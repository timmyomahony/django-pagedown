from django.contrib import admin
from django.db import models

from music.models import Artist, Song, Album
from music.forms import AdminAlbumForm

from pagedown.widgets import AdminPagedownWidget


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget}
    }


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    form = AdminAlbumForm
