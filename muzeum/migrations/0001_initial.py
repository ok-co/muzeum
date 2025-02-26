# Generated by Django 4.2.17 on 2025-01-23 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('birth_year', models.IntegerField()),
                ('death_year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=64)),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('valuable', models.BooleanField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muzeum.artist')),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muzeum.gallery')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('magazyn', 'Magazyn'), ('wystawa', 'Wystawa'), ('wypozyczenie', 'Wypozyczenie')], max_length=16)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muzeum.artwork')),
                ('gallery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='muzeum.gallery')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='muzeum.institution')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='muzeum.room')),
            ],
        ),
        migrations.AddConstraint(
            model_name='artist',
            constraint=models.CheckConstraint(check=models.Q(('birth_year__gt', 0)), name='valid_birth_year'),
        ),
        migrations.AddConstraint(
            model_name='artist',
            constraint=models.CheckConstraint(check=models.Q(('death_year__gt', 0)), name='valid_death_year'),
        ),
        migrations.AddConstraint(
            model_name='artist',
            constraint=models.CheckConstraint(check=models.Q(('death_year__gt', models.F('birth_year'))), name='valid_age'),
        ),
        migrations.AddConstraint(
            model_name='history',
            constraint=models.CheckConstraint(check=models.Q(('end_date__gt', models.F('start_date'))), name='valid_period'),
        ),
        migrations.AddConstraint(
            model_name='history',
            constraint=models.CheckConstraint(check=models.Q(('status__in', ['magazyn', 'wystawa', 'wypozyczenie'])), name='valid_status'),
        ),
        migrations.AddConstraint(
            model_name='history',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('status', 'magazyn'), ('institution__isnull', True), ('gallery__isnull', True), ('room__isnull', True)), models.Q(('status', 'wystawa'), ('institution__isnull', True), ('gallery__isnull', False), ('room__isnull', False)), models.Q(('status', 'wypozyczenie'), ('institution__isnull', False), ('gallery__isnull', True), ('room__isnull', True)), _connector='OR'), name='valid_conditions'),
        ),
        migrations.AddConstraint(
            model_name='artwork',
            constraint=models.CheckConstraint(check=models.Q(('height__gt', 0)), name='valid_height'),
        ),
        migrations.AddConstraint(
            model_name='artwork',
            constraint=models.CheckConstraint(check=models.Q(('width__gt', 0)), name='valid_width'),
        ),
        migrations.AddConstraint(
            model_name='artwork',
            constraint=models.CheckConstraint(check=models.Q(('weight__gt', 0)), name='valid_weight'),
        ),
    ]
