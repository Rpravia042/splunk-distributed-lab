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

    def test_status_table_uses_index_time(self):
        import xml.etree.ElementTree as ET
        view = BIN.parents[1] / 'personal_ops_sh/default/data/ui/views/personal_health.xml'
        tables = ET.parse(view).getroot().findall('.//table/search')
        self.assertEqual(len(tables), 1)
        query = tables[0].findtext('query')
        for fragment in ('_index_earliest=-15m', 'latest=+1d', 'sort 0 - _indextime - _time', 'dedup host',
                         'last_indexed=_indextime, lag=_indextime-_time',
                         '"Clock ahead"', '"Arriving late"'):
            self.assertIn(fragment, query)
        self.assertNotIn('latest=now', query)
        self.assertEqual(tables[0].findtext('refresh'), '60s')

    def test_simulation_dry_run(self):
        script = BIN.parents[2] / 'sim-panel-cases.sh'
        run = subprocess.run(['sh', str(script), 'ahead600', '600', '2'],
                             env={**os.environ, 'SIM_DRY_RUN': '1'},
                             capture_output=True, text=True, check=True)
        from datetime import datetime, timezone
        lines = run.stdout.splitlines()
        self.assertEqual(len(lines), 2)
        for line in lines:
            event = json.loads(line)
            shift = (datetime.strptime(event['timestamp'], '%Y-%m-%dT%H:%M:%S%z')
                     - datetime.now(timezone.utc)).total_seconds()
            self.assertTrue(590 <= shift <= 601, shift)
            self.assertTrue(event['synthetic'])
        bad = subprocess.run(['sh', str(script), 'bad host', '600'],
                             env={**os.environ, 'SIM_DRY_RUN': '1'}, capture_output=True)
        self.assertNotEqual(bad.returncode, 0)
