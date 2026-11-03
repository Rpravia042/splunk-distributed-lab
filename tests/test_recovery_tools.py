"""Synthetic tests: no real lab data or credentials."""

import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from collect_node import collect
from sanitize import sanitize
from check_repo import issues_for_text


class SanitizationTests(unittest.TestCase):
    def test_sensitive_fields_and_multiline_key(self):
        value = 'synthetic-' + 'credential'
        label = 'pass4' + 'SymmKey'
        key_label = 'PRIVATE' + ' KEY'
        raw = label + ' = ' + value + '\n-----BEGIN ' + key_label + '-----\n' + value + '\n-----END ' + key_label + '-----\n'
        clean = sanitize(raw)
        self.assertNotIn(value, clean)
        self.assertIn('[REDACTED]', clean)

    def test_ips_email_url_and_literal_mapping(self):
        address = '.'.join(['192', '0', '2', '8'])
        email = 'person' + '@' + 'example.invalid'
        raw = 'host=' + address + '\n' + email + '\nhttps://' + 'name:fictional@' + 'example.invalid\nprivate-project'
        clean = sanitize(raw, {'private-project': '<PROJECT>'})
        for original in (address, email, 'name:fictional', 'private-project'):
            self.assertNotIn(original, clean)
        self.assertIn('<PROJECT>', clean)

    def test_encrypted_values_and_bearer(self):
        raw = 'value=' + '$' + '7$fictionalEncryptedValue\nAuthorization: Bearer fictionalBearer'
        clean = sanitize(raw)
        self.assertNotIn('fictionalEncryptedValue', clean)
        self.assertNotIn('fictionalBearer', clean)

    def test_normal_config_preserved(self):
        raw = '[tcpout]\ndefaultGroup = lab_indexer\n'
        self.assertEqual(raw, sanitize(raw))

    def test_cli_refuses_overwrite_and_invalid_map(self):
        script = Path(__file__).resolve().parents[1] / 'scripts/sanitize.py'
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            source, dest, mapping = base / 'input', base / 'output', base / 'map.json'
            source.write_text('[example]\n')
            dest.write_text('preserve me')
            result = subprocess.run([sys.executable, str(script), str(source), str(dest)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(dest.read_text(), 'preserve me')
            mapping.write_text('["invalid"]')
            result = subprocess.run([sys.executable, str(script), str(source), str(base / 'new'), '--map', str(mapping)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((base / 'new').exists())

    def test_scanner_flags_values_without_returning_them(self):
        key = 'pass' + 'word'
        value = 'fictional-sensitive-value'
        findings = issues_for_text(key + '=' + value)
        self.assertIn('sensitive assignment', findings)
        self.assertNotIn(value, str(findings))
        self.assertEqual(issues_for_text(key + '=[REDACTED]'), [])


class CollectionTests(unittest.TestCase):
    def test_bounded_capture_excludes_secret_stores_and_links(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder) / 'splunk'
            local = home / 'etc/system/local'
            local.mkdir(parents=True)
            (local / 'inputs.conf').write_text('[sample]\n')
            (local / 'passwords.conf').write_text('must stay out')
            (local / 'large.conf').write_text('x' * 80)
            (home / 'etc/auth').mkdir()
            (home / 'etc/auth/data.conf').write_text('must stay out')
            outside = Path(folder) / 'outside.conf'
            outside.write_text('outside data')
            (local / 'link.conf').symlink_to(outside)
            output = io.BytesIO()
            report = collect(home, output, max_file=50, max_total=60)
            self.assertEqual(len(report['files']), 1)
            self.assertTrue(report['errors'])  # symlink access was rejected
            output.seek(0)
            with tarfile.open(fileobj=output) as archive:
                self.assertEqual(set(archive.getnames()), {'etc/system/local/inputs.conf', 'collection-report.json'})
                summary = json.load(archive.extractfile('collection-report.json'))
                self.assertTrue(summary['skipped'])
                self.assertTrue(all(not n.startswith('/') and '..' not in n.split('/') for n in archive.getnames()))
            self.assertEqual((local / 'inputs.conf').read_text(), '[sample]\n')

    def test_missing_installation_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                collect(Path(folder), io.BytesIO())


if __name__ == '__main__':
    unittest.main()
