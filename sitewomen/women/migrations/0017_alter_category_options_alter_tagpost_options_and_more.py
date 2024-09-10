# Generated by Django 4.2.1 on 2024-09-10 18:28

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0016_uploadfiles_delete_uploadedfile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='tagpost',
            options={'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
        migrations.AlterModelOptions(
            name='women',
            options={'ordering': ['time_create'], 'verbose_name': 'Женщина', 'verbose_name_plural': 'Женщины'},
        ),
        migrations.AlterField(
            model_name='women',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Текст статьи'),
        ),
    ]
