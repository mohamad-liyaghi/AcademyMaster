# Generated by Django 4.2.1 on 2023-06-10 12:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=32, unique=True)),
                ('avatar', models.ImageField(default='assets/pictures/profiles/default-avatar.jpg', upload_to='avatars/')),
                ('birth_date', models.DateField()),
                ('address', models.CharField(max_length=150)),
                ('passport_id', models.CharField(max_length=15)),
                ('phone_number', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator('^\\+98\\d{10}$')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'db_table': 'profiles',
            },
        ),
    ]