from django.db import models

class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_year = models.IntegerField()
    death_year = models.IntegerField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(birth_year__gt=0), name='valid_birth_year'),
            models.CheckConstraint(check=models.Q(death_year__gt=0), name='valid_death_year'),
            models.CheckConstraint(check=models.Q(death_year__gt=models.F('birth_year')), name='valid_age')
        ]

class Exhibits(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    height = models.IntegerField()
    width = models.IntegerField()
    weight = models.IntegerField()
    valuable = models.BooleanField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(height__gt=0), name='valid_height'),
            models.CheckConstraint(check=models.Q(width__gt=0), name='valid_width'),
            models.CheckConstraint(check=models.Q(weight__gt=0), name='valid_weight')
        ]

class Gallery(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

class Institution(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)

class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)

class History(models.Model):
    STATUS_CHOICES = [
        ('magazyn', 'Magazyn'),
        ('wystawa', 'Wystawa'),
        ('wypozyczenie', 'Wypozyczenie')
    ]

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    exhibit = models.ForeignKey(Exhibits, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(end_date__gt=models.F('start_date')), name='valid_period'),
            models.CheckConstraint(check=models.Q(status__in=['magazyn', 'wystawa', 'wypozyczenie']), name='valid_status'),
            models.CheckConstraint(
                check=(
                    (models.Q(status='magazyn') & models.Q(institution__isnull=True) & models.Q(gallery__isnull=True) & models.Q(room__isnull=True)) |
                    (models.Q(status='wystawa') & models.Q(institution__isnull=True) & models.Q(gallery__isnull=False) & models.Q(room__isnull=False)) |
                    (models.Q(status='wypozyczenie') & models.Q(institution__isnull=False) & models.Q(gallery__isnull=True) & models.Q(room__isnull=True))
                ),
                name='valid_conditions'
            )
        ]