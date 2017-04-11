from django.views.generic.edit import CreateView

from music.models import Artist, Album, Song
from music.forms import ArtistForm, AlbumForm, SongForm


class CreateArtist(CreateView):
    '''Create an artist view.'''
    model = Artist
    form_class = ArtistForm


class CreateAlbum(CreateView):
    '''Create an artist view.'''
    model = Album
    form_class = AlbumForm


class CreateSong(CreateView):
    '''Create an artist view.'''
    model = Song
    form_class = SongForm
