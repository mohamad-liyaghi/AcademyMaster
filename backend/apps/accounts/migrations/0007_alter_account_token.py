# Generated by Django 4.2.1 on 2023-07-09 10:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_rename_account_verificationcode_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
