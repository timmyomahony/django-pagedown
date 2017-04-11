from django import forms

from music.models import Artist, Album, Song

from pagedown.widgets import AdminPagedownWidget, PagedownWidget


class AdminAlbumForm(forms.ModelForm):
    '''An admin form for Albums'''
    descripion = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Album
        fields = '__all__'


class ArtistForm(forms.ModelForm):
    '''A form for Artists'''
    about = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Artist
        fields = '__all__'


class AlbumForm(forms.ModelForm):
    '''A form for Albums'''
    descripion = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Album
        fields = '__all__'


class SongForm(forms.ModelForm):
    '''A form for Songs'''
    descripion = forms.CharField(widget=PagedownWidget())
    lyrics = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Song
        fields = '__all__'
