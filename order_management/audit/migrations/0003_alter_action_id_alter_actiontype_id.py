# Generated by Django 4.2.5 on 2023-09-20 11:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0002_alter_action_id_alter_actiontype_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='id',
            field=models.UUIDField(default=uuid.UUID('9626c060-e965-4f66-b76b-041902df5f20'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='actiontype',
            name='id',
            field=models.UUIDField(default=uuid.UUID('9626c060-e965-4f66-b76b-041902df5f20'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
