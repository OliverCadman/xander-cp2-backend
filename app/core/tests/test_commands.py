from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError

from unittest.mock import patch

from django.core.management import call_command

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Tests for management commands..."""

    def test_wait_for_db(self, patched_check):
        """Test waiting for db until ready"""
        patched_check.return_value = True
        call_command('wait_for_db')

        patched_check.assert_called_once_with(
            databases=['default']
        )
    
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for delay before database is up."""

        patched_check.side_effect = [Psycopg2Error] * 3 + \
            [OperationalError] * 2 + [True]
        
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(
            databases=['default']
        )
