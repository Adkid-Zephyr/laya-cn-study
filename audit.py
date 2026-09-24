"""Offline checksum, denominator, label alignment and metric audit (stdlib only)."""
import gzip
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def audit(root=ROOT):
    source = json.loads((root / 'SOURCE.json').read_text())
    for entry in source['files']:
        assert hashlib.sha256((root / entry['path']).read_bytes()).hexdigest() == entry['sha256'], entry['path']
    expected = json.loads((root / 'expected_metrics.json').read_text())
    groups = defaultdict(list)
    identities = defaultdict(dict)
    with gzip.open(root / 'predictions.jsonl.gz', 'rt', encoding='utf8') as stream:
        for line in stream:
            row = json.loads(line)
            p, y = row['p'], row['y']
            assert isinstance(y, int) and 0 <= y < len(p)
            assert all(math.isfinite(v) and 0 <= v <= 1 for v in p)
            assert abs(sum(p) - 1) < 1e-6
            assert len(row['label_names']) == len(p)
            identity = (row['source'], row['language'], row['id'])
            key = (row['model'], row['panel'])
            assert identity not in identities[key]
            identities[key][identity] = (y, row['label_names'])
            src = row['source']
            group = src
            if src in ['massive', 'massive_binary']:
                group = ('binary_' if src == 'massive_binary' else 'massive_') + ('zh' if row['language'].startswith('zh') else 'en')
            groups[row['model'], row['panel'], group].append(row)
    assert set(groups) == {(m, panel, g) for m, panels in expected.items() for panel, metrics in panels.items() for g in metrics}
    for panel in ['test_original', 'test_adapted', 'dev_t2_original']:
        for model in expected:
            assert identities[model, panel] == identities['laya', panel]
    for (model, panel, group), rows in groups.items():
        gold = expected[model][panel][group]
        assert len(rows) == gold['n']
        correct = sum(max(range(len(r['p'])), key=r['p'].__getitem__) == r['y'] for r in rows)
        assert abs(correct / len(rows) - gold['accuracy']) < 1e-10
        if group == 'crosswoz':
            pairs = [(max(range(len(r['p'])), key=r['p'].__getitem__), r['y']) for r in rows]
            tp = sum(p == y == 1 for p, y in pairs)
            fp = sum(p == 1 and y == 0 for p, y in pairs)
            fn = sum(p == 0 and y == 1 for p, y in pairs)
            assert abs(2 * tp / max(1, 2 * tp + fp + fn) - gold['micro_f1']) < 1e-10
        if group == 't2':
            rps = sum(sum((sum(r['p'][:i + 1]) - int(r['y'] <= i)) ** 2 for i in range(3)) / 3 for r in rows) / len(rows)
            assert abs(rps - gold['rps']) < 1e-10
    feishu = json.loads((root / 'feishu.json').read_text())['rows']
    assert len(feishu) == 128 and len({(r['id'], r['mode']) for r in feishu}) == 128
    for mode, expected_correct, false, missed in [('choice', 25, 23, 1), ('four_noul', 19, 0, 30)]:
        rows = [r for r in feishu if r['mode'] == mode]
        assert len(rows) == 64
        for row in rows:
            answers = row['answers']
            if mode == 'choice':
                answer = answers['category']
                prediction = max(answer['probabilities'], key=answer['probabilities'].__getitem__)
                assert prediction == answer['choice']
            else:
                related, action, urgent, value = [answers[k]['noul'] for k in ['related', 'action', 'urgent', 'value']]
                assert all(math.isfinite(x) and 0 <= x <= 1 for x in [related, action, urgent, value])
                prediction = ('urgent' if urgent >= .75 else 'todo') if related >= .5 and action >= .5 else ('valuable' if related >= .5 and value >= .5 else 'noise')
            assert prediction == row['predicted']
        assert sum(r['predicted'] == r['expected'] for r in rows) == expected_correct
        assert sum(r['expected'] in ['noise', 'valuable'] for r in rows) == 32
        assert sum(r['expected'] in ['noise', 'valuable'] and r['predicted'] in ['todo', 'urgent'] for r in rows) == false
        assert sum(r['expected'] in ['todo', 'urgent'] and r['predicted'] in ['noise', 'valuable'] for r in rows) == missed
    return {'prediction_rows': sum(map(len, groups.values())), 'feishu_rows': len(feishu), 'status': 'PASS'}


if __name__ == '__main__':
    print(json.dumps(audit()))
