# Generated by Django 4.0.1 on 2022-02-09 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0008_remove_modelresult_tfidf_bigram_acc_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modelresult',
            old_name='tfidf_brigram_acc',
            new_name='tfidf_bigram_acc',
        ),
        migrations.RenameField(
            model_name='modelresult',
            old_name='tfidf_brigram_time',
            new_name='tfidf_bigram_time',
        ),
    ]
