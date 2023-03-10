# Generated by Django 3.2 on 2021-11-18 16:19

from django.db import migrations, models
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_commontext_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('text', djrichtextfield.models.RichTextField(verbose_name='Текст')),
                ('publishing_date', models.DateTimeField(verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
        migrations.AlterModelOptions(
            name='commontext',
            options={'verbose_name': 'Текст для раздела', 'verbose_name_plural': 'Тексты для разделов'},
        ),
    ]
