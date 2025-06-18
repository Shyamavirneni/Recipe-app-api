"""
Tests for Django management commands.
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    """Test management commands."""

    @patch('core.management.commands.wait_for_db.Command.check')
    def test_wait_for_db_ready(self, mocked_check):
        """Test waiting for database when database is ready."""
        mocked_check.return_value = True

        call_command('wait_for_db')

        mocked_check.assert_called_once_with(databases=['default'])


    @patch('core.management.commands.wait_for_db.Command.check')
    @patch('time.sleep')
    def test_wait_for_db_delay(self, mocked_sleep, mocked_check):
        """Test waiting for database when getting OperationalError."""
        # Simulate 2 Psycopg2Error, 3 OperationalError, then True
        mocked_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(mocked_check.call_count, 6)
        mocked_check.assert_called_with(databases=['default'])
        