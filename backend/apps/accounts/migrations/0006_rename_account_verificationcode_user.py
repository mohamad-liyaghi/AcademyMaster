# Generated by Django 4.2.1 on 2023-07-04 09:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_remove_account_role"),
    ]

    operations = [
        migrations.RenameField(
            model_name="verificationcode",
            old_name="account",
            new_name="user",
        ),
    ]
