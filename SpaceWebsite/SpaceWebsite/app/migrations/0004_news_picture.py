# Generated by Django 3.2 on 2021-11-24 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20211118_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='picture',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
