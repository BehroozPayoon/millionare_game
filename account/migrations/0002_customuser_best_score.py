# Generated by Django 5.0.6 on 2024-07-04 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='best_score',
            field=models.IntegerField(default=0),
        ),
    ]