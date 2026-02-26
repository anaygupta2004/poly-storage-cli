import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import Mock, patch

from poly_storage_cli.main import main


class CLITests(unittest.TestCase):
    @patch("poly_storage_cli.main.PolyStorageClient")
    def test_health_command(self, client_cls):
        client = client_cls.return_value
        client.system.health = Mock(return_value={"status": "healthy"})

        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = main(["health"])

        self.assertEqual(code, 0)
        data = json.loads(stdout.getvalue())
        self.assertEqual(data["status"], "healthy")

    @patch("poly_storage_cli.main.PolyStorageClient")
    def test_polymarket_market_data_command(self, client_cls):
        client = client_cls.return_value
        client.polymarket.get_market_data = Mock(return_value={"data_count": 1})

        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = main(
                [
                    "polymarket",
                    "market-data",
                    "--condition-id",
                    "0xabc",
                    "--date",
                    "2026-02-13",
                    "--offset",
                    "10",
                    "--limit",
                    "20",
                ]
            )

        self.assertEqual(code, 0)
        client.polymarket.get_market_data.assert_called_once_with(
            condition_id="0xabc",
            date="2026-02-13",
            offset=10,
            limit=20,
        )

    def test_missing_command_returns_error_code(self):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            code = main([])
        self.assertEqual(code, 2)
        self.assertIn("usage:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
