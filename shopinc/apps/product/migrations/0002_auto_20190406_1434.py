# Generated by Django 2.1.7 on 2019-04-06 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.ImageField(default='', upload_to='images'),
            preserve_default=False,
        ),
    ]
