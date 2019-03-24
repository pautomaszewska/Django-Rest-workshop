from django.core.management.base import BaseCommand
from movielist.fake_data import Populate


class Command(BaseCommand):
    help = 'Populate DB'

    def handle(self, *args, **options):
        populate = Populate()
        populate.setUp()