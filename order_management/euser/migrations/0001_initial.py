# Generated by Django 3.2.6 on 2021-12-14 19:58

import base.models
from django.db import migrations, models
import django.db.models.deletion
import euser.backend.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('corporate', '0001_initial'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EUser',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(help_text='System-wide identifier used to identify the admin for authentication', max_length=50, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('other_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(max_length=20, verbose_name='phone number')),
                ('email', models.CharField(max_length=50)),
                ('security_code', models.CharField(blank=True, max_length=150, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='User is currently active.', verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, help_text='User can login login to the dashboard.', verbose_name='staff')),
                ('is_superuser', models.BooleanField(default=False, help_text='User has full permissions on the admin dashboard.', verbose_name='super user')),
                ('language_code', models.CharField(default='en', max_length=5)),
                ('last_activity', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='last activity')),
                ('branch', models.ForeignKey(blank=True, help_text='The branch the user belongs to. Cannot be null unless super user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='corporate.branch')),
                ('checkoff_branch', models.ForeignKey(blank=True, help_text='The branch the user belongs to. Cannot be null unless super user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checkoff_branches', to='corporate.checkoffbranch')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', euser.backend.managers.EUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=35)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('simple_name', models.TextField(blank=True, max_length=255, null=True)),
                ('extendable_by_corporate', models.BooleanField(default=False)),
                ('extendable_by_service_provider', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euser.permission')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=35)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('is_corporate_role', models.BooleanField(default=False)),
                ('is_service_provider_role', models.BooleanField(default=False)),
                ('is_super_admin_role', models.BooleanField(default=False)),
                ('corporate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corporate.corporate')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='ExtendedEUserPermission',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('euser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='euser.euser')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='euser.permission')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'verbose_name': 'Extended Permission',
                'verbose_name_plural': 'Extended Permissions',
                'unique_together': {('euser', 'permission')},
            },
        ),
        migrations.CreateModel(
            name='EUserSecurityQuestion',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('answer_hash', models.CharField(max_length=255)),
                ('euser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_questions', to='euser.euser')),
                ('security_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.securityquestion')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'ordering': ('-date_created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EUserPassword',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('hashed_password', models.BooleanField(default=False, editable=False, verbose_name='is password hashed')),
                ('euser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_passwords', to='euser.euser')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'verbose_name': 'Password',
                'verbose_name_plural': 'Passwords',
                'ordering': ('-date_created',),
            },
        ),
        migrations.AddField(
            model_name='euser',
            name='permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='euser_set', related_query_name='euser', through='euser.ExtendedEUserPermission', to='euser.Permission'),
        ),
        migrations.AddField(
            model_name='euser',
            name='role',
            field=models.ForeignKey(blank=True, help_text='The role for the user belongs to. Cannot be null unless super user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='euser.role'),
        ),
        migrations.AddField(
            model_name='euser',
            name='state',
            field=models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state'),
        ),
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='euser.permission')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='euser.role')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'unique_together': {('role', 'permission')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='euser',
            unique_together={('id',)},
        ),
    ]
