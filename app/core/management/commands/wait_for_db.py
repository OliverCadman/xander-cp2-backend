from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import BaseCommand
import time


class Command(BaseCommand):
    """Custom command to wait for db ready"""
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Waiting for database')
        db_up = False
        
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write(
                    self.style.ERROR(
                        'Database unavailable. Waiting one second...'
                    )
                )
                time.sleep(1)
            self.stdout.write(
                self.style.SUCCESS(
                    'Database available!'
                )
            )
