"""
Django command to wait for the database to be available.
"""

import time

from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entry point for the command."""
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                # Check if the default database is available
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError):
                # If not available, print message and wait
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)
        # Once database is available, print success message
        self.stdout.write(self.style.SUCCESS("Database available!"))
