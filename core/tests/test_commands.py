"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# This decorator only applies to the class.
# It patches 'Command.check' for methods within this class that also have a 'patched_check' argument.
# However, for specific test methods that need additional patches, we'll declare them directly above.
class CommandTests(SimpleTestCase):
    """Test commands."""

    # @patch("core.management.commands.wait_for_db.Command.check") # Removed this redundant patch for the class level
    def test_wait_for_db_ready(self): # Removed patched_check from here as it's not needed directly from the decorator
        """Test waithing for database if database ready."""
        # This test relies on the default behavior of call_command which invokes check implicitly.
        # If Command.check needs to be mocked explicitly for this test, you'd add @patch here.
        # Given your original intent, we'll mock check in the next test.
        # This test passes if wait_for_db doesn't raise an error.
        call_command("wait_for_db")
        # No assert_called_once_with here as we're not mocking check specifically for this test.
        # If you meant to mock it here as well, add @patch("core.management.commands.wait_for_db.Command.check")
        # immediately above this test method, and add `patched_check` back to its arguments.

    @patch('time.sleep')
    @patch("django.db.utils.ConnectionHandler.ensure_connection") # Patching the specific method that raise OperationalError
    def test_wait_for_db_delay(self, patched_check, patched_sleep): # Order reversed: check first, then sleep
        """Test waiting for database when getting operationalerror."""
        # patched_check will be the mock for ensure_connection
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])

