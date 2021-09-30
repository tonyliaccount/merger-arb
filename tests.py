import helpers


def test_get_price():
    prices= helpers.get_prices(['KL.TO','AEM.TO'])
    for price in prices:
        print (price)


if __name__ == '__main__':
    test_get_price()
