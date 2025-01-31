from django.contrib import admin
from django.urls import path, include
from staff import views as staff_views
from user import views as user_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', staff_views.login_view, name='login'),
    path('logout/', staff_views.logout_view, name='logout'),
    path('dashboard/', staff_views.dashboard_view, name='dashboard'),
    path('home/', user_views.home_view, name='home'),
    path('exhibits/', user_views.exhibits_view, name='exhibits'),
    path('artists/', user_views.artists_view, name='artists'),
    path('galleries/', user_views.galleries_view, name='galleries'),
    path('add', staff_views.add_view, name='add'),
    path('move', staff_views.move_view, name='move'),
    path('lend', staff_views.lend_view, name='lend'),
    path('add_exhibit/', staff_views.add_exhibit_view, name='add_exhibit'),
    path('add_artist/', staff_views.add_artist_view, name='add_artist'),
    path('add_gallery/', staff_views.add_gallery_view, name='add_gallery'),
    path('add_room/', staff_views.add_room_view, name='add_room'),
    path('add_institution/', staff_views.add_institution_view, name='add_institution'),
    path('move_to_warehoues/', staff_views.move_to_warehouse, name='move_to_warehouse'),


    
    path('', RedirectView.as_view(url='/home/', permanent=True))
]
