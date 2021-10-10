import unittest
from helpers import margin_call_long

# class CalculateMergerTestCase(unittest.TestCase):
#     def test_positive(self):
#         """Check a regular case with a reasonable merger"""
#         days = 30 * 4 # ~4 months
#         stocks = [{'Name':'KLG', 'Price':51.43}, {'Name':'AEM',
#                   'Price':67.29}]
#         exchange_range = 0.7935
#         margin_interest = 0.04
#         commission = 9.99
#         position_size = 200000
#         initial_margin = 0.4
#         assert(calculate_merger(days, stocks, exchange_range,
#                margin_interest, commission, position_size, initial_margin), )


class MarginCallPriceTestCase(unittest.TestCase):
    def test_base(self):
        """Share price dropping below 37.5 trigger margin call"""
        args = {
                'price': 50,
                'initial_margin': 0.4,
                'maintenance_margin': 0.2,
        }
        margin_call_long_price = margin_call_long(**args)
        assert margin_call_long_price == 37.5

    def test_stock_price(self):
        """Make sure initial price still can't be negative"""
        args = {
                'price': -50,
                'initial_margin': 0.4,
                'maintenance_margin': 0.2,
        }
        with self.assertRaises(ValueError) as context:
            margin_call_long(**args)
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
            margin_call_long(**args)
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
            margin_call_long(**args)
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
            margin_call_long(**args)
        self.assertTrue(("can't be greater than") in str(context.exception))


if __name__ == "__main__":
    unittest.main()
