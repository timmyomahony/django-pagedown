from django.conf.urls import url

from music.views import CreateArtist, CreateAlbum, CreateSong


urlpatterns = [
    url(r'^songs/create$', CreateSong.as_view()),
    url(r'^albums/create$', CreateAlbum.as_view()),
    url(r'^artists/create$', CreateArtist.as_view()),
]
