# Generated by Django 2.0.6 on 2018-07-05 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogcategory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategory',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
