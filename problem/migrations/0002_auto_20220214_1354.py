# Generated by Django 3.1 on 2022-02-14 13:54

from django.db import migrations, models
import utils.common


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='data',
            field=models.FileField(blank=True, null=True, upload_to=utils.common.upload_to_data),
        ),
        migrations.AlterField(
            model_name='problem',
            name='solution',
            field=models.FileField(blank=True, null=True, upload_to=utils.common.upload_to_solution),
        ),
        migrations.AlterField(
            model_name='problem',
            name='title',
            field=models.TextField(unique=True),
        ),
    ]
