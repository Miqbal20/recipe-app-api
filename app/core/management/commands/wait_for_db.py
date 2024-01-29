import time

from psycopg2 import OperationalError as pc2Error

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """ Wait for database to be available """

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Waiting for database...'))
        db_up = False
        while db_up == False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (pc2Error, OperationalError):
                self.stdout.write(self.style.WARNING("Database Unavailable, please wait for some moment..."))
                time.sleep(4)
                
        self.stdout.write(self.style.SUCCESS('Database Available\n'))

