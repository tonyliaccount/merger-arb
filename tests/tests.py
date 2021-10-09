import unittest
from helpers import calculate_merger

class TestCalcMerger(unittest.TestCase):
    def test_positive(self):
        """Check a regular case with a reasonable merger"""
        days = 30 * 4 # ~4 months
        stocks = [{'Name':'KLG', 'Price':51.43}, {'Name':'AEM',
                  'Price':67.29}]
        exchange_range = 0.7935
        margin_interest = 0.04
        commission = 9.99
        position_size = 200000
        initial_margin = 0.4
        assert(calculate_merger(days, stocks, exchange_range, margin_interest,
               commission, position_size, initial_margin), )
