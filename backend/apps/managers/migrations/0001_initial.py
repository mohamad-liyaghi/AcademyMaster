# Generated by Django 4.2.1 on 2023-06-13 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_date', models.DateTimeField(auto_now_add=True)),
                ('promoted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promoted_managers', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Manager',
                'verbose_name_plural': 'Managers',
                'db_table': 'managers',
                'permissions': [('promote_manager', 'Can promote a user to manager'), ('demote_manager', 'Can demote a manager to user')],
            },
        ),
    ]
