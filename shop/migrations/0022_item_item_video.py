# Generated by Django 3.2 on 2021-05-09 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_alter_item_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_video',
            field=models.FileField(blank=True, upload_to='items_videos'),
        ),
    ]