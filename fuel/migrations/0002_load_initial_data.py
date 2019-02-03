from django.conf import settings
from django.db import migrations


def load_initial_data(apps, schema_editor):
    Fuel = apps.get_model('fuel', 'Fuel')
    Fuel.objects.bulk_create([
        Fuel(pk=1, name='Gazole'),
        Fuel(pk=2, name='SP95'),
        Fuel(pk=3, name='E85'),
        Fuel(pk=4, name='GPLc'),
        Fuel(pk=5, name='E10'),
        Fuel(pk=6, name='SP98'),
    ])


def unload_initial_data(apps, schema_editor):
    # Nothing here, just make the data migration reversible.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('fuel', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, unload_initial_data)
    ]
