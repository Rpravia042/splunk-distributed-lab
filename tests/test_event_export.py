import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from verify_event_export import records, values, verify


class EventExportTests(unittest.TestCase):
    def test_count_and_metadata_checks(self):
        row = {'_raw': 'synthetic event\nsecond line', '_time': '2026-01-01T00:00:00Z',
               'host': 'example', 'source': 'synthetic', 'sourcetype': 'sample', 'index': 'lab'}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'export.json'
            path.write_text(json.dumps({'preview': False, 'result': row}) + '\n')
            self.assertEqual(verify(path, {'lab': 1})['status'], 'PASS')
            self.assertEqual(verify(path, {'lab': 2})['status'], 'FAIL')
            del row['_time']
            path.write_text(json.dumps({'results': [row]}))
            self.assertEqual(verify(path, {'lab': 1})['status'], 'FAIL')

    def test_truncation_report_retains_partial_counts(self):
        row = {'_raw': 'synthetic', '_time': '2026-01-01T00:00:00Z', 'host': 'sample',
               'source': 'sample', 'sourcetype': 'sample', 'index': 'lab'}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'truncated.json'
            path.write_text(json.dumps({'result': row}) + '\n{"result":')
            report = verify(path, {'lab': 1})
            self.assertEqual(report['status'], 'FAIL')
            self.assertEqual(report['counts'], {'lab': 1})
            self.assertFalse(report['valid_complete_json'])

    def test_truncated_and_preview_data_rejected(self):
        with self.assertRaises(ValueError):
            list(values(io.StringIO('{"result":')))
        with self.assertRaises(ValueError):
            list(records({'preview': True, 'result': {'_raw': 'sample'}}))

    def test_multiple_json_values_and_array(self):
        source = '[{"_raw":"one"}]\n{"results":[{"_raw":"two"}]}\n'
        result = [r for value in values(io.StringIO(source)) for r in records(value)]
        self.assertEqual([r['_raw'] for r in result], ['one', 'two'])


if __name__ == '__main__':
    unittest.main()
