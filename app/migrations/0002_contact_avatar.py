# Generated by Django 5.0 on 2025-01-12 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='avatar',
            field=models.ImageField(default=1, upload_to='avatars/'),
            preserve_default=False,
        ),
    ]
