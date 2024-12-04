# Generated by Django 5.0.7 on 2024-12-02 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_advertisement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='banners/')),
                ('button_text_1', models.CharField(default='Get Ticket', max_length=50)),
                ('button_url_1', models.URLField()),
                ('button_text_2', models.CharField(default='Know More', max_length=50)),
                ('button_url_2', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='video',
            field=models.FileField(max_length=200, upload_to='ads/'),
        ),
    ]
