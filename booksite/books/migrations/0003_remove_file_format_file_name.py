# Generated by Django 5.0.2 on 2024-04-02 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_file_remove_book_download_links_alter_book_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='format',
        ),
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(default=1, max_length=100),
        ),
    ]
