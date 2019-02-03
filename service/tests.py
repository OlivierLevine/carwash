from django.test import TestCase
from service.models import Service


class ServiceTests(TestCase):

    def test_service_default(self):
        """
        Store and check fields
        """

        service = Service(
            id=123456,
            name="name",
        )
        service.save()

        saved_service = Service.objects.get(pk=123456)
        self.assertEqual(saved_service.name, "name")
