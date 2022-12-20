from django.core.management import BaseCommand
from django_school.parsing import parse


class Command(BaseCommand):

    def handle(self, *args, **options):
        parse.add_rates()