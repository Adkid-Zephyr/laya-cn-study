import gzip
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from audit import ROOT, audit


class AuditTests(unittest.TestCase):
    def test_archive(self):
        self.assertEqual(audit()['prediction_rows'], 31200)

    def test_missing_row_even_with_updated_checksum(self):
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder)
            for name in ['SOURCE.json', 'expected_metrics.json', 'predictions.jsonl.gz', 'feishu.json']:
                shutil.copy(ROOT / name, dest / name)
            with gzip.open(dest / 'predictions.jsonl.gz', 'rt') as stream:
                rows = list(stream)
            with gzip.open(dest / 'predictions.jsonl.gz', 'wt') as stream:
                stream.writelines(rows[1:])
            source = json.loads((dest / 'SOURCE.json').read_text())
            for f in source['files']:
                f['sha256'] = hashlib.sha256((dest / f['path']).read_bytes()).hexdigest()
            (dest / 'SOURCE.json').write_text(json.dumps(source))
            with self.assertRaises(AssertionError):
                audit(dest)

    def test_tampered_file(self):
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder)
            for name in ['SOURCE.json', 'expected_metrics.json', 'predictions.jsonl.gz', 'feishu.json']:
                shutil.copy(ROOT / name, dest / name)
            (dest / 'feishu.json').write_text('{}')
            with self.assertRaises(AssertionError):
                audit(dest)


if __name__ == '__main__':
    unittest.main()
