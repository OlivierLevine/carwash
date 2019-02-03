from django.test import TestCase
from fuel.models import Fuel


class FuelTests(TestCase):

    def test_fuel_default(self):
        """
        Store and check fields
        """

        fuel = Fuel(
            id=123456,
            name="name",
        )
        fuel.save()

        saved_fuel = Fuel.objects.get(pk=123456)
        self.assertEqual(saved_fuel.name, "name")
