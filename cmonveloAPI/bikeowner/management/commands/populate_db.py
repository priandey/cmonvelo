from random import randint, random
import os
from faker import Faker
from django.core.management.base import BaseCommand
from django.core.files import File
from bikeowner.models import Owner, Bike

class Command(BaseCommand):
    help ='Populate the db with x users, earch one with 1 to 4 bikes associated'

    def add_arguments(self, parser):
        parser.add_argument('bike_number', nargs='+', type=int)

    def handle(self, *args, **options):
        fake = Faker(locale='fr-FR')
        bike_count = 0

        while bike_count < options['bike_number'][0]:
            new_owner = Owner.objects.create(username=fake.name(), email=fake.email(), phone=fake.phone_number())
            for i in range(randint(1,4)):
                bike = Bike.objects.create(
                    owner=new_owner,
                    name=fake.word(),
                    robbed=random() > 0.5,
                    reference=fake.isbn10(),
                )
                if bike.robbed:
                    robbed_location = fake.local_latlng(country_code='FR', coords_only=True)
                    bike.robbed_location = {
                        'latitude': robbed_location[0],
                        'longitude': robbed_location[1],
                    }
                    bike.set_robbery_date()
                    bike.save()
            bike_count += 1
