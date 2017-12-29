# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-27 23:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='wishitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='poke',
            name='poked',
        ),
        migrations.RemoveField(
            model_name='poke',
            name='poker',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='bday',
            new_name='date_hired',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='email',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='alias',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='poke_count',
        ),
        migrations.RemoveField(
            model_name='user',
            name='poked_by_count',
        ),
        migrations.DeleteModel(
            name='Poke',
        ),
        migrations.AddField(
            model_name='wishitem',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creates', to='users.User'),
        ),
        migrations.AddField(
            model_name='wishitem',
            name='wished_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishes', to='users.User'),
        ),
    ]