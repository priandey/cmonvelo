from random import randint, random, uniform
import os
from faker import Faker
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.core.files import File
from ...models import Owner, Bike

class Command(BaseCommand):
    help ='Populate the db with x users, earch one with 1 to 4 bikes associated'

    def add_arguments(self, parser):
        parser.add_argument('bike_number', nargs='+', type=int)

    def handle(self, *args, **options):
        fake = Faker(locale='fr-FR')
        bike_count = 0

        while bike_count < options['bike_number'][0]:
            try:
                new_owner = Owner.objects.create(
                    username=fake.name(),
                    email=fake.email(),
                )
            except IntegrityError:
                pass
            for i in range(randint(1,4)):
                bike = Bike.objects.create(
                    owner=new_owner,
                    name=fake.word(),
                    robbed=random() > 0.5,
                    reference=fake.isbn10(),
                )
                if bike.robbed:
                    bike.robbed_location = {
                        'latitude': str(round(uniform(43.604500, 50.954468), 6)),
                        'longitude': str(round(uniform(-4.486076, 7.2619532), 6)),
                    }
                    bike.set_robbery_date()
                    bike.save()
            bike_count += 1
