# Generated by Django 3.2.6 on 2021-08-07 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Veterinaria', '0014_auto_20210806_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='activoServicio',
            field=models.BooleanField(blank=True, default=1),
        ),
    ]
