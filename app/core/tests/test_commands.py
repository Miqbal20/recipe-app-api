from unittest.mock import patch

from psycopg2 import OperationalError as pc2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTest(SimpleTestCase):
    """Test Waiting for Database ready"""

    def test_wait_for_db_ready(self, patched_check):
        patched_check.return_value = True
        call_command("wait_for_db")
        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for the database when getting an error"""

        # Simulate two pc2Error, one OperationalError, and then success
        patched_check.side_effect = [pc2Error] * 2 + \
            [OperationalError] + [True]
        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 4)
        patched_check.assert_called_with(databases=["default"])
