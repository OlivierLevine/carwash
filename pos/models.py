from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import datetime
from lxml import etree
import pytz

from service.models import Service
from fuel.models import Fuel

from logging import getLogger


logger = getLogger('carwash.pos')


class Pos(models.Model):
    """A Point Of Sale structure."""
    "   id: the primary key"
    "   address: the POS address"
    "   zip: the POS zip code"
    "   city: the POS city"
    "   longitude: the POS longitude in GeoDecimal (WSG84)"
    "   latitude: the POS latitude in GeoDecimal (WSG84)"

    address = models.CharField(verbose_name=_("Adresse"), max_length=128)
    zip = models.CharField(verbose_name=_("Code Postal"), max_length=5)
    city = models.CharField(verbose_name=_("Ville"), max_length=128, null=True)
    longitude = models.FloatField(verbose_name=_("Longitude"))
    latitude = models.FloatField(verbose_name=_("Latitude"))

    updated_at = models.DateTimeField(verbose_name=_("Updated date"))

    class Meta:
        verbose_name = _("Point De Vente")
        verbose_name_plural = _("Points De Vente")

    def __str__(self):
        return str(self.id)

    @classmethod
    def import_file(cls, filename):
        tree = etree.parse(filename)
        for pos in tree.xpath("/pdv_liste/pdv"):
            try:
                pos_attributes = dict(pos.attrib)
                kwargs = dict(
                    id=pos_attributes["id"],
                    address=pos.find("adresse").text,
                    zip=pos_attributes["cp"],
                    city=pos.find("ville").text,
                    latitude=pos_attributes["latitude"],
                    longitude=pos_attributes["longitude"],
                    services=[],
                    fuels=[]
                )
                services = pos.find("services")
                for service in services:
                    kwargs['services'].append(service.text)
                for prix in pos.iter("prix"):
                    kwargs['fuels'].append(dict(prix.attrib))
                logger.info("Importing POS %s", dict(id=pos_attributes["id"]))
                Pos.import_pos(kwargs)
            except AttributeError as err:
                logger.error("Missing value: %s", err)

    @classmethod
    def import_pos(cls, args, **kwargs):
        latitute = float(args["latitude"]) / 100000
        longitude = float(args["longitude"]) / 100000
        pos, created = Pos.objects.update_or_create(
            id=args['id'],
            defaults={
                'id': args["id"],
                'address': args["address"],
                'zip': args["zip"],
                'city': args["city"],
                'latitude': latitute,
                'longitude': longitude,
                'updated_at': timezone.now(),
            },
        )
        for fuel in args['fuels']:
            AvailableFuel.import_fuel(pos, fuel)

        AvailableService.objects.filter(pos=pos).delete()
        for service in args['services']:
            AvailableService.import_service(pos, service)

        return pos


class AvailableService(models.Model):
    """Available services inside the pos."""
    "   id: the primary key"
    "   pos: the POS (Foreign Jey)"
    "   service: the service (Foreign Key)"

    pos = models.ForeignKey(Pos, db_index=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Service Disponible")
        verbose_name_plural = _("Services Disponibles")

    def __str__(self):
        return "{} => {}".format(str(self.pos.id), self.service.name)

    @classmethod
    def import_service(cls, pos, service):
        existing_service = Service.objects.filter(name=service).first()
        if existing_service is not None:
            AvailableService.objects.update_or_create(
                pos=pos,
                service=existing_service,
                defaults={},
            )


class AvailableFuel(models.Model):
    """Available fuel with price."""
    "   id: the primary key"
    "   pos: the POS (Foreign Jey)"
    "   fuel: the fuel (Foreign Key)"

    pos = models.ForeignKey(Pos, db_index=True, on_delete=models.CASCADE)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    value = models.DecimalField(verbose_name=_("Prix"), max_digits=10, decimal_places=3)
    updated_at = models.DateTimeField(verbose_name=_("Updated date"))

    class Meta:
        verbose_name = _("Carburant Disponible")
        verbose_name_plural = _("Carburants Disponibles")

    def __str__(self):
        return "{} => {}".format(str(self.pos.id), self.fuel.name)

    @classmethod
    def import_fuel(cls, pos, fuel):
        maj = datetime.strptime(fuel["maj"], '%Y-%m-%d %H:%M:%S')
        timezoneConverter = pytz.timezone('Europe/Paris')
        timezone_maj = timezoneConverter.localize(maj)
        existing_fuel = AvailableFuel.objects.filter(
            pos=pos,
            fuel_id=fuel['id'],
            updated_at__gte=timezone_maj
        ).first()
        if existing_fuel is not None:
            logger.debug(
                "A record already exists with greater date"
            )
            return
        AvailableFuel.objects.update_or_create(
            pos=pos,
            fuel_id=fuel['id'],
            defaults={
                'value': fuel["valeur"],
                'updated_at': timezone_maj,
            },
        )
