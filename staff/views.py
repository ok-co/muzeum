from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from muzeum.models import Gallery, Artist, History, Exhibits, Room, Institution
from .forms import ArtistForm, GalleryForm, RoomForm, InstitutionForm, ExhibitForm, MoveForm, LendForm
from datetime import datetime

def login_view(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard
        else:
            return render(request, 'staff/login.html', {'error': 'Błędy login lub hasło'})
    return render(request, 'staff/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'staff/dashboard.html')

@login_required(login_url='login')
def add_view(request):
    return render(request, 'staff/add.html')

@login_required(login_url='login')
def move_view(request):
    return render(request, 'staff/move.html')

@login_required(login_url='login')
def lend_view(request):
    if request.method == 'POST':
        form = LendForm(request.POST)
        if form.is_valid():
            exhibit_id = request.POST.get('exhibit_id')
            institution_id = request.POST.get('institution_id')

            exhibit = Exhibits.objects.get(id=exhibit_id)
            institution = Institution.objects.get(id=institution_id)

            last_status = History.objects.filter(exhibit=exhibit).order_by('-start_date').first()

            if last_status and last_status.status != 'wypozyczenie':
                History.objects.create(
                    status='wypozyczenie',
                    exhibit=exhibit,
                    institution=institution,
                    start_date=datetime.now()
                )

                messages.success(request, 'Eksponat został wypożyczony pomyślnie')
            else:
                messages.error(request, 'Wypożyczenie nie powiodło się')


    exhibits = Exhibits.objects.all().select_related('artist').all()
    institutions = Institution.objects.all()

    warehouse_exhibits = []

    for exhibit in exhibits:
        last_status = History.objects.filter(exhibit=exhibit).order_by('-start_date').first()
        if last_status and last_status.status != 'wystawa':
            warehouse_exhibits.append({
                'exhibit': exhibit,
                'status' : last_status.status,
            })


    context = {
        'exhibits': exhibits,
        'warehouse_exhibits': warehouse_exhibits,
        'institutions': institutions,
    }

    return render(request, 'staff/lend.html', context)

@login_required(login_url='login')
def add_exhibit_view(request):
    if request.method == 'POST':
        form = ExhibitForm(request.POST)
        if form.is_valid():
            form.save()
            History.objects.create(
                status='magazyn',
                exhibit=form.instance,
                start_date=datetime.now()
                )

            messages.success(request, 'Eksponat został dodany pomyślnie')
            return redirect('add_exhibit')
    else:
        form = ExhibitForm()

    
    return render(request, 'staff/add_exhibit.html', {'form': form, 'artists': Artist.objects.all()})

@login_required(login_url='login')
def add_artist_view(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artysta został dodany pomyślnie')
            return redirect('add_artist')

    else:
        form = ArtistForm()
        
    return render(request, 'staff/add_artist.html', {'form': form})

@login_required(login_url='login')
def add_gallery_view(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Galeria została dodana pomyślnie')
            return redirect('add_gallery')

    else:
        form = GalleryForm()

    return render(request, 'staff/add_gallery.html', {'form': form})

@login_required(login_url='login')
def add_room_view(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pokój został dodany pomyślnie')
            return redirect('add_room')

    else:
        form = RoomForm()

    return render(request, 'staff/add_room.html', {'form': form, 'galleries': Gallery.objects.all()})

@login_required(login_url='login')
def add_institution_view(request):
    if request.method == 'POST':
        form = InstitutionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instytucja została dodana pomyślnie')
            return redirect('add_institution')

    else:
        form = InstitutionForm()

    return render(request, 'staff/add_institution.html', {'form': form})

@login_required(login_url='login')
def warehouse_view(request):
    return render(request, 'staff/warehouse.html')


@login_required(login_url='login')
def move_view(request):
    if request.method == 'POST':
        form = MoveForm(request.POST)

        if form.is_valid():
            exhibit_id = request.POST.get('exhibit_id')
            room_id = request.POST.get('room_id')

            exhibit = Exhibits.objects.get(id=exhibit_id)
            room = Room.objects.get(id=room_id)

            last_status = History.objects.filter(exhibit=exhibit).order_by('-start_date').first()

            if last_status and last_status.status != 'wypozyczenie':
                History.objects.create(
                    status='wystawa',
                    exhibit=exhibit,
                    room=room,
                    gallery=room.gallery,
                    start_date=datetime.now()
                )

                messages.success(request, 'Eksponat został przeniesiony pomyślnie')
            else:
                messages.error(request, 'Przeniesienie nie powiodło się')
        
        else:
            messages.error(request, 'Przeniesienie nie powiodło się', extra_tags='danger')


        return redirect('move')


    exhibits = Exhibits.objects.all().select_related('artist').all()

    available_exhibits = []

    for exhibit in exhibits:
        last_status = History.objects.filter(exhibit=exhibit).order_by('-start_date').first()
        if last_status and last_status.status != 'wypozyczenie':
            available_exhibits.append({
                'exhibit': exhibit,
                'status' : last_status.status,
            })

    rooms = Room.objects.select_related('gallery').order_by('id').all()

    context = {
        'exhibits': exhibits,
        'available_exhibits': available_exhibits,
        'rooms': rooms,
    }

    return render(request, 'staff/move.html', context)

@login_required(login_url='login')
def move_to_warehouse(request):
    if request.method == 'POST':
        exhibit_id = request.POST.get('exhibit_id')

        exhibit = Exhibits.objects.get(id=exhibit_id)

        last_status = History.objects.filter(exhibit=exhibit).order_by('-start_date').first()

        if last_status and last_status.status != 'wypozyczenie':
            History.objects.create(
                status='magazyn',
                exhibit=exhibit,
                start_date=datetime.now()
            )

            messages.success(request, 'Eksponat został przeniesiony do magazynu')
        else:
            messages.error(request, 'Przeniesienie nie powiodło się')

        return redirect('move')

    return redirect('move')

@login_required(login_url='login')
def request_back(request):
    if request.method == 'POST':
        exhibit_id = request.POST.get('exhibit_id')

        exhibit = Exhibits.objects.get(id=exhibit_id)
        last_status = History.objects.filter(exhibit=exhibit).order_by('-start_date').first()

        if last_status:
            last_status.end_date = datetime.now()
            last_status.save()

        if last_status and last_status.status == 'wypozyczenie':
            History.objects.create(
                status='magazyn',
                exhibit=exhibit,
                start_date=datetime.now()
            )

            messages.success(request, 'Eksponat został zwrócony do magazynu')
        else:
            messages.error(request, 'Zwrócenie nie powiodło się')

        return redirect('lend')

    return redirect('lend')