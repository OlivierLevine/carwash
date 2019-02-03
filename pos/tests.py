from django.test import TestCase
from django.utils import timezone
from pos.models import Pos


class PosTests(TestCase):

    def test_pos_default(self):
        """
        Store and check fields
        """

        now = timezone.now()
        pos = Pos(
            id=123456,
            address="address",
            zip="zip",
            city="city",
            latitude=1234.5678,
            longitude=9876.5432,
            updated_at=now,
        )
        pos.save()

        saved_pos = Pos.objects.get(pk=123456)
        self.assertEqual(saved_pos.address, "address")
        self.assertEqual(saved_pos.zip, "zip")
        self.assertEqual(saved_pos.city, "city")
        self.assertEqual(saved_pos.latitude, 1234.5678)
        self.assertEqual(saved_pos.longitude, 9876.5432)
        self.assertEqual(saved_pos.updated_at, now)

    def test_pos_error_default(self):
        """
        Try to store a badly formated pos
        """

        now = timezone.now()
        pos = Pos(
            id=123456,
            address="address",
            zip="zip",
            city="city",
            latitude="AAAA",
            longitude=9876.5432,
            updated_at=now,
        )
        with self.assertRaises(ValueError):
            pos.save()
