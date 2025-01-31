from django.shortcuts import render
from muzeum.models import Exhibits, History, Artist, Gallery
from django.db.models import Q, F, Value
from django.db.models.functions import Concat

def home_view(request):
    return render(request, 'user/home.html')

def exhibits_view(request):
    query = request.GET.get('q')
    if query:
        exhibits = Exhibits.objects.annotate(
            full_name=Concat(F('artist__first_name'), Value(' '), F('artist__last_name'))
        ).filter(
            Q(title__icontains=query) |
            Q(full_name__icontains=query) |
            Q(type__icontains=query)
        )
    else:
        exhibits = Exhibits.objects.all().select_related('artist').all()

    available_exhibits = []
    borrowed_exhibits = []

    for exhibit in exhibits:
        last_status = History.objects.filter(exhibit=exhibit).order_by('-start_date').first()
        if last_status and last_status.status == 'wypozyczenie':
            borrowed_exhibits.append({
                'exhibit': exhibit,
                'return_date': last_status.end_date
            })
        elif last_status and last_status.status == 'wystawa':
            room = last_status.room if last_status else None
            gallery = last_status.gallery if last_status else None

            available_exhibits.append({
                'exhibit': exhibit,
                'room': room,
                'gallery': gallery,
            })
    

    context = {
        'exhibits': exhibits,
        'available_exhibits': available_exhibits,
        'borrowed_exhibits': borrowed_exhibits,
        'query': query
    }

    return render(request, 'user/exhibits.html', context)

def artists_view(request):
    all_artists = Artist.objects.all()
    artists = []
    for artist in all_artists:
        if artist.death_year is None:
            artist.death_year = "Żyje"

        if Exhibits.objects.filter(artist=artist).exists():
            artists.append(artist)

    context = {
        'artists': artists
        
    }

    return render(request, 'user/artists.html', context)

def galleries_view(request):
    galleries = Gallery.objects.all()


    context = {
        'galleries': galleries
    }
    return render(request, 'user/galleries.html', context)