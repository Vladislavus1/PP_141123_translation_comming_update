# Generated by Django 4.2.1 on 2023-08-22 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='user_id_number',
            field=models.IntegerField(default=0),
        ),
    ]
