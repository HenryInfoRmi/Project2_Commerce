# Generated by Django 3.1.7 on 2021-03-16 06:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210316_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auct_list',
            name='date_act',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='auct_list',
            name='name_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment_auct',
            name='date_comment',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 16, 3, 16, 18, 980755)),
        ),
    ]
