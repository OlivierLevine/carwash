from django.conf import settings
from django.db import migrations


def load_initial_data(apps, schema_editor):
    Service = apps.get_model('service', 'Service')
    Service.objects.bulk_create([
        Service(name='Aire de camping-cars'),
        Service(name='Automate CB'),
        Service(name='Automate CB 24/24'),
        Service(name='Bar'),
        Service(name='Boutique alimentaire'),
        Service(name='Boutique non alimentaire'),
        Service(name='Douches'),
        Service(name='GNV'),
        Service(name='Lavage automatique'),
        Service(name='Lavage manuel'),
        Service(name='Laverie'),
        Service(name='Piste poids lourds'),
        Service(name='Relais colis'),
        Service(name='Restauration sur place'),
        Service(name='Station de gonflage'),
        Service(name='Toilettes publiques'),
        Service(name='Vente d\'additifs carburants'),
        Service(name='Vente de fioul domestique'),
        Service(name='Vente de gaz domestique (Butane, Propane)'),
        Service(name='Wifi'),
    ])


def unload_initial_data(apps, schema_editor):
    # Nothing here, just make the data migration reversible.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, unload_initial_data)
    ]
