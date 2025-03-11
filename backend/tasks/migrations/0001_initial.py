# Generated by Django 5.1.6 on 2025-03-11 13:59

import django.db.models.deletion
import tasks.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.CharField(default=tasks.models.generate_id, editable=False, max_length=16, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.CharField(default=tasks.models.generate_id, editable=False, max_length=16, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
