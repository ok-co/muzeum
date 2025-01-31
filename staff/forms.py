from django import forms
from muzeum.models import Artist, Gallery, Room, Institution, Exhibits

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['first_name', 'last_name', 'birth_year', 'death_year']


    def clean(self):
        cleaned_data = super().clean()
        birth_year = cleaned_data.get('birth_year')
        death_year = cleaned_data.get('death_year')

        if death_year and death_year < birth_year:
            raise forms.ValidationError('Data śmierci nie może być wcześniejsza niż data urodzenia')

        return cleaned_data

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['name']


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if Gallery.objects.filter(name=name).exists():
            raise forms.ValidationError('Galeria o takiej nazwie już istnieje') 

        return cleaned_data

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['id', 'gallery']


    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data.get('id')

        if Room.objects.filter(id=id).exists():
            raise forms.ValidationError('Pokój o takim numerze już istnieje') 

        return cleaned_data

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'city']


class ExhibitForm(forms.ModelForm):
    class Meta:
        model = Exhibits
        fields = ['title', 'type', 'height', 'width', 'weight', 'valuable', 'artist']

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get('height')
        width = cleaned_data.get('width')
        weight = cleaned_data.get('weight')

        if height < 0 or width < 0 or weight < 0:
            raise forms.ValidationError('Wartości muszą być większe od zera')

        return cleaned_data

class MoveForm(forms.ModelForm):
    room_id = forms.IntegerField()
    exhibit_id = forms.IntegerField()

    class Meta:
        model = Exhibits
        fields = ['room_id', 'exhibit_id']

        