# Generated by Django 4.0.1 on 2022-02-09 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0003_alter_modelresult_tfidf_brigram_acc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelresult',
            name='created_at',
        ),
    ]
