from django.conf import settings
from django.core.management.base import BaseCommand
from modelCore.fakeData import importCityCounty, seedData, fakeData

class Command(BaseCommand):

    def handle(self, *args, **options):
        importCityCounty()
        seedData()
        fakeData()