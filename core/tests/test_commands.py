"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from django.db import connections # Import connections to correctly refer to it in patch


# This decorator only applies to the class.
# It patches 'Command.check' for methods within this class that also have a 'patched_check' argument.
# However, for specific test methods that need additional patches, we'll declare them directly above.
class CommandTests(SimpleTestCase):
    """Test commands."""

    # test_wait_for_db_ready does not explicitly mock Command.check,
    # as its purpose is to test the command runs without error when DB is available.
    def test_wait_for_db_ready(self):
        """Test waiting for database if database ready."""
        # For this test, we assume the database is ready, so `call_command` should succeed.
        # The `wait_for_db` command internally calls `connections['default'].ensure_connection()`.
        # Since no side_effect is provided for it in this test, it proceeds as if connection is successful.
        call_command("wait_for_db")


    @patch('time.sleep')
    # Patching the specific ensure_connection method on the 'default' connection object
    @patch("django.db.connections.default.ensure_connection") 
    def test_wait_for_db_delay(self, patched_ensure_connection, patched_sleep): # Renamed to reflect what is patched
        """Test waiting for database when getting operationalerror."""
        # Simulate OperationalError (Psycopg2Error for first two, then generic OperationalError)
        # followed by success (True)
        patched_ensure_connection.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        
        call_command("wait_for_db")
        
        # Verify that ensure_connection was called 6 times (2 Psycopg2Error + 3 OperationalError + 1 True)
        self.assertEqual(patched_ensure_connection.call_count, 6)
        
        # Verify that ensure_connection was always called with no arguments
        patched_ensure_connection.assert_called_with()

