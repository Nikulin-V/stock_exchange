# Generated by Django 4.0.4 on 2022-05-07 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название отрасли')),
            ],
            managers=[
                ('industries', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно')),
                ('industry', models.ManyToManyField(related_name='companies', to='companies.industry', verbose_name='Отрасль')),
                ('shareholders', models.ManyToManyField(related_name='shareholders', to=settings.AUTH_USER_MODEL, verbose_name='Акционеры')),
            ],
            managers=[
                ('companies', django.db.models.manager.Manager()),
            ],
        ),
    ]