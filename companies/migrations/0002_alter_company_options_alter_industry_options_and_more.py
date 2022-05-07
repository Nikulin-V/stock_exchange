# Generated by Django 4.0.4 on 2022-05-07 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Компания', 'verbose_name_plural': 'Компании'},
        ),
        migrations.AlterModelOptions(
            name='industry',
            options={'verbose_name': 'Отрасль', 'verbose_name_plural': 'Отрасли'},
        ),
        migrations.RemoveField(
            model_name='company',
            name='industry',
        ),
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='companies', to='companies.industry', verbose_name='Отрасль'),
            preserve_default=False,
        ),
    ]
