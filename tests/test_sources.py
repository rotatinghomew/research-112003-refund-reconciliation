"""核对业务资料的格式与可关联性。"""
import csv
from pathlib import Path
import unittest

DATA = Path(__file__).resolve().parents[1] / 'data'
TABLES = {'quotes': ('line', 'order', 'category', 'merchant', 'gross', 'paid_weight'), 'payments': ('pay', 'order', 'leg', 'channel', 'received', 'amount'), 'awards': ('case', 'revision', 'line', 'pay', 'payer', 'amount', 'status', 'known', 'period'), 'movements': ('id', 'pay', 'payer', 'chan_ref', 'case_hint', 'state', 'amount', 'known', 'prior'), 'confirmations': ('id', 'observed', 'canonical', 'case', 'known', 'state'), 'signed_lines': ('report', 'line', 'case', 'party', 'period', 'payable', 'issued', 'signed'), 'cycles': ('period', 'effective', 'asof', 'state')}
RELATION = ('awards', 'pay', 'payments', 'pay')


class SourceContract(unittest.TestCase):
    def read(self, table):
        with (DATA / f'{table}.csv').open(encoding='utf-8', newline='') as file:
            return list(csv.DictReader(file))

    def test_shape(self):
        for name, columns in TABLES.items():
            with self.subTest(table=name):
                rows = self.read(name)
                self.assertTrue(rows)
                for row in rows:
                    self.assertEqual(tuple(row), columns)
                    self.assertNotIn(None, row.values())

    def test_references(self):
        left, left_key, right, right_key = RELATION
        self.assertLessEqual({row[left_key] for row in self.read(left)}, {row[right_key] for row in self.read(right)})

    def test_source_variation(self):
        flows = {row['id']: row for row in self.read('movements')}
        self.assertEqual(flows[flows['f2']['prior']]['amount'], flows['f2']['amount'])
        self.assertTrue(any(row['observed'] != row['canonical'] and int(row['known']) > 18 for row in self.read('confirmations')))
