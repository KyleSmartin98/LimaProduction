# Generated by Django 3.2.9 on 2022-01-06 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FreeLims', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='criteria',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cheminventory',
            name='quarantine',
            field=models.BooleanField(choices=[(True, 'Quarantine'), (False, 'Do Not Quarantine')], default=False),
        ),
        migrations.AlterField(
            model_name='sample',
            name='initiated',
            field=models.BooleanField(choices=[(True, 'Initiated'), (False, 'Not Initiated')], default=False),
        ),
    ]
