# Generated by Django 2.2 on 2019-05-25 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('build', '0003_auto_20190525_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='part',
            field=models.ForeignKey(help_text='Select part to build', limit_choices_to={'active': True, 'buildable': True, 'is_template': False}, on_delete=django.db.models.deletion.CASCADE, related_name='builds', to='part.Part'),
        ),
    ]
