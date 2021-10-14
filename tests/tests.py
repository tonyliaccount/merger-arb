import unittest
from helpers import calculate_acquisition_arb, calculate_shares, \
    margin_call_price, calculate_merger_arb


class CalculateMergerTestCase(unittest.TestCase):
    def test_positive(self):
        """Check a regular case with a reasonable merger"""
        args = {
            'days': 30 * 4,  # ~4 months
            'stocks': [{'Name': 'AEM', 'Price': 67.29},
                       {'Name': 'KLG', 'Price': 51.43}],
            'exchange_rate': 0.7935,
            'margin_interest': 0.04,
            'commission': 9.99,
            'position_size': 200000,
            'initial_margin': 0.4,
        }
        assert round(calculate_merger_arb(**args), 2) == 5467.36


class AcqArbTestCase(unittest.TestCase):
    def test_long(self):
        args = {
                'share_price': 50,
                'acquire_price': 60,
                'days': 190,
                'initial_margin': 0.4,
                'margin_interest': 0.04,
                'commission': 9.99,
                'buying_power': 150000,
        }
        assert round(calculate_acquisition_arb(**args), 2) == 28133.66

    def test_short(self):
        args = {
                'share_price': 70,
                'acquire_price': 60,
                'days': 190,
                'initial_margin': 0.4,
                'margin_interest': 0.04,
                'commission': 9.99,
                'buying_power': 150000,
        }
        assert round(calculate_acquisition_arb(**args), 2) == 19562.23


class CalculateSharesTest(unittest.TestCase):
    def test_base(self):
        """Return appropriate long and short positions"""
        args = {
            'long_price': 51.43,
            'short_price': 67.29,
            'buying_power': 500000,
            'long_short_rate': 1 / 0.7935
        }
        print(calculate_shares(**args)['long_shares'])
        assert round(calculate_shares(**args)['long_shares'], 2) == 4769.87


class MarginCallPriceTestCase(unittest.TestCase):
    def test_base_long(self):
        """Share price dropping below 37.5 trigger margin call"""
        args = {
                'price': 50,
                'initial_margin': 0.4,
                'maintenance_margin': 0.2,
        }
        price = margin_call_price(**args)
        assert price == 37.5

    def test_base_short(self):
        """Share price climbing above 80 triggers margin call"""
        args = {
                'price': 40,
                'initial_margin': 0.4,
                'maintenance_margin': 0.2,
                'type': 'short',
        }
        price = margin_call_price(**args)
        assert price == 80

    def test_stock_price(self):
        """Make sure initial price still can't be negative"""
        args = {
                'price': -50,
                'initial_margin': 0.4,
                'maintenance_margin': 0.2,
        }
        with self.assertRaises(ValueError) as context:
            margin_call_price(**args)
        self.assertTrue("Stock price can't be negative" in
                        str(context.exception))

    def test_initial_margin(self):
        """Make sure initial margin is greater than zero"""
        args = {
                'price': 50,
                'initial_margin': 0,
                'maintenance_margin': 0.2,
        }
        with self.assertRaises(ZeroDivisionError) as context:
            margin_call_price(**args)
        self.assertTrue("Initial margin can't be zero" in
                        str(context.exception))

    def test_maintenance_margin(self):
        """Check that maintenance margin > 0 is working"""
        args = {
                'price': 50,
                'initial_margin': 0.4,
                'maintenance_margin': 0,
        }
        with self.assertRaises(ZeroDivisionError) as context:
            margin_call_price(**args)
        self.assertTrue("Maintenance margin can't be zero" in
                        str(context.exception))

    def test_maintenance_intial_difference(self):
        """Check that initial margin > maintenance margin validation
        is working"""
        args = {
                'price': 50,
                'initial_margin': 0.4,
                'maintenance_margin': 0.5,
        }
        with self.assertRaises(ZeroDivisionError) as context:
            margin_call_price(**args)
        self.assertTrue(("can't be greater than") in str(context.exception))


if __name__ == "__main__":
    unittest.main()
