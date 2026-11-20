"""Check the installed forwarder entry point and the disk warning boundary."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import importlib.util

BIN = Path(__file__).resolve().parents[1] / 'personal-lab/apps/personal_ops_uf/bin'
spec = importlib.util.spec_from_file_location("capacity", BIN / "capacity.py")
capacity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capacity)


class PilotTests(unittest.TestCase):
    def test_repair_and_threshold(self):
        for available, expected in [(4799356928, "warning"), (15011602432, "ok"),
                                    (6 * 1024**3 - 1, "warning"), (6 * 1024**3, "ok")]:
            with self.subTest(available=available):
                self.assertEqual(capacity.capacity_state(available), expected)

    def test_scripted_input(self):
        with tempfile.TemporaryDirectory() as directory:
            run = subprocess.run([str(BIN / 'collect.sh')], cwd='/',
                                 env={**os.environ, 'SPLUNK_HOME': directory},
                                 capture_output=True, text=True, check=True)
            event = json.loads(run.stdout)
            self.assertGreaterEqual(event['available_bytes'], 0)
            self.assertEqual(event['capacity_state'], capacity.capacity_state(event['available_bytes']))
            failed = subprocess.run([str(BIN / 'collect.sh')],
                                    env={**os.environ, 'SPLUNK_HOME': directory + '/missing'},
                                    capture_output=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertFalse(failed.stdout)
