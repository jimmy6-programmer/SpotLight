# Generated by Django 5.0.7 on 2024-11-29 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfomer',
            name='security_code',
            field=models.CharField(blank=True, default='vhyoiR', max_length=8, null=True, unique=True),
        ),
    ]
