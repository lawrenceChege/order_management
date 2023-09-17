# Generated by Django 4.2.5 on 2023-09-17 05:07

import base.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.UUID('0650689a-d14b-737b-8000-1441967d8d03'), editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=35)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ('name',),
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.UUID('0650689a-d14b-737b-8000-1441967d8d03'), editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=35)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(max_length=10)),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'verbose_name_plural': 'Currencies',
                'abstract': False,
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.UUID('0650689a-d14b-737b-8000-1441967d8d03'), editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=35)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'abstract': False,
                'unique_together': {('name',)},
            },
        ),
    ]
